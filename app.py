from flask import Flask, render_template,session,redirect, url_for
from backend.login import login_bp  # Import the Blueprint
from backend.chatbot import chatbot_bp  # Import chatbot blueprint
from backend.predict_bp import predict_bp
from backend.signup import signup_bp  
from backend.search import search_bp 
from backend.contact import contact_bp
from backend.forgotpw import forgotpw_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Register the login Blueprint
app.register_blueprint(login_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(signup_bp, url_prefix='/auth')
app.register_blueprint(search_bp, url_prefix="/api")
app.register_blueprint(contact_bp)
app.register_blueprint(forgotpw_bp)



@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def home():
    return render_template("prelogin.html")


@app.route("/chatbot")
def chatbot():
    if 'user' not in session:
        print("Chatbot route accessed")
        return redirect(url_for('home'))
    
    return render_template("chatbot.html")

@app.route("/index")
def index():

    if 'user' not in session:
        return redirect(url_for('home'))
    
    full_name = session.get('full_name')  # Retrieve the full name from session if logged in
    # Render the index page and pass full_name to the template
    return render_template('index.html', full_name=full_name)

@app.route("/login", methods=['GET'])
def login_page():
    return render_template("login.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/budgets")
def budgets():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template("budgets.html")

@app.route("/reminders")
def reminders():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template("reminders.html")

@app.route("/calculators")
def calculators():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template("calculators.html")

@app.route("/prediction")
def prediction():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template("prediction.html")

@app.route('/signout')
def signout_page():
    # if 'user' not in session:
    #     return redirect(url_for('home'))
    return render_template('signout.html')


@app.route("/faq")
def faq():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template("faq.html")

@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))  # assuming 'home' is your prelogin route name







if __name__ == "__main__":
    app.run(debug=True)
