from flask import Blueprint, request, jsonify
import random
import smtplib
from email.message import EmailMessage
import hashlib
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb+srv://saahosan3:tSMiuQ1MlMBPNdAS@cluster0.ux4ex.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['finwise_db']
users_collection = db['users']

forgotpw_bp = Blueprint('forgotpw_bp', __name__, url_prefix='/auth')

# Store OTPs temporarily (in memory)
otp_store = {}

from flask import render_template

@forgotpw_bp.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgotpw.html')


# Hash password function
def hash_password(password):
    """Hash the password before storing it."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Route to send OTP to the user's email
@forgotpw_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400

    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    otp_store[email] = otp

    print(f"[DEBUG] OTP for {email} is {otp}")

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Your Password Reset OTP'
        msg['From'] = 'finwise.org@gmail.com'
        msg['To'] = email
        msg.set_content(f'Your verification code is: {otp}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('finwise.org@gmail.com', 'upuu pgff qotl vqvu')  # Replace with your actual app password
            smtp.send_message(msg)

        return jsonify({'success': True, 'message': 'OTP sent to your email'})
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'success': False, 'message': 'Failed to send OTP'}), 500

# Route to verify OTP
@forgotpw_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({'success': False, 'message': 'Email and OTP code are required'}), 400

    expected_code = otp_store.get(email)

    if expected_code == code:
        # Optionally: delete used OTP
        del otp_store[email]
        return jsonify({'success': True, 'message': 'OTP verified successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid or expired OTP'}), 401

# Route to reset the password
@forgotpw_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({'success': False, 'message': 'Email and new password are required'}), 400

    # Hash the new password
    hashed_password = hash_password(new_password)

    # Update the password in the database
    result = users_collection.update_one(
        {"email": email},  # Match user by email
        {"$set": {"password": hashed_password}}  # Set the new hashed password
    )

    # Debug log to check if the update was successful
    if result.matched_count == 0:
        print(f"[DEBUG] No matching email found for {email}. No update performed.")
    else:
        print(f"[DEBUG] Password updated for {email}. Document modified: {result.modified_count}")

    # Check if the update was successful
    if result.matched_count > 0 and result.modified_count > 0:
        return jsonify({'success': True, 'message': 'Password reset successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update password or email not found'}), 404

