from notion_client import Client
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 YOUR CONFIG
NOTION_API_KEY = "secret_xxx"
DATABASE_ID = "330012223c0b80c1b915e21483ad2a62"

notion = Client(auth=NOTION_API_KEY)

# 📊 Fetch jobs from Notion
def get_jobs():
    response = notion.databases.query(
        database_id=DATABASE_ID
    )
    return response["results"]

# 🏠 Home route
@app.route("/")
def home():
    return "🚀 CareerPilot AI Backend Running!"

# 🤖 Smart AI Route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        query = data.get("query", "").lower()

        jobs = get_jobs()

        # 📊 Count jobs
        if "how many" in query or "applied" in query:
            return jsonify({
                "answer": f"You have applied to {len(jobs)} jobs 📊"
            })

        # 🏢 List companies
        elif "company" in query or "companies" in query:
            companies = []

            for job in jobs:
                try:
                    name = job["properties"]["Company"]["title"][0]["text"]["content"]
                    companies.append(name)
                except:
                    pass

            if companies:
                return jsonify({
                    "answer": "You applied to: " + ", ".join(companies)
                })
            else:
                return jsonify({
                    "answer": "No companies found"
                })

        # 📌 Status breakdown
        elif "status" in query:
            status_count = {}

            for job in jobs:
                try:
                    status = job["properties"]["Status"]["status"]["name"]
                    status_count[status] = status_count.get(status, 0) + 1
                except:
                    pass

            if status_count:
                result = ", ".join([f"{k}: {v}" for k, v in status_count.items()])
                return jsonify({
                    "answer": f"Your application status: {result}"
                })
            else:
                return jsonify({
                    "answer": "No status data found"
                })

        # 🚀 Suggestions
        elif "suggest" in query or "advice" in query:
            return jsonify({
                "answer": "🚀 Suggestion: Apply to at least 3 more companies this week and focus on high-priority roles!"
            })

        # 🎯 Default
        else:
            return jsonify({
                "answer": "🤖 I can help with job tracking, companies, status, and suggestions!"
            })

    except Exception as e:
        return jsonify({
            "answer": "⚠️ Error: " + str(e)
        })

# ▶️ Run server
if __name__ == "__main__":
    app.run(debug=True)