import hashlib
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage

# MongoDB Connection
MONGO_URI = "mongodb+srv://saahosan3:tSMiuQ1MlMBPNdAS@cluster0.ux4ex.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['finwise_db']
users_collection = db['users']

# Create Flask Blueprint
signup_bp = Blueprint('signup', __name__)

# Temporary OTP storage for signup
signup_otp_store = {}

# Email configuration
EMAIL_ADDRESS = 'finwise.org@gmail.com'
EMAIL_PASSWORD = 'upuu pgff qotl vqvu'  # Replace with your actual app password

# Hash password
def hash_password(password):
    """Hash the password before storing it."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Flask Route: Send OTP for Signup
@signup_bp.route("/send-otp-signup", methods=["POST"])
def send_otp_signup():
    """Send OTP to the user's email for signup."""
    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")

    if not email or not full_name:
        return jsonify({"success": False, "message": "Email and full name are required"}), 400

    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    signup_otp_store[email] = {"otp": otp, "full_name": full_name} # Store OTP and full name

    print(f"[DEBUG] Signup OTP for {email} is {otp}")

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Verify Your Email for Finwise Signup'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg.set_content(f'Your verification code is: {otp}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return jsonify({"success": True, "message": "OTP sent to your email"})
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"success": False, "message": "Failed to send OTP"}), 500

# Flask Route: Verify OTP for Signup
@signup_bp.route("/verify-otp-signup", methods=["POST"])
def verify_otp_signup():
    """Verify the OTP entered by the user during signup."""
    data = request.json
    email = data.get("email")
    code = data.get("code")

    if not email or not code:
        return jsonify({"success": False, "message": "Email and OTP code are required"}), 400

    stored_data = signup_otp_store.get(email)

    if stored_data and stored_data["otp"] == code:
        # Optionally, remove the OTP after successful verification
        del signup_otp_store[email]
        return jsonify({"success": True, "message": "OTP verified successfully", "full_name": stored_data["full_name"]})
    else:
        return jsonify({"success": False, "message": "Invalid or expired OTP"}), 401

# Flask Route: Signup (after OTP verification)
@signup_bp.route("/signup", methods=["POST"])
def signup():
    """Handle user signup after OTP verification."""
    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not all([full_name, email, password]):
        return jsonify({"message": "Full name, email, and password are required"}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Insert new user into the database
    new_user = {
        "full_name": full_name,
        "email": email,
        "password": hashed_password  # Store hashed password
    }

    # Add user to the MongoDB database
    users_collection.insert_one(new_user)

    # Return a success message
    return jsonify({"success": True, "message": "Account created successfully! Redirecting to login page..."}), 201