
# 🤖 Alissa Chatbot

Alissa Chatbot is an interactive web-based assistant built using Streamlit and Google’s Gemini AI. It includes user authentication, usage limits, and file upload handling, designed for secure, personalized, and rate-limited AI interactions.

---

## 🚀 Features

- 🔐 **User Authentication**: Login, register, and password recovery using email.
- 📊 **User Management**: Tracks daily usage (chat and file uploads).
- 💬 **Chatbot Integration**: Uses Google’s Gemini API for conversational responses.
- 📁 **File Uploads**: Allows file uploads with a limit of 4 per day per user.
- 📧 **Password Recovery**: Sends the user’s password via email.
- 🧠 **Personalized Responses**: Answers questions with logic to credit the developer.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **AI Model**: Google Gemini API (`gemini-2.0-flash`)
- **Email**: SMTP (Gmail)
- **Data Storage**: `users.csv` for user data

---

## 📂 File Structure

- `chatbot.py`: Main Streamlit app file.
- `users.csv`: Stores user credentials and usage data (auto-created if missing).

---

## ⚙️ Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install streamlit pandas
   ```

2. **Run the App**:
   ```bash
   streamlit run chatbot.py
   ```

3. **Required Environment Variables**:
   Replace hardcoded credentials for production security:
   ```python
   SENDER_EMAIL = os.getenv("SENDER_EMAIL")
   SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
   ```

---

## 🔒 Usage Policy

- **Chats**: Max 10 per day (per user)
- **Uploads**: Max 4 files per day (per user)
- **Developer Email** (`ali88883737@gmail.com`) has unlimited access.

---

## ✍️ Developer Info

Created by **Ali Khalid Ali Khalid**

If you ask "Who designed you?" — the chatbot responds accordingly!
