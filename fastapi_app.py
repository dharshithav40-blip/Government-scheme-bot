from fastapi import FastAPI
import json
import uvicorn
import webbrowser

app = FastAPI()

# Load JSON data
with open("schemes.json") as f:
    schemes = json.load(f)

# Home API
@app.get("/")
def home():

    return {
        "message":
        "Government Scheme Bot Running"
    }

# Search API
@app.get("/search")
def search(query: str):

    # Save history
    with open("history.txt", "a") as file:
        file.write(query + "\n")

    query = query.lower()

    results = []

    # Search schemes
    for s in schemes:

        if (
            query in s["category"].lower()
            or
            query in s["name"].lower()
        ):

            # Chatbot-style answer
            answer = f"""
You are eligible for {s['name']}.

Benefits:
{s['benefits']}

Source:
{s['source']}
"""

            results.append({

                "answer": answer

            })

    # Return results
    if results:

        return {

            "message":
            "Matching schemes found",

            "results":
            results

        }

    else:

        return {

            "message":
            "Sorry, no matching schemes found"

        }

# Admin API
admin_password = "admin123"

@app.get("/admin")
def admin(password: str):

    if password == admin_password:

        return {

            "message":
            "Admin access granted"

        }

    else:

        return {

            "message":
            "Access denied"

        }

# Run FastAPI
if __name__ == "__main__":

    webbrowser.open(
        "http://127.0.0.1:8000/docs"
    )

    uvicorn.run(
        "fastapi_app:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )