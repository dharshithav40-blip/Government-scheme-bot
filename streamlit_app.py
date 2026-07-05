
import streamlit as st
import requests


st.set_page_config(
    page_title="Government Scheme Chatbot",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Light background */
.stApp { background: #F4F6FB; }

/* Sidebar – white with navy left border */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 3px solid #1A3A6B !important;
    box-shadow: 2px 0 12px rgba(26,58,107,.07);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stMarkdown { color: #1E293B !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1A3A6B !important; }

/* Title */
h1 {
    font-family: 'Rajdhani', sans-serif !important;
    color: #1A3A6B !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}
h2, h3 { color: #1A3A6B !important; }

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
    color: #1E293B !important;
    box-shadow: 0 1px 4px rgba(26,58,107,.07) !important;
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    border: 1.5px solid #1A3A6B !important;
    color: #1E293B !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar quick-search buttons */
.stButton > button {
    background: #EEF2FF !important;
    border: 1px solid #C7D2FE !important;
    color: #1A3A6B !important;
    font-weight: 600 !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    width: 100%;
    margin-bottom: 4px;
    transition: background .2s !important;
}
.stButton > button:hover {
    background: #1A3A6B !important;
    color: #fff !important;
    border-color: #1A3A6B !important;
}

/* Alert boxes */
div[data-testid="stAlert"] { border-radius: 10px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #C7D2FE; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

FASTAPI_URL = "http://127.0.0.1:8000"


with st.sidebar:
    st.markdown("## 🏛️ Govt Scheme Bot")
    st.markdown("**v2.0** · FastAPI + Streamlit")
    st.markdown("---")
    st.markdown("#### ⚡ Quick Search")

    categories = [
        ("🎓", "student"),
        ("🌾", "farmer"),
        ("👩", "female"),
        ("👴", "senior citizen"),
        ("📚", "education"),
        ("🏠", "housing"),
        ("🏥", "health"),
        ("🛠️",  "skill"),
        ("💡", "startup"),
    ]
    for icon, cat in categories:
        if st.button(f"{icon} {cat.title()}"):
            st.session_state["pending_query"] = cat

    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.markdown("""
- 11 government schemes
- Category + keyword search
- FastAPI REST backend
- Query logging & admin
    """)
    st.markdown("---")
    st.markdown("*By **Dharshitha***")


st.markdown("# 🏛️ Government Scheme Chatbot")
st.success("✅ Ask about any scheme — student, farmer, health, housing, startup and more!")
st.info("💡 Type a category below or click a quick-search button on the left.")


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Namaste! 🙏 I am your **Government Scheme Assistant**.\n\n"
                "Tell me your category — *student, farmer, female, senior citizen, "
                "education, housing, health, skill,* or *startup* — "
                "and I will find the right schemes for you!"
            )
        }
    ]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


query = None
if "pending_query" in st.session_state:
    query = st.session_state.pop("pending_query")
else:
    query = st.chat_input("Ask about government schemes…")


if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    try:
        resp = requests.get(f"{FASTAPI_URL}/search", params={"query": query}, timeout=5)
        data = resp.json()

        if data.get("results"):
            bot_reply = f"✅ **{data['message']}**\n\n"
            for s in data["results"]:
                bot_reply += (
                    f"---\n"
                    f"### 📋 {s['name']}\n"
                    f"**Category:** `{s['category']}`\n\n"
                    f"**Benefits:** {s['benefits']}\n\n"
                    f"**Eligibility:** {s['eligibility']}\n\n"
                    f"**How to Apply:** {s['how_to_apply']}\n\n"
                    f"**Source:** {s['source']}\n\n"
                )
        else:
            bot_reply = (
                f"❌ **{data['message']}**\n\n"
                "Try one of these:\n\n"
                "`student` · `farmer` · `female` · `senior citizen` · "
                "`education` · `housing` · `health` · `skill` · `startup`"
            )

    except requests.exceptions.ConnectionError:
        bot_reply = (
            "⚠️ **Cannot reach the FastAPI backend.**\n\n"
            "Start it in a separate terminal:\n"
            "```bash\npython fastapi_app.py\n```"
        )
    except Exception as e:
        bot_reply = f"⚠️ Error: `{e}`"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
