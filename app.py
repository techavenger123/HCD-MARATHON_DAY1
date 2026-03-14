import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import time

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=500, key="datarefresh")

# ---------- FIREBASE CONNECTION ----------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://mq6-monitor-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# ---------- CREATE ADMIN ----------
admin_ref = db.reference("users/admin")
if admin_ref.get() is None:
    admin_ref.set({
        "email": "admin@gmail.com",
        "devices": {}
    })

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# store graph history
if "history" not in st.session_state:
    st.session_state.history = {}

# ---------- TITLE ----------
st.title("MQ6 Gas Monitoring System")

# ---------- LOGIN ----------
if not st.session_state.logged_in:

    st.sidebar.header("Login")

    email = st.sidebar.text_input("Email")
    user_id = st.sidebar.text_input("User ID")

    if st.sidebar.button("Login"):

        user_ref = db.reference("users/" + user_id)
        user_data = user_ref.get()

        if user_data and user_data["email"] == email:

            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.rerun()

        else:
            st.sidebar.error("Invalid Login")

# ---------- LOGGED IN ----------
else:

    user_id = st.session_state.user_id
    st.sidebar.success(f"Logged in as {user_id}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.rerun()

    user_data = db.reference("users/" + user_id).get()

    # =================================================
    # ADMIN DASHBOARD
    # =================================================
    if user_id == "admin":

        st.header("Admin Dashboard")

        users = db.reference("users").get()
        devices = db.reference("devices").get()

        st.subheader("Registered Users")
        for uid in users:
            st.write(uid, users[uid]["email"])

        st.subheader("Register New User")

        new_user_id = st.text_input("New User ID")
        new_user_email = st.text_input("User Email")

        if st.button("Create User"):

            new_user_ref = db.reference("users/" + new_user_id)

            if new_user_ref.get() is None:
                new_user_ref.set({
                    "email": new_user_email,
                    "devices": {}
                })
                st.success("User created successfully")
            else:
                st.error("User already exists")

        st.subheader("Assign Device")

        if users and devices:

            selected_user = st.selectbox("Select User", list(users.keys()))
            selected_device = st.selectbox("Select Device", list(devices.keys()))

            if st.button("Assign Device"):

                ref = db.reference(f"users/{selected_user}/devices/{selected_device}")
                ref.set(True)

                st.success("Device Assigned")

    # =================================================
    # USER DASHBOARD
    # =================================================
    else:

        st.header("My Devices")

        devices = user_data.get("devices", {})

        if not devices:
            st.warning("No devices assigned")

        else:

            for device in devices:

                device_data = db.reference("devices/" + device).get()

                mq6_value = device_data.get("mq6", 0)

                st.subheader(f"Device: {device}")
                st.metric("MQ6 Gas Level", mq6_value)

                # ---------- STORE HISTORY ----------
                if device not in st.session_state.history:
                    st.session_state.history[device] = []

                st.session_state.history[device].append(mq6_value)

                # limit history
                if len(st.session_state.history[device]) > 30:
                    st.session_state.history[device].pop(0)

                df = pd.DataFrame(st.session_state.history[device], columns=["MQ6"])

                st.line_chart(df)