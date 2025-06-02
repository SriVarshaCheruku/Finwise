from flask import Blueprint, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
import hashlib  # To use sha256 for password hashing

# MongoDB Connection
MONGO_URI = "mongodb+srv://saahosan3:tSMiuQ1MlMBPNdAS@cluster0.ux4ex.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['finwise_db']
users_collection = db['users']

# Create Flask Blueprint
login_bp = Blueprint('login', __name__)

def hash_password(password):
    """Hash the password using SHA-256 before comparison."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def authenticate_user(email, password):
    """Check if email and password match in MongoDB."""
    user = users_collection.find_one({"email": email})
    if user:
        stored_password = user['password']  # The hashed password from MongoDB
        hashed_password = hash_password(password)  # Hash the entered password to compare

        if stored_password == hashed_password:
            return True
    return False

# Flask Route: Login
@login_bp.route("/login", methods=["POST"])
def login():
    """Handle login request"""
    data = request.json  # Get JSON data from frontend
    email = data.get("email")
    password = data.get("password")

    if authenticate_user(email, password):

        print('HELLLO')
        # Fetch the user's full name
        user = users_collection.find_one({"email": email})
        full_name = user["full_name"]

        # Store user details in session
        session["user"] = email
        session["full_name"] = full_name  # Store the full name in session

        return jsonify({"message": "Login successful", "redirect": url_for("index")}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# Flask Route: Dashboard (Protected Page)
@login_bp.route("/dashboard")
def dashboard():
    """A protected page, accessible only if logged in"""
    if "user" in session:
        return f"Welcome, {session['full_name']}! This is your dashboard."
    else:
        return redirect(url_for("login"))
