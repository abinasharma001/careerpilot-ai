from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from notion_client import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔐 Secure credentials (from .env)
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)


# 📊 Fetch jobs from Notion
def get_jobs():
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID
        )
        return response["results"]
    except Exception as e:
        print("Notion Error:", e)
        return []


# 🏠 Serve frontend UI
@app.route("/")
def home():
    return render_template("index.html")


# 🤖 AI Logic
def smart_ai(query, jobs):
    total = len(jobs)

    # Extract some info
    companies = []
    statuses = []

    for job in jobs:
        props = job.get("properties", {})

        # Company name
        company = props.get("Company", {}).get("title", [])
        if company:
            companies.append(company[0]["plain_text"])

        # Status
        status = props.get("Status", {}).get("select")
        if status:
            statuses.append(status["name"])

    # Logic responses
    if "how many" in query or "applied" in query:
        return f"You have applied to {total} jobs."

    elif "company" in query:
        return f"You applied to: {', '.join(companies) if companies else 'No companies found'}"

    elif "interview" in query:
        interviews = statuses.count("Interview")
        return f"You have {interviews} interviews scheduled."

    elif "status" in query:
        return f"Statuses: {', '.join(statuses)}"

    elif "suggest" in query or "improve" in query:
        if total < 5:
            return "Apply to more companies 🚀"
        elif total < 10:
            return "Good progress 👍 Keep applying!"
        else:
            return "Great job! Focus on interview prep 🎯"

    else:
        return "Ask me about your job applications 📊"


# 🤖 API route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        query = data.get("query", "").lower()

        jobs = get_jobs()

        answer = smart_ai(query, jobs)

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": "⚠️ Error: " + str(e)})


# 🚀 Run app
if __name__ == "__main__":
    app.run(debug=True)
