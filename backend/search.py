from flask import Blueprint, request, jsonify
import requests

search_bp = Blueprint('search', __name__)

API_KEY = "b0bf92d6610c497ab1bcd6ba34432868"  # Replace with your actual API Key

@search_bp.route("/news", methods=["GET"])
def get_news():
    ticker = request.args.get("company")

    if not ticker:
        return jsonify({"error": "Company ticker is required"}), 400

    # Remove exchange suffix like .NS, .BO, .L, etc.
    base_ticker = ticker.split(".")[0]

    # Use the cleaned ticker in the search query
    url = f"https://newsapi.org/v2/everything?q={base_ticker}&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"News API request failed: {str(e)}"}), 500

    if "articles" in news_data and news_data["articles"]:
        return jsonify(news_data["articles"][:4])  # Return top 4 articles
    else:
        return jsonify({"error": f"No news found for {base_ticker}"}), 404
