# FINWISE – A Financial Advisor Application

FINWISE is an AI-powered personal finance platform that simplifies budgeting, bill tracking, financial calculators (SIP, mutual funds, stock forecasting), and financial literacy through an all-in-one web-based solution. Built to address the growing need for integrated financial tools and improved financial awareness among young adults, FINWISE combines intelligent automation with user-centric design to empower smarter money management.

Features-

🔐 Secure Login & Dashboard – SHA-256 password hashing with session-based user authentication.
📊 Expense Tracking & Budgeting – Log and categorize expenses, set budgets, and visualize spending.
⏰ Bill Reminders – Schedule recurring bills and receive in-app alerts via Moment.js.
🤖 AI Financial Chatbot – Get real-time financial advice using Google Generative AI.
📈 Stock Price Prediction – Forecast stock trends using a hybrid LSTM + ARIMA model.
🧮 Financial Calculators – Built-in EMI, SIP, FD, and compound interest tools.
📰 Live Financial News – Ticker-based stock news updates using NewsAPI.
🏗️ Architecture

Frontend: HTML5, CSS3, JavaScript (ES6+), Chart.js, Plotly.js
Backend: Python, Flask, TensorFlow, Keras, NumPy, scikit-learn, PyMongo
Database: MongoDB (NoSQL)
APIs: Google Generative AI, NewsAPI
Security: SHA-256 hashing, session tokens, input validation

System Design:-

Modular architecture with Flask backend and MongoDB for persistent storage
Predictive models (LSTM + ARIMA) for stock forecasting
Chatbot integration with Google's GenAI for personalized responses

Screenshots:
Home Page(Before Login)
<img width="1440" alt="Screenshot 2025-06-02 at 9 47 00 PM" src="https://github.com/user-attachments/assets/2cae6553-b588-4f3f-9d64-3c4d2c93b3e3" />
Login Page
<img width="1440" alt="Screenshot 2025-06-02 at 9 47 42 PM" src="https://github.com/user-attachments/assets/373dbbfe-5103-4799-9474-8f45fd058f06" />
Signup Page
<img width="1440" alt="Screenshot 2025-06-02 at 9 47 29 PM" src="https://github.com/user-attachments/assets/8a25f83c-9480-4d40-960a-6a075e1fd9fd" />
Dashboard(index.html)
<img width="1440" alt="Screenshot 2025-06-02 at 9 47 50 PM" src="https://github.com/user-attachments/assets/91203964-da1a-49bd-b81e-b19aa1073a27" />
Expense Tracker
<img width="1440" alt="Screenshot 2025-06-02 at 9 48 27 PM" src="https://github.com/user-attachments/assets/5d75d0c5-5ae3-4a8b-86fb-968b6a951479" />
Chatbot Interface
<img width="1440" alt="Screenshot 2025-06-02 at 9 48 12 PM" src="https://github.com/user-attachments/assets/eb4c6a9d-339a-4a78-aff4-c378320a448b" />
Stock Prediction with News Headlines
<img width="1440" alt="Screenshot 2025-06-02 at 9 56 26 PM" src="https://github.com/user-attachments/assets/e64d4ce0-98b9-4682-9bf5-bbccf48a1163" />
Budget and Bill Reminder Tools
![Screenshot 2025-06-02 at 9 57 12 PM](https://github.com/user-attachments/assets/575e0b7a-c3bf-4ba3-86bb-958d478cf5f9)

🚀 How to Run Locally

### 📁 Project Structure

```text
├── app.py                  # Main application entry point  
├── backend/                # Backend logic and utilities  
│   ├── login.py  
│   ├── predict.py  
│   └── ...                 # Additional backend Python files  
├── templates/              # HTML templates for the frontend  
│   ├── index.html  
│   ├── login.html  
│   └── ...                 # Additional HTML files  

🚀 How to Run Locally

Clone the repository:
git clone https://github.com/Sri_Varsha__/Finwise.git
cd finwise
Install Python dependencies:
pip install -r requirements.txt
Set up MongoDB and update the connection URI in the Flask config.
Run the Flask app:
python app.py
Open your browser and navigate to http://localhost:5000

📦 Requirements

Python 3.8+
Flask
TensorFlow, Keras, scikit-learn
MongoDB
Internet access for API calls (chatbot and news)

📚 Future Enhancements

☁️ Cloud deployment with real-time syncing
🌐 Banking API integration for live tracking
🔔 Smart alerts for bills and spending
🌎 Multi-currency support
📱 Android/iOS mobile app versions
📖 License

This project is developed as part of an academic curriculum and is available for educational and non-commercial use only.

