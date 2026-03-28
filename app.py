import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from crew import run_crew
from resume_parser import extract_text_from_pdf
from tools import search_youtube

# ------------------ CONFIG ------------------ #
st.title("🚀 CareerPilot AI - Your AI Career Mentor")

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
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------ #
st.title("🚀 CareerPilot AI")
st.caption("Chat with your AI Career Mentor")

# ------------------ SESSION ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ INPUT ------------------ #
uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])
goal = st.text_input("🎯 Enter Career Goal")

if st.button("✨ Analyze"):

    if not uploaded_file or not goal:
        st.warning("Upload resume & enter goal")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)

    user_msg = f"I want to become a {goal}"
    st.session_state.messages.append(("user", user_msg))

    with st.spinner("🤖 Thinking..."):

        crew_output = run_crew(resume_text, goal)
        result = crew_output.raw
        result = result.strip().replace("```json", "").replace("```", "")

        try:
            data = json.loads(result)
        except:
            st.error("JSON parsing failed")
            st.write(result)
            st.stop()

    st.session_state.messages.append(("bot", data))

# ------------------ CHAT UI ------------------ #
for role, msg in st.session_state.messages:

    if role == "user":
        st.markdown(f"<div class='chat-user'>🧑 {msg}</div>", unsafe_allow_html=True)

    elif role == "bot":

        st.markdown("<div class='chat-bot'>🤖 Here's your career plan:</div>", unsafe_allow_html=True)

        # ------------------ SKILLS ------------------ #
        st.markdown("### 📊 Skills")
        cols = st.columns(3)
        for i, skill in enumerate(msg.get("skills", [])):
            cols[i % 3].markdown(f"<div class='card'>{skill}</div>", unsafe_allow_html=True)

        # ------------------ MISSING ------------------ #
        st.markdown("### ❌ Missing Skills")
        for skill in msg.get("missing_skills", []):
            st.markdown(f"<div class='card'>{skill}</div>", unsafe_allow_html=True)

        # ------------------ GRAPH ------------------ #
        st.markdown("### 📊 Skill Gap Analysis")

        df = pd.DataFrame({
            "Category": ["Skills", "Missing Skills"],
            "Count": [len(msg.get("skills", [])), len(msg.get("missing_skills", []))]
        })

        fig, ax = plt.subplots()
        ax.bar(df["Category"], df["Count"])
        ax.set_title("Skill Gap Overview")
        st.pyplot(fig)

        # ------------------ ROADMAP ------------------ #
        st.markdown("### 🛣️ Roadmap")

        roadmap = msg.get("roadmap", {})
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 📅 0–1 Month")
            for item in roadmap.get("0-1_month", []):
                st.write("•", item)

        with col2:
            st.markdown("#### 📅 1–3 Months")
            for item in roadmap.get("1-3_months", []):
                st.write("•", item)

        with col3:
            st.markdown("#### 📅 3–6 Months")
            for item in roadmap.get("3-6_months", []):
                st.write("•", item)

        # ------------------ RESOURCES ------------------ #
        st.markdown("### 🎓 Resources")

        resources = msg.get("resources", {})

        # ------------------ COURSES ------------------ #
        st.markdown("#### 📘 Courses")
        for c in resources.get("courses", []):
            st.markdown(f"🔗 [{c.get('title')}]({c.get('link')})")

        # ------------------ YOUTUBE ------------------ #
        st.markdown("#### 🎥 YouTube Videos")

        all_videos = []

        for video in resources.get("youtube", []):
            if "SEARCH:" in video.get("link", ""):
                query = video["link"].replace("SEARCH:", "") + " full course"
                yt_results = search_youtube(query)
                all_videos.extend(yt_results)

        # 🔥 LIMIT VIDEOS
        show_more = st.checkbox("🔍 Show more videos")

        if show_more:
            display_videos = all_videos
        else:
            display_videos = all_videos[:6]

        cols = st.columns(3)

        for i, vid in enumerate(display_videos):
            with cols[i % 3]:
                st.image(vid["thumbnail"])
                st.markdown(f"[▶️ {vid['title']}]({vid['link']})")

        # ------------------ PRACTICE ------------------ #
        st.markdown("#### 💻 Practice Platforms")

        for p in resources.get("practice", []):
            st.markdown(f"🔗 [{p.get('title','Platform')}]({p.get('link','#')})")

        # ------------------ DOWNLOAD ------------------ #
        st.download_button(
            "📥 Download Plan",
            data=json.dumps(msg, indent=4),
            file_name="career_plan.json"
        )