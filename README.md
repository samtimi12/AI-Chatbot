# AI Chatbot Demo

This is a portfolio-ready Flask application that demonstrates how to build an AI chatbot system with authentication, persistent conversations, and an admin escalation dashboard. The chatbot currently runs in **local mode** (using simulated responses instead of an external API) to keep the project self-contained. API integration can easily be added when scaling to production.

---

## Features

- **User Authentication**: Secure signup, login, and session management with Flask-Login.  
- **Persistent Chat History**: Each logged-in user has their messages stored and retrievable even after logging out.  
- **Chat Interface**: Clean, responsive UI.  
- **FAQ Quick Replies**: Buttons for common questions (hours, pricing, signup, features, contact).  
- **Human Escalation**: Users can request human support; requests appear on the admin dashboard.  
- **Admin Dashboard**: Centralized view for handling pending human requests with status updates.  
- **Local AI Simulation**: Replies are generated locally for demonstration. Easily replaceable with an AI API like OpenAI, Dialogflow, or Rasa if desired.  

---

## Real-World Usage & Value

Although this project is designed as a portfolio demo, it demonstrates the foundations of systems that are actively needed across industries:

- **Customer Support Chatbots**: Businesses (e-commerce, SaaS, logistics) use chatbots to handle repetitive customer queries (hours, pricing, features) before escalating to human agents.  
- **Internal Team Tools**: Companies deploy lightweight chat assistants for staff to quickly retrieve company policies, workflow guides, or FAQs.  
- **Persistent Communication Systems**: The concept of saving chat history per user is a core requirement in messaging apps, CRMs, and ticketing systems.  
- **Authentication & Session Management**: Any real-world SaaS, dashboard, or platform requires secure login and user-specific data handling — a direct parallel to what is built here.  
- **Admin Oversight (Scalability)**: The human request handling system mirrors real-world escalation systems used in call centers and support desks.  

### Who Needs This?

- **Small businesses** that want a lightweight FAQ/chat system without paying for expensive third-party SaaS.  
- **Tech startups** prototyping chat-based products before scaling to APIs.  
- **Developers** who need a boilerplate for Flask apps with authentication, persistence, and messaging.  
- **Students / Researchers** who want to learn full-stack development with a practical, end-to-end project.  

In short, the value here is not just a chatbot — it’s a **template for scalable, real-world systems** that can be adapted for e-commerce, helpdesks, and any app requiring **auth + messaging + persistence**.

---

## Tech Stack

- **Backend**: Flask (Python), Flask-Login  
- **Frontend**: HTML, CSS, Vanilla JS  
- **Database**: SQLite (lightweight, file-based persistence)  
- **Authentication**: Session-based with secure password hashing  

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-chatbot-demo.git
   cd ai-chatbot-demo

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate    # macOS/Linux
    venv\Scripts\activate       # Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Run the application:
    flask run

5. Visit:
    http://127.0.0.1:5000

### Project Structure

/ai-chatbot-demo
│── /app
│   ├── /routes        # Flask route handlers
│   ├── /templates     # HTML templates (Jinja2)
│   ├── /static
│   │   ├── /css       # Custom styles (style.css)
│   │   └── /js        # Frontend logic
│   └── models.py      # Database models
│── requirements.txt   # Dependencies
│── run.py             # Entry point
│── README.md          # Documentation

#### Notes on AI Integration

This demo intentionally uses local simulated responses to avoid API dependency and ensure the project runs anywhere with no setup costs.
For real-world deployment, the response generator can be replaced with:
- OpenAI API (ChatGPT, GPT-4)
- Dialogflow / Rasa for structured bots
- Custom ML Models if specialized domain knowledge is needed

##### License
This project is released under the MIT License. You are free to use, modify, and distribute with attribution.