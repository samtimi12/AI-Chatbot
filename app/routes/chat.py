from flask import Blueprint, request, jsonify, render_template, abort
from flask_login import login_required, current_user
from app import db
from app.models import Message
from functools import wraps

try:
    from app.services.ai_service import get_ai_response
except ImportError:
    from ..services.ai_service import get_ai_response


chat_bp = Blueprint("chat", __name__)

# -----------------------------
# Admin decorator
# -----------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


# -----------------------------
# Local FAQ dictionary (fallbacks)
# -----------------------------
FAQ_RESPONSES = {
    "hours": "Our support is available 9am–5pm Monday–Friday.",
    "pricing": "Pricing starts at $50/month for the basic plan.",
    "signup": "You can sign up using the registration form on the home page.",
    "features": "Our chatbot can answer FAQs and allow you to request a human admin.",
    "contact": "You can contact support via email: support@example.com."
}


# -----------------------------
# Dashboard page
# -----------------------------
@chat_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# Send a new message (FAQ + AI + human request)
# -----------------------------
@chat_bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    request_human_flag = False
    bot_reply_text = ""

    # 1. First check FAQ
    for keyword, response in FAQ_RESPONSES.items():
        if keyword in user_message.lower():
            bot_reply_text = response
            break

    # 2. If no FAQ match, check for human/help request
    if not bot_reply_text:
        if "human" in user_message.lower() or "help" in user_message.lower():
            bot_reply_text = "An admin will contact you soon!"
            request_human_flag = True
        else:
            # 3. Otherwise try AI service (OpenAI)
            bot_reply_text = get_ai_response(user_message)

    # Save user message
    user_msg = Message(
        user_id=current_user.id,
        sender="user",
        text=user_message,
        request_human=request_human_flag,
    )
    db.session.add(user_msg)

    # Save bot reply
    bot_msg = Message(
        user_id=current_user.id,
        sender="bot",
        text=bot_reply_text,
    )
    db.session.add(bot_msg)
    db.session.commit()

    # Return response for frontend typing effect handling
    return jsonify({
        "status": "done",
        "reply": bot_reply_text
    })


# -----------------------------
# Load chat history
# -----------------------------
@chat_bp.route("/chat/history", methods=["GET"])
@login_required
def chat_history():
    messages = (
        Message.query.filter_by(user_id=current_user.id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    return jsonify(
        [
            {
                "sender": m.sender,
                "text": m.text,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in messages
        ]
    )


# -----------------------------
# Admin Dashboard page
# -----------------------------
@chat_bp.route("/admin-dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Unauthorized", 403
    return render_template("admin_dashboard.html")


# -----------------------------
# View pending human requests (Admin only)
# -----------------------------
@chat_bp.route("/admin/requests", methods=["GET"])
@login_required
@admin_required
def admin_human_requests():
    messages = (
        Message.query.filter_by(request_human=True, handled=False)
        .order_by(Message.timestamp.desc())
        .all()
    )
    return jsonify(
        [
            {
                "id": m.id,
                "user": m.user.username,
                "text": m.text,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in messages
        ]
    )


# -----------------------------
# Mark human request as handled (Admin only)
# -----------------------------
@chat_bp.route("/admin/requests/<int:msg_id>/handle", methods=["POST"])
@login_required
@admin_required
def handle_request(msg_id):
    msg = Message.query.get_or_404(msg_id)
    msg.handled = True
    db.session.commit()
    return jsonify({"status": "success"})
