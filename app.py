import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from crew import run_crew
from resume_parser import extract_text_from_pdf
from tools import search_youtube
from ai_chatbot import chat_with_ai

# ------------------ CONFIG ------------------ #
st.set_page_config(page_title="CareerPilot AI - Your AI Career Mentor", layout="wide")
st.title("🚀 CareerPilot AI - Navigate Your Future with Intelligence")

# ------------------ CSS ------------------ #
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #0f172a);
}
.chat-user {
    background-color: #38bdf8;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
    color: black;
}
.chat-bot {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    color: white;
}
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

/* Floating Chat Button */
.chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #38bdf8;
    color: black;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 28px;
    text-align: center;
    line-height: 60px;
}

/* Chat Box */
.chat-box {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 350px;
    height: 450px;
    background: #1e293b;
    border-radius: 10px;
    padding: 10px;
    overflow-y: auto;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

st.caption("Chat with your AI Career Mentor")

# ------------------ SESSION ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ INPUT ------------------ #
uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])
goal = st.text_input("🎯 Enter Career Goal")

# ------------------ ANALYZE ------------------ #
if st.button("✨ Analyze"):

    if not uploaded_file or not goal:
        st.warning("Upload resume & enter goal")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)

    user_msg = f"I want to become a {goal}"
    st.session_state.messages.append(("user", user_msg))

    with st.spinner("🤖 Thinking..."):

        crew_output = run_crew(resume_text, goal)

        if crew_output is None:
            st.error("❌ AI system failed to generate output. Try again.")
            st.stop()

        # Extract output safely
        try:
            result = crew_output.raw
        except:
            try:
                result = str(crew_output)
            except:
                st.error("❌ Unexpected output format")
                st.stop()
        result = result.strip().replace("```json", "").replace("```", "")

        try:
            data = json.loads(result)
        except:
            st.error("JSON parsing failed")
            st.write(result)
            st.stop()

    st.session_state.messages.append(("bot", data))

# ------------------ MAIN OUTPUT ------------------ #
for role, msg in st.session_state.messages:

    if role == "user":
        st.markdown(f"<div class='chat-user'>🧑 {msg}</div>", unsafe_allow_html=True)

    elif role == "bot":

        st.markdown("<div class='chat-bot'>🤖 Here's your career plan:</div>", unsafe_allow_html=True)

        # Skills
        st.markdown("### 📊 Skills")
        cols = st.columns(3)
        for i, skill in enumerate(msg.get("skills", [])):
            cols[i % 3].markdown(f"<div class='card'>{skill}</div>", unsafe_allow_html=True)

        # Missing
        st.markdown("### ❌ Missing Skills")
        for skill in msg.get("missing_skills", []):
            st.markdown(f"<div class='card'>{skill}</div>", unsafe_allow_html=True)

        # Graph
        # st.markdown("### 📊 Skill Gap Analysis")
        # df = pd.DataFrame({
        #     "Category": ["Skills", "Missing Skills"],
        #     "Count": [len(msg.get("skills", [])), len(msg.get("missing_skills", []))]
        # })
        # fig, ax = plt.subplots()
        # ax.bar(df["Category"], df["Count"])
        # st.pyplot(fig)

        # Roadmap
        st.markdown("### 🛣️ Roadmap")
        roadmap = msg.get("roadmap", {})
        col1, col2, col3 = st.columns(3)

        with col1:
            for item in roadmap.get("0-1_month", []):
                st.write("•", item)

        with col2:
            for item in roadmap.get("1-3_months", []):
                st.write("•", item)

        with col3:
            for item in roadmap.get("3-6_months", []):
                st.write("•", item)

        # Resources
        st.markdown("### 🎓 Resources")
        resources = msg.get("resources", {})

        # Courses
        for c in resources.get("courses", []):
            st.markdown(f"🔗 [{c.get('title')}]({c.get('link')})")

        # YouTube
        st.markdown("#### 🎥 Videos")
        all_videos = []

        for video in resources.get("youtube", []):
            if "SEARCH:" in video.get("link", ""):
                query = video["link"].replace("SEARCH:", "") + " full course"
                all_videos.extend(search_youtube(query))

        display_videos = all_videos[:6]
        cols = st.columns(3)

        for i, vid in enumerate(display_videos):
            with cols[i % 3]:
                st.image(vid["thumbnail"])
                st.markdown(f"[▶️ {vid['title']}]({vid['link']})")

        # Practice
        st.markdown("#### 💻 Practice")
        for p in resources.get("practice", []):
            if isinstance(p, dict):
                st.markdown(f"🔗 [{p.get('title')}]({p.get('link')})")
            else:
                st.write("•", p)

# ------------------ FLOATING CHAT BUTTON ------------------ #
if st.button("💬", key="chat_toggle"):
    st.session_state.chat_open = not st.session_state.chat_open

# ------------------ CHAT POPUP ------------------ #
if st.session_state.chat_open:

    st.markdown("## 💬 AI Assistant")

    user_question = st.text_input("Ask your question...", key="chat_input")

    if st.button("Send", key="chat_send"):

        if user_question:

            context = ""
            if "messages" in st.session_state:
                for role, m in reversed(st.session_state.messages):
                    if role == "bot":
                        context = json.dumps(m)
                        break

            answer = chat_with_ai(user_question, context)

            st.session_state.chat_history.append(("user", user_question))
            st.session_state.chat_history.append(("bot", answer))

    # Show chat
    for role, text in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"<div class='chat-user'>🧑 {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'>🤖 {text}</div>", unsafe_allow_html=True)