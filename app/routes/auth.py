from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


# 🏠 Home
@auth_bp.route('/')
def home():
    return render_template('home.html')


# 📝 Signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        # Already logged in → redirect to dashboard
        return redirect(url_for('chat.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('auth.signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))  # Redirect to login after signup
    return render_template('signup.html')


# 🔑 Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Already logged in → redirect to dashboard
        return redirect(url_for('chat.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('chat.dashboard'))  #  redirect to dashboard
    return render_template('login.html')




# 🚪 Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.home'))
