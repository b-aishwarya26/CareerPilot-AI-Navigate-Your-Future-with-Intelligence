# 🚀 CareerPilot AI – Navigate Your Future with Intelligence

**CareerPilot AI** is an intelligent multi-agent system that analyzes your resume, identifies skill gaps, and generates a personalized career roadmap with curated learning resources.

Built using **CrewAI + Groq + Streamlit**, this project simulates real-world collaboration between AI agents such as career coaches, market analysts, and learning advisors.

---

## 🌟 Features

* 📄 Resume Analysis (PDF Upload)
* 🧠 Skill Gap Identification
* 🔥 Trending Skills Detection
* 🛣️ Personalized Career Roadmap (0–6 months)
* 🎥 YouTube Resource Recommendations (with thumbnails)
* 📘 Course Suggestions (with links)
* 💻 Practice Platform Recommendations
* 📊 Skill Gap Visualization (graph)
* 📥 Downloadable Career Plan (JSON)

---

## 🧠 How It Works (Agentic AI)

The system uses multiple AI agents powered by CrewAI:

1. **Profile Analyzer Agent**

   * Extracts skills and identifies gaps from resume

2. **Market Research Agent**

   * Finds trending skills based on industry demand

3. **Roadmap Planner Agent**

   * Creates structured learning roadmap

4. **Resource Finder Agent**

   * Suggests courses, YouTube videos, and practice platforms

All agents collaborate using **context sharing**, making the system truly *agentic*.

---

## 🏗️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Framework:** CrewAI
* **LLM:** Groq (LLaMA 3)
* **APIs Used:**

  * YouTube Data API v3
* **Libraries:**

  * pandas
  * matplotlib
  * PyPDF2
  * requests

---

## 📂 Project Structure

```
careerpilot-ai/
│
├── app.py                # Streamlit UI
├── crew.py              # Agents & tasks
├── tools.py             # API integrations (YouTube)
├── resume_parser.py     # Resume text extraction
├── requirements.txt
├── .env                 # API keys (not uploaded)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/careerpilot-ai.git
cd careerpilot-ai
```

---

### 2️⃣ Create Virtual Environment (optional)

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` File (IMPORTANT ⚠️)

Create a file named `.env` in the root folder and add your API keys:

```
GROQ_API_KEY=your_groq_api_key
YOUTUBE_API_KEY=your_youtube_api_key
```

👉 **Do NOT upload this file to GitHub**
(Add `.env` to `.gitignore`)

---

### 5️⃣ Run the App

```
streamlit run app.py
```

---

## 🔐 API Setup

### 🔹 Groq API

* Get key from: https://console.groq.com

### 🔹 YouTube API

* Enable **YouTube Data API v3** from Google Cloud Console

---

## 🚀 Future Improvements

* 🎤 Voice input (speech-to-text)
* 📊 Interactive graphs (Plotly)
* 💬 Chat-based continuous conversation
* 🌐 Deployment with custom domain
* 📄 PDF report generation
* 🔗 LinkedIn / GitHub profile analysis

---

## ⚠️ Disclaimer

This tool provides AI-generated career guidance and should be used for informational purposes only.

---

## 👩‍💻 Author

**B Aishwarya**
AI & ML Enthusiast | Future AI Product Manager

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share it!

---
