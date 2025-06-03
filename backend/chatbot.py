from flask import Blueprint, request, jsonify, render_template
import google.generativeai as genai
import re

# Configure Gemini API
genai.configure(api_key="your_API_key")

# Create Flask Blueprint
chatbot_bp = Blueprint('chatbot', __name__)

# Chat messages for context
messages = [{"role": "system", "content": "You are an expert financial assistant with deep knowledge of investments, budgeting, and risk management. Your responses should be highly detailed, incorporating relevant symbols (%, $, ₹, €), numerical measures, and critical financial warnings or cautions where necessary. Always provide structured insights, highlight important points with bullet points, and emphasize risks with cautionary symbols (⚠️) to help users make well-informed financial decisions.If a question is unrelated to finance, politely refuse to answer."}]


def format_text(text: str) -> str:
    """Formats generated text with HTML structure."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = text.replace("\n", "<br>")
    text = re.sub(r'- (.*?)(?=<br>|$)', r'<li>\1</li>', text)
    if "<li>" in text:
        text = f"<ul>{text}</ul>"
    return text

# Route to render chatbot page
# @chatbot_bp.route("/chatbot")
# def chatbot_page():
#     return render_template("chatbot.html")

# Route to handle chatbot messages
@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    messages.append({"role": "user", "content": user_message})

    conversation_context = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(conversation_context)

    reply = format_text(response.text)
    messages.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})
