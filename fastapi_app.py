# ─────────────────────────────────────────────────────────────
#  fastapi_app.py  –  REST API Backend  |  Government Scheme Bot v2.0
#  Run  :  python fastapi_app.py
#  Docs :  http://127.0.0.1:8000/docs
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import uvicorn
import webbrowser


app = FastAPI(
    title="Government Scheme Bot API",
    description="Search Indian government schemes by category or name.",
    version="2.0.0"
)

# Allow Streamlit frontend and browser to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


with open("schemes.json", encoding="utf-8") as f:
    schemes = json.load(f)

HISTORY_FILE   = "history.txt"
ADMIN_PASSWORD = "admin123"   # Change this before deploying!



def log_query(query: str):
    """Append search query with timestamp to history.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {query}\n")



@app.get("/", tags=["General"])
def home():
    """Health check – confirms the API is running."""
    return {
        "status":    "ok",
        "message":   "Government Scheme Bot API v2.0 is running",
        "endpoints": ["/search", "/schemes", "/history", "/admin"]
    }


@app.get("/search", tags=["Schemes"])
def search(
    query: str = Query(..., description="Category or scheme name (e.g. student, farmer, health)")
):
    """
    Search government schemes by category or name keyword.
    Every query is logged automatically to history.txt.
    """
    log_query(query)
    q = query.strip().lower()

    results = []
    for s in schemes:
        if q in s["category"].lower() or q in s["name"].lower():
            results.append({
                "name":          s["name"],
                "category":      s["category"],
                "benefits":      s["benefits"],
                "eligibility":   s.get("eligibility", "See official portal"),
                "how_to_apply":  s.get("how_to_apply", "Visit official portal"),
                "source":        s["source"],
                "answer": (
                    f"You may be eligible for {s['name']}.\n\n"
                    f"Benefits: {s['benefits']}\n\n"
                    f"Eligibility: {s.get('eligibility', 'See official portal')}\n\n"
                    f"How to Apply: {s.get('how_to_apply', 'Visit official portal')}\n\n"
                    f"Source: {s['source']}"
                )
            })

    if results:
        return {
            "status":  "success",
            "query":   query,
            "count":   len(results),
            "message": f"{len(results)} scheme(s) found",
            "results": results
        }

    return {
        "status":  "not_found",
        "query":   query,
        "count":   0,
        "message": "No matching schemes found. Try: student, farmer, female, senior citizen, education, housing, health, skill, startup",
        "results": []
    }


@app.get("/schemes", tags=["Schemes"])
def all_schemes():
    """Return all available government schemes."""
    categories = sorted({s["category"] for s in schemes})
    return {
        "total":      len(schemes),
        "categories": categories,
        "schemes":    schemes
    }


@app.get("/history", tags=["Admin"])
def get_history(
    password: str = Query(..., description="Admin password required")
):
    """View recent search history. Admin only."""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        return {
            "total_queries": len(lines),
            "recent_10":     lines[-10:]
        }
    except FileNotFoundError:
        return {"total_queries": 0, "recent_10": []}


@app.get("/admin", tags=["Admin"])
def admin(
    password: str = Query(..., description="Admin password")
):
    """Admin dashboard – view query stats and top searches."""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        # Count top queries (strip timestamp prefix)
        counts: dict = {}
        for line in lines:
            q = line.split("] ")[-1].strip().lower() if "]" in line else line.lower()
            counts[q] = counts.get(q, 0) + 1

        top5 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "message":       "Admin access granted",
            "total_queries": len(lines),
            "top_searches":  [{"query": q, "count": c} for q, c in top5]
        }
    except FileNotFoundError:
        return {"message": "Admin access granted", "total_queries": 0, "top_searches": []}



if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000/docs")
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)
