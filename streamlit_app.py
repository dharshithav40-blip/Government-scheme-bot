import streamlit as st
import requests

# Page settings
st.set_page_config(
    page_title="Government Scheme Chatbot",
    layout="centered"
)

# Sidebar
with st.sidebar:

    st.header("About")

    st.write(
        "Government Scheme Chatbot"
    )

    st.write(
        "Built using FastAPI and Streamlit"
    )

    st.write(
        "Mini Project"
    )

# Title
st.title("Government Scheme Chatbot")

# Welcome message
st.success(
    "Welcome to Government Scheme Chatbot"
)

# Instructions
st.info(
    "Try queries like: student, farmer, female, education"
)

# Store messages
if "messages" not in st.session_state:

    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat input
query = st.chat_input(
    "Ask about government schemes..."
)

# If user enters query
if query:

    # Save user message
    st.session_state.messages.append({

        "role": "user",

        "content": query

    })

    # Show user message
    with st.chat_message("user"):

        st.markdown(query)

    try:

        # FastAPI URL
        url = (
            f"http://127.0.0.1:8000/"
            f"search?query={query}"
        )

        # Send request
        response = requests.get(url)

        # Convert to JSON
        data = response.json()

        # If schemes found
        if "results" in data:

            bot_reply = ""

            for scheme in data["results"]:

                bot_reply += (
                    f"{scheme['answer']}\n\n"
                )

        # No results
        else:

            bot_reply = data["message"]

    # Backend error
    except:

        bot_reply = (
            "FastAPI server is not running"
        )

    # Save bot response
    st.session_state.messages.append({

        "role": "assistant",

        "content": bot_reply

    })

    # Show bot response
    with st.chat_message("assistant"):

        st.markdown(bot_reply)