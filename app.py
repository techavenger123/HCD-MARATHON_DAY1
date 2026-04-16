import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import time


# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MQ6 Gas Monitor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-stale="true"], [data-stale="true"] * { opacity: 1 !important; transition: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
.element-container, .stMarkdown, .stMetric, .block-container { animation: none !important; transition: opacity 0s !important; }
html, body, [class*="css"] { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background-color: #0d0f14; color: #e8eaf0; }
.stApp { background-color: #0d0f14; }
section[data-testid="stSidebar"] { background: #13161e; border-right: 1px solid #1f2333; }
section[data-testid="stSidebar"] * { color: #c8cad8 !important; }
.stButton > button { background: linear-gradient(135deg, #e84545, #c62828); color: #fff; border: none; border-radius: 8px; font-family: 'Courier New','Consolas',monospace; font-size: 0.82rem; letter-spacing: 0.06em; padding: 0.55rem 1.4rem; transition: all 0.2s ease; box-shadow: 0 4px 18px rgba(232,69,69,0.3); }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(232,69,69,0.45); }
input[type="text"], input[type="password"] { background: #1a1e2a !important; border: 1px solid #2a2f42 !important; border-radius: 6px !important; color: #e8eaf0 !important; font-family: 'Courier New','Consolas',monospace !important; }
h1 { font-size: 1.9rem !important; font-weight: 800 !important; letter-spacing: -0.02em; }
h2 { font-size: 1.35rem !important; font-weight: 600 !important; color: #a0a5be !important; border-bottom: 1px solid #1f2333; padding-bottom: 0.4rem; }
h3 { font-size: 1.1rem !important; font-weight: 600 !important; }
[data-testid="stMetric"] { background: #13161e; border: 1px solid #1f2333; border-radius: 12px; padding: 1rem 1.2rem; }
[data-testid="stMetricLabel"] { color: #6b708a !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.1em; }
[data-testid="stMetricValue"] { color: #e8eaf0 !important; font-family: 'Courier New','Consolas',monospace !important; font-size: 2rem !important; }
.card { background: #13161e; border: 1px solid #1f2333; border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; }
.card-title { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em; color: #6b708a; margin-bottom: 0.3rem; }
.card-value { font-family: 'Courier New','Consolas',monospace; font-size: 1.5rem; font-weight: 700; }
.card-divider { height: 1px; background-color: #1f2333; margin: 0.65rem 0; }
.badge { display: inline-block; padding: 0.25rem 0.85rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700; font-family: 'Courier New','Consolas',monospace; letter-spacing: 0.06em; text-transform: uppercase; }
.badge-open   { background: rgba(54,217,123,0.12);  color: #36d97b; border: 1px solid rgba(54,217,123,0.3); }
.badge-closed { background: rgba(232,69,69,0.12);   color: #e84545; border: 1px solid rgba(232,69,69,0.3); }
.badge-alert  { background: rgba(255,165,0,0.12);   color: #ffb347; border: 1px solid rgba(255,165,0,0.3); }
.badge-auth   { background: rgba(54,217,123,0.12);  color: #36d97b; border: 1px solid rgba(54,217,123,0.3); }
.badge-unauth { background: rgba(232,69,69,0.12);   color: #e84545; border: 1px solid rgba(232,69,69,0.3); }
.badge-fp-id  { background: rgba(120,120,255,0.12); color: #9b9bff; border: 1px solid rgba(120,120,255,0.3); }
.badge-owner  { background: rgba(255,200,50,0.12);  color: #ffd966; border: 1px solid rgba(255,200,50,0.3); }
.badge-na     { background: rgba(100,100,100,0.15); color: #6b708a; border: 1px solid #2a2f42; }
.alert-banner  { background: rgba(232,69,69,0.1);   border: 1px solid rgba(232,69,69,0.4);  border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 1rem; font-family: 'Courier New','Consolas',monospace; font-size: 0.85rem; color: #e84545; letter-spacing: 0.04em; }
.safe-banner   { background: rgba(54,217,123,0.08); border: 1px solid rgba(54,217,123,0.3); border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 1rem; font-family: 'Courier New','Consolas',monospace; font-size: 0.85rem; color: #36d97b; letter-spacing: 0.04em; }
.auth-banner   { background: rgba(120,120,255,0.08); border: 1px solid rgba(120,120,255,0.3); border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 1rem; font-family: 'Courier New','Consolas',monospace; font-size: 0.85rem; color: #9b9bff; letter-spacing: 0.04em; }
.unauth-banner { background: rgba(232,69,69,0.08);  border: 1px solid rgba(232,69,69,0.3);  border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 1rem; font-family: 'Courier New','Consolas',monospace; font-size: 0.85rem; color: #e84545; letter-spacing: 0.04em; }
.device-id { font-family: 'Courier New','Consolas',monospace; font-size: 1rem; font-weight: 700; color: #e8eaf0; }
.stSelectbox > div > div { background: #1a1e2a !important; border: 1px solid #2a2f42 !important; color: #e8eaf0 !important; }
[data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=1000, key="datarefresh")

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://mq6-monitor-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

admin_ref = db.reference("users/admin")
if admin_ref.get() is None:
    admin_ref.set({"email": "admin@gmail.com", "devices": {}})

for key, val in [("logged_in", False), ("user_id", None), ("history", {})]:
    if key not in st.session_state:
        st.session_state[key] = val

GAS_THRESHOLD = 400

st.markdown("# 🔥 MQ6 Gas Monitoring System")
st.markdown(
    "<div style='color:#6b708a;font-size:0.82rem;margin-top:-0.6rem;margin-bottom:1.4rem;"
    "font-family:Courier New,Consolas,monospace;'>Real-time LPG / Gas Leak Detection &amp; Valve Control</div>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.sidebar.markdown("## 🔐 Login")
    email   = st.sidebar.text_input("Email")
    user_id = st.sidebar.text_input("User ID")
    if st.sidebar.button("Login"):
        user_ref  = db.reference("users/" + user_id)
        user_data = user_ref.get()
        if user_data and user_data.get("email") == email:
            st.session_state.logged_in = True
            st.session_state.user_id   = user_id
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")
    st.sidebar.markdown("---")
    st.markdown(
        "<div style='margin-top:6rem;text-align:center;color:#3a3f56;"
        "font-family:Courier New,Consolas,monospace;font-size:0.78rem;'>Please login from the sidebar →</div>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# LOGGED IN
# ══════════════════════════════════════════════════════════════════════════════
else:
    user_id = st.session_state.user_id

    st.sidebar.markdown(f"### 👤 {user_id}")
    st.sidebar.markdown("<span class='badge badge-open'>● ONLINE</span>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id   = None
        st.rerun()

    user_data = db.reference("users/" + user_id).get()

    # ══════════════════════════════════════════════════════════════════════════
    # ADMIN
    # ══════════════════════════════════════════════════════════════════════════
    if user_id == "admin":
        st.markdown("## 🛡️ Admin Dashboard")

        users   = db.reference("users").get()   or {}
        devices = db.reference("devices").get() or {}

        device_owners = {}
        for uid, udata in users.items():
            if isinstance(udata, dict):
                for dev_id in udata.get("devices", {}).keys():
                    device_owners[dev_id] = uid

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("### Registered Users")
            for uid, udata in users.items():
                st.markdown(
                    f"<div class='card'><div class='card-title'>User ID</div>"
                    f"<div class='device-id'>{uid}</div>"
                    f"<div style='color:#6b708a;font-size:0.78rem;font-family:Courier New,Consolas,monospace;margin-top:0.3rem'>"
                    f"{udata.get('email','—')}</div></div>",
                    unsafe_allow_html=True
                )
        with col2:
            st.markdown("### Register New User")
            new_uid   = st.text_input("New User ID",  key="new_uid")
            new_email = st.text_input("User Email",   key="new_email")
            if st.button("➕ Create User"):
                ref = db.reference("users/" + new_uid)
                if ref.get() is None:
                    ref.set({"email": new_email, "devices": {}})
                    st.success(f"User **{new_uid}** created")
                else:
                    st.error("User already exists")

        st.markdown("---")
        st.markdown("### Assign Device to User")
        if users and devices:
            ca, cb, cc = st.columns([1, 1, 0.6])
            with ca: sel_user   = st.selectbox("Select User",   list(users.keys()))
            with cb: sel_device = st.selectbox("Select Device", list(devices.keys()))
            with cc:
                st.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
                if st.button("Assign →"):
                    db.reference(f"users/{sel_user}/devices/{sel_device}").set(True)
                    st.success("Device assigned")
        else:
            st.warning("No users or devices available yet")

        st.markdown("---")
        st.markdown("### Live Device Overview")

        if devices:
            device_list = list(devices.items())
            # ── KEY FIX: fresh st.columns() per row — no col context reuse ──
            for row_start in range(0, len(device_list), 3):
                row_slice = device_list[row_start : row_start + 3]
                cols = st.columns(len(row_slice))

                for col_idx, (dev_id, dev_data) in enumerate(row_slice):
                    mq6        = dev_data.get("mq6", 0)            if isinstance(dev_data, dict) else 0
                    valve      = dev_data.get("valve", True)        if isinstance(dev_data, dict) else True
                    auto_c     = dev_data.get("auto_closed", False) if isinstance(dev_data, dict) else False
                    authorized = dev_data.get("authorized", None)   if isinstance(dev_data, dict) else None
                    finger_id  = dev_data.get("finger_id", -1)      if isinstance(dev_data, dict) else -1
                    is_danger  = mq6 >= GAS_THRESHOLD
                    owner      = device_owners.get(dev_id)

                    border_color = "rgba(232,69,69,0.5)" if is_danger else "#1f2333"
                    gas_color    = "#e84545" if is_danger else "#36d97b"
                    valve_cls    = "badge-closed" if not valve else "badge-open"
                    valve_label  = "CLOSED" if not valve else "OPEN"
                    valve_icon   = "🔴" if not valve else "🟢"

                    auto_badge_html = (
                        "<div style='margin-top:0.35rem'><span class='badge badge-alert'>AUTO CLOSED</span></div>"
                        if auto_c else ""
                    )

                    if authorized is True:
                        auth_html = "<span class='badge badge-auth'>✅ AUTHORIZED</span>"
                    elif authorized is False:
                        auth_html = "<span class='badge badge-unauth'>🚫 UNAUTHORIZED</span>"
                    else:
                        auth_html = "<span class='badge badge-na'>— N/A</span>"

                    fp_html = (
                        f"<span class='badge badge-fp-id'>🖐️ ID #{finger_id}</span>"
                        if finger_id >= 0 else "<span class='badge badge-na'>No scan</span>"
                    )

                    owner_html = (
                        f"<span class='badge badge-owner'>👤 {owner}</span>"
                        if owner else "<span class='badge badge-na'>— Unassigned</span>"
                    )

                    # ── card_divider div replaces every <hr> ─────────────────
                    card_html = (
                        f"<div class='card' style='border-color:{border_color}'>"
                        f"<div style='display:flex;justify-content:space-between;align-items:flex-start'>"
                        f"<div><div class='card-title'>Device ID</div><div class='device-id'>{dev_id}</div></div>"
                        f"<div style='text-align:right'><div class='card-title'>Owner</div>{owner_html}</div>"
                        f"</div>"
                        f"<div class='card-divider'></div>"
                        f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                        f"<div><div class='card-title'>Gas Level</div>"
                        f"<div class='card-value' style='color:{gas_color}'>{mq6}</div></div>"
                        f"<div style='text-align:right'><div class='card-title'>Valve</div>"
                        f"<span class='badge {valve_cls}'>{valve_icon} {valve_label}</span>{auto_badge_html}</div>"
                        f"</div>"
                        f"<div class='card-divider'></div>"
                        f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                        f"<div><div class='card-title'>Auth Status</div>{auth_html}</div>"
                        f"<div style='text-align:right'><div class='card-title'>Last Fingerprint</div>{fp_html}</div>"
                        f"</div>"
                        f"</div>"
                    )

                    with cols[col_idx]:
                        st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("No devices registered yet.")

    # ══════════════════════════════════════════════════════════════════════════
    # USER
    # ══════════════════════════════════════════════════════════════════════════
    else:
        st.markdown("## 📡 My Devices")
        devices = user_data.get("devices", {})

        if not devices:
            st.warning("No devices assigned. Contact your administrator.")
        else:
            for device in devices:
                dev_data    = db.reference("devices/" + device).get() or {}
                mq6_value   = dev_data.get("mq6", 0)
                valve_open  = dev_data.get("valve", True)
                auto_closed = dev_data.get("auto_closed", False)
                authorized  = dev_data.get("authorized", None)
                finger_id   = dev_data.get("finger_id", -1)
                is_danger   = mq6_value >= GAS_THRESHOLD

                if is_danger:
                    st.markdown(
                        f"<div class='alert-banner'>⚠️ &nbsp; GAS LEAK DETECTED on <strong>{device}</strong>"
                        " — Valve auto-closed. Use registered fingerprint to re-open after ventilation.</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='safe-banner'>✅ &nbsp; Air quality is normal on <strong>{device}</strong></div>",
                        unsafe_allow_html=True
                    )

                if authorized is True:
                    fp_label = f"ID #{finger_id}" if finger_id >= 0 else "unknown"
                    st.markdown(
                        f"<div class='auth-banner'>🖐️ &nbsp; Fingerprint <strong>{fp_label}</strong>"
                        f" recognized — Access <strong>AUTHORIZED</strong> on <strong>{device}</strong></div>",
                        unsafe_allow_html=True
                    )
                elif authorized is False:
                    st.markdown(
                        f"<div class='unauth-banner'>🚫 &nbsp; Unrecognized fingerprint on"
                        f" <strong>{device}</strong> — Access <strong>DENIED</strong></div>",
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem'>"
                    f"<span class='device-id' style='font-size:1.1rem'>📟 {device}</span>"
                    f"<span class='badge badge-owner'>👤 {user_id}</span></div>",
                    unsafe_allow_html=True
                )

                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.metric("🌡️ Gas Level (ADC)", mq6_value, help=f"Raw ADC (0–1023). Threshold: {GAS_THRESHOLD}")
                with c2:
                    pct = min(int(mq6_value / 1023 * 100), 100)
                    st.metric("📊 Concentration %", f"{pct}%")
                with c3:
                    st.metric("🚰 Valve Status", "🟢 OPEN" if valve_open else "🔴 CLOSED")
                with c4:
                    fp_status = "🔒 Auto-Closed" if auto_closed else ("🔓 Manual" if not valve_open else "✅ Normal")
                    st.metric("🖐️ Fingerprint Lock", fp_status)
                with c5:
                    auth_display = "✅ Authorized" if authorized is True else ("🚫 Denied" if authorized is False else "— N/A")
                    st.metric("🔐 Auth Status", auth_display)

                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

                with st.expander(f"📋 Device Details — {device}", expanded=True):
                    d1, d2 = st.columns([2, 1])

                    with d1:
                        if device not in st.session_state.history:
                            st.session_state.history[device] = []
                        st.session_state.history[device].append(mq6_value)
                        if len(st.session_state.history[device]) > 60:
                            st.session_state.history[device].pop(0)
                        df = pd.DataFrame(st.session_state.history[device], columns=["Gas Level (ADC)"])
                        df["Threshold"] = GAS_THRESHOLD
                        st.markdown("**Gas Level History**")
                        st.line_chart(df, height=220)

                    with d2:
                        st.markdown("**Valve &amp; Fingerprint Control**")

                        valve_badge = "badge-open" if valve_open else "badge-closed"
                        valve_text  = "OPEN" if valve_open else "CLOSED"

                        if authorized is True:
                            auth_cls = "badge-auth"; auth_txt = "✅ AUTHORIZED"
                        elif authorized is False:
                            auth_cls = "badge-unauth"; auth_txt = "🚫 UNAUTHORIZED"
                        else:
                            auth_cls = "badge-na"; auth_txt = "— N/A"

                        fp_id_html = (
                            f"<span class='badge badge-fp-id'>🖐️ ID #{finger_id}</span>"
                            if finger_id >= 0
                            else "<span style='color:#6b708a;font-size:0.82rem'>No recent scan</span>"
                        )

                        auto_warn_html = (
                            "<div style='color:#ffb347;font-size:0.82rem;margin-top:0.5rem'>"
                            "⚠️ Auto-closed due to gas. Will unlock after gas clears.</div>"
                            if auto_closed else ""
                        )

                        # ── all detail cards use card-divider, zero <hr> tags ──
                        st.markdown(
                            f"<div class='card' style='margin-bottom:0.7rem'>"
                            f"<div class='card-title'>Owner / User</div>"
                            f"<span class='badge badge-owner'>👤 {user_id}</span></div>"

                            f"<div class='card' style='margin-bottom:0.7rem'>"
                            f"<div class='card-title'>Current Valve State</div>"
                            f"<span class='badge {valve_badge}'>{'🟢' if valve_open else '🔴'} {valve_text}</span></div>"

                            f"<div class='card' style='margin-bottom:0.7rem'>"
                            f"<div class='card-title'>Authorization Status</div>"
                            f"<span class='badge {auth_cls}'>{auth_txt}</span>"
                            f"<div style='margin-top:0.5rem'><div class='card-title'>Last Fingerprint ID</div>"
                            f"{fp_id_html}</div></div>"

                            f"<div class='card' style='margin-bottom:0.7rem'>"
                            f"<div class='card-title'>Fingerprint Control</div>"
                            f"<div style='font-size:0.82rem;color:#a0a5be;line-height:1.6'>"
                            f"Valve is toggled by an enrolled fingerprint on the device sensor."
                            f"{auto_warn_html}</div></div>"

                            f"<div class='card'>"
                            f"<div class='card-title'>LED Indicators</div>"
                            f"<div style='font-size:0.82rem;color:#a0a5be;line-height:1.8'>"
                            f"🟢 GREEN → Valve Open<br>🔴 RED &nbsp;&nbsp;→ Valve Closed</div></div>",
                            unsafe_allow_html=True
                        )

                st.markdown("---")