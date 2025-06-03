from flask import Blueprint, render_template, request, flash, redirect, url_for
import smtplib
from email.message import EmailMessage

contact_bp = Blueprint('contact_bp', __name__, template_folder='templates')

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('contact-email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        print(f"Received: {name}, {email}, {subject}, {message}")  # Debug log

        try:
            msg = EmailMessage()
            msg['Subject'] = f'Contact Form: {subject}'
            msg['From'] = 'finwise.org@gmail.com'
            msg['To'] = 'finwise.org@gmail.com'
            msg.set_content(f"From: {name} <{email}>\n\n{message}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('finwise.org@gmail.com', 'app_password')  # Replace securely
                smtp.send_message(msg)

            flash('Message sent successfully!', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Something went wrong while sending your message.', 'danger')

        return redirect(url_for('contact_bp.contact'))

    return render_template('contact.html')
