import streamlit as st
import pandas as pd
import datetime
import smtplib
import re
from email.mime.text import MIMEText
from google import genai

st.set_page_config(page_title="Coding chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Alissa Chatbot")

SENDER_EMAIL = "ali88883737@gmail.com"
SENDER_PASSWORD = "awch igef pnta xkyv"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

client = genai.Client(api_key="AIzaSyAmWf4qrM_1X0SlwuOJrsV0W9bi1rgVkZA")

USER_CSV = "users.csv"
DEVELOPER_EMAIL = "ali88883737@gmail.com"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "rerun_flag" not in st.session_state:
    st.session_state.rerun_flag = False  
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def rerun():
    st.session_state.rerun_flag = not st.session_state.rerun_flag
    st.experimental_set_query_params(rerun=str(datetime.datetime.now()))

def load_users():
    try:
        return pd.read_csv(USER_CSV)
    except:
        return pd.DataFrame(columns=["email", "password", "usage_date", "chat_count", "upload_count"])

def save_users(df):
    df.to_csv(USER_CSV, index=False)

def send_email(recipient, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def login(email, password):
    df = load_users()
    user = df[(df.email == email) & (df.password == password)]
    if not user.empty:
        st.session_state.logged_in = True
        st.session_state.email = email
        return True
    return False

def register(email, password):
    df = load_users()
    if email == DEVELOPER_EMAIL:
        return False
    if email in df.email.values:
        return False
    if not is_strong_password(password):
        return False
    new_row = {
        "email": email,
        "password": password,
        "usage_date": str(datetime.date.today()),
        "chat_count": 0,
        "upload_count": 0
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_users(df)
    return True

def update_usage(email, is_upload=False):
    df = load_users()
    today = str(datetime.date.today())
    user_index = df[df.email == email].index
    if not user_index.empty:
        idx = user_index[0]
        if df.at[idx, "usage_date"] != today:
            df.at[idx, "usage_date"] = today
            df.at[idx, "chat_count"] = 0
            df.at[idx, "upload_count"] = 0
        if is_upload:
            df.at[idx, "upload_count"] += 1
        else:
            df.at[idx, "chat_count"] += 1
        save_users(df)
        return df.at[idx, "chat_count"], df.at[idx, "upload_count"]
    return 0, 0

def can_use(email, is_upload=False):
    if email == DEVELOPER_EMAIL:
        return True
    df = load_users()
    today = str(datetime.date.today())
    user = df[df.email == email]
    if user.empty:
        return False
    user = user.iloc[0]
    if user.usage_date != today:
        return True
    if is_upload:
        return user.upload_count < 4
    return user.chat_count < 10

def main():
    if not st.session_state.logged_in:
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

        with tab1:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if login(email, password):
                    st.session_state.chat_history = []  
                    rerun()
                else:
                    st.error("Invalid credentials")

        with tab2:
            new_email = st.text_input("New Email")
            new_password = st.text_input("New Password", type="password")
            if st.button("Register"):
                if register(new_email, new_password):
                    st.success("Registered successfully")
                else:
                    st.error("Weak password or user exists or not allowed")

        with tab3:
            reset_email = st.text_input("Enter your email to reset password")
            if st.button("Send Password"):
                df = load_users()
                user = df[df.email == reset_email]
                if not user.empty:
                    password = user.iloc[0]["password"]
                    message = f"Your password is: {password}"
                    try:
                        send_email(reset_email, "Your Password Recovery", message)
                        st.success("Password sent to your email.")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")
                else:
                    st.error("Email not found")

        return

    st.sidebar.success(f"Logged in as {st.session_state.email}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.chat_history = []
        rerun()

    chat_container = st.container()

    input_text = st.text_input("Ask Alissa something")

    if input_text:
        if not can_use(st.session_state.email):
            st.warning("Limit reached. Try again tomorrow.")
            return

        st.session_state.chat_history.append({"sender": "user", "message": input_text})

        with st.spinner("Alissa is thinking..."):
            if "مين صممك" in input_text or "من صممك" in input_text or "who designed you" in input_text.lower():
                bot_response = "Ali Khalid Ali Khalid"
            else:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=input_text
                )
                bot_response = response.text.strip()

            update_usage(st.session_state.email)

        # تحقق إذا الرد يحتوي على كود محاط بـ ``` 
        if bot_response.startswith("```") and bot_response.endswith("```"):
            code_only = bot_response.strip("```").strip()
            st.session_state.chat_history.append({"sender": "bot", "message": code_only, "is_code": True})
        else:
            st.session_state.chat_history.append({"sender": "bot", "message": bot_response, "is_code": False})

    with chat_container:
        for chat in st.session_state.chat_history:
            if chat["sender"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 8px 0;">
                    <div style="
                        background-color: #0078d7;
                        color: white;
                        padding: 12px 18px;
                        border-radius: 20px 20px 0 20px;
                        max-width: 70%;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        font-size: 15px;
                        word-wrap: break-word;">
                        {chat['message']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:  # bot
                if chat.get("is_code", False):
                    st.code(chat["message"], language="python")
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 8px 0;">
                        <div style="
                            background-color: #f1f0f0;
                            color: #333;
                            padding: 12px 18px;
                            border-radius: 20px 20px 20px 0;
                            max-width: 70%;
                            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            font-size: 15px;
                            word-wrap: break-word;">
                            {chat['message']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload a file (Max 4 per day)", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if not can_use(st.session_state.email, is_upload=True):
                st.warning("Upload limit reached.")
                break
            update_usage(st.session_state.email, is_upload=True)
            st.success(f"File {uploaded_file.name} uploaded")

if __name__ == "__main__":
    main()
#requirements.txt