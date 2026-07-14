import streamlit as st
import plotly.graph_objects as go
import requests
import time
import random

st.set_page_config(page_title="Room Dashboard", page_icon="📊", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #E5E7EB;
        text-align: center;
        border-left: 6px solid #3B82F6;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .metric-card:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
    }
    .status-on {
        color: #EF4444; /* Red for Alert/On */
    }
    .status-off {
        color: #10B981; /* Green for Normal/Off */
    }
</style>
""", unsafe_allow_html=True)

# กำหนด URL ของ Realtime Database (ตอนนี้ใช้ข้อมูลจำลองแทน)
url = 'https://roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app/data.json'

# ฟังก์ชันสำหรับดึงข้อมูล (ใช้ข้อมูลจำลองแทนการดึงจาก Firebase)
def fetch_data(target_url):
    # จำลองค่าแสง (สมมติ 0-100) และค่าเสียง (สมมติ 0-1023)
    mock_light = random.randint(20, 100)
    mock_sound = random.randint(200, 700)
    return mock_light, mock_sound

# ใช้ session_state เพื่อป้องกันไม่ให้ส่งข้อความ LINE แจ้งเตือนรัวๆ ทุกครั้งที่หน้ารีเฟรช
if 'line_notified' not in st.session_state:
    st.session_state.line_notified = False

st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.page_link("main.py", label="Home", icon="🏠")
st.sidebar.markdown("---")

Room = ["2-304", "2-305", "2-306", "2-307", "2-308", "2-310", "2-311", "2-312"]
st.sidebar.markdown("### 🚪 Room Selection")
selected_tab = st.sidebar.selectbox("Select Room", Room, label_visibility="collapsed")
st.sidebar.markdown("---")

if selected_tab == "2-304":
    st.title(f"📊 Dashboard - Room {selected_tab}")
    st.markdown("ระบบมอนิเตอร์สถานะแสงสว่างและระดับเสียงแบบเรียลไทม์")
    st.write("---")
    
    # รับข้อมูลจาก Firebase
    light_value, sound_value = fetch_data(url)
    
    if light_value is not None and sound_value is not None:
        
        # สมมติฐาน: หากค่าแสง <= 50 คือมืด(อาจจะหมายถึงมีคนเปิดไฟ หรือค่าเซนเซอร์ตามสภาพจริง)
        # ปรับค่าลอจิกตามที่ฮาร์ดแวร์วัดได้จริง
        is_light_on = (light_value <= 50)
        is_noisy = (sound_value >= 490) # ค่าเสียงดัง
        
        # จัดการแสดงไอคอนสถานะห้อง
        st.sidebar.markdown("### 📡 Live Status")
        status_emoji = f"**{selected_tab}** : "
        if is_light_on: status_emoji += "💡 เปิดไฟ "
        if is_noisy: status_emoji += "🗣️ มีเสียงดัง "
        if not is_light_on and not is_noisy: status_emoji += "✅ ปกติ"
        st.sidebar.info(status_emoji)
        
        # การแจ้งเตือน (จำลองการแจ้งเตือนบนหน้าจอแทน LINE Bot)
        if is_light_on:
            if not st.session_state.line_notified:
                st.toast(f'🚨 แจ้งเตือน: ไฟห้อง {selected_tab} เปิดอยู่!')
                st.session_state.line_notified = True # จำไว้ว่าแจ้งเตือนไปแล้ว
        else:
            st.session_state.line_notified = False # รีเซ็ตสถานะเมื่อไฟปิด

        # ห้องอื่นๆ เป็นค่าจำลองชั่วคราว
        st.sidebar.write("2-306 : 🗣️💡")
        st.sidebar.write("2-305 : 🗣️")
        st.sidebar.write("2-307 : 💡")
        
        # --- UI LAYOUT ---
        col1, col2, col3 = st.columns([1, 1, 1.5])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {'#EF4444' if is_light_on else '#10B981'};">
                <div class="metric-title">💡 สถานะหลอดไฟ</div>
                <div class="metric-value {'status-on' if is_light_on else 'status-off'}">
                    {'สว่าง/เปิดใช้งาน' if is_light_on else 'ปกติ (ปิด)'}
                </div>
                <div style="margin-top: 10px; color: #6B7280; font-size: 0.9rem;">
                    ค่าเซนเซอร์: <b>{light_value}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {'#EF4444' if is_noisy else '#10B981'};">
                <div class="metric-title">🔊 ระดับเสียง</div>
                <div class="metric-value {'status-on' if is_noisy else 'status-off'}">
                    {'เสียงดัง' if is_noisy else 'ปกติ'}
                </div>
                <div style="margin-top: 10px; color: #6B7280; font-size: 0.9rem;">
                    ค่าเซนเซอร์: <b>{sound_value}</b> / 1023
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # สร้างกราฟมาตรวัดระดับเสียง (Gauge Chart) ด้วย Plotly
            fig = go.Figure()
            fig.add_trace(go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=sound_value,  # ใช้ค่าเสียงจากเซนเซอร์จริงๆ
                mode="gauge+number+delta",
                title={'text': "ระดับเสียง (Sound Level)", 'font': {'size': 20, 'color': '#374151'}},
                delta={'reference': 490, 'increasing': {'color': "#EF4444"}, 'decreasing': {'color': "#10B981"}},
                gauge={'axis': {'range': [None, 1023], 'tickwidth': 1, 'tickcolor': "darkblue"},
                       'bar': {'color': "#3B82F6"},
                       'bgcolor': "white",
                       'borderwidth': 2,
                       'bordercolor': "#E5E7EB",
                       'steps': [
                           {'range': [0, 250], 'color': "#D1FAE5"}, # Light green
                           {'range': [250, 490], 'color': "#FEF3C7"}, # Light yellow
                           {'range': [490, 1023], 'color': "#FEE2E2"}  # Light red
                       ],
                       'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

            fig.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#374151"})
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("⏳ กำลังรอข้อมูลจาก Firebase...")

    # หน่วงเวลา 5 วินาที แล้วรีเฟรชหน้าต่างอัตโนมัติ
    time.sleep(5)
    st.rerun() # อัปเดตคำสั่งใหม่ แทนที่ st.experimental_rerun()