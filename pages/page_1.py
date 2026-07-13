import streamlit as st
import plotly.graph_objects as go
import requests
import time
from linebot import LineBotApi
from linebot.models import TextSendMessage

# กำหนด URL ของ Realtime Database
url = 'https://roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app/data.json'
# กำหนด Channel Access Token ของคุณที่นี่
line_bot_api = LineBotApi('34loTH/TdYPoz42K9XBFNxN6j95YP4FBP53bKysGSjF4LlECXthpHI5Wf4NDP2LdEsQX4rX2fBmriSX4VresVKIxPB2kTpNWLgbzouozjjh2pG5xy+5n5MuCRor5/+eNdCMNhjc/ceb7RdSG4Ns0GgdB04t89/1O/w1cDnyilFU=')

# ฟังก์ชันสำหรับดึงข้อมูล (ดึงเพียงครั้งเดียวต่อ 1 รอบรัน ไม่ใช้ while loop เพื่อลดภาระเว็บ)
def fetch_data(target_url):
    try:
        response = requests.get(target_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and 'Light' in data and 'Sound' in data:
                return data['Light'], data['Sound']
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการรับข้อมูล: {e}")
    return None, None

# ใช้ session_state เพื่อป้องกันไม่ให้ส่งข้อความ LINE แจ้งเตือนรัวๆ ทุกครั้งที่หน้ารีเฟรช
if 'line_notified' not in st.session_state:
    st.session_state.line_notified = False

Room = ["2-304", "2-305", "2-306", "2-307", "2-308", "2-310", "2-311", "2-312"]
st.sidebar.page_link("main.py", label="Home", icon="🏠")
selected_tab = st.sidebar.selectbox("Select Room", Room)

if selected_tab == "2-304":
    st.header("Room 2-304")
    
    # รับข้อมูลจาก Firebase
    light_value, sound_value = fetch_data(url)
    
    if light_value is not None and sound_value is not None:
        
        # สมมติฐาน: หากค่าแสง <= 50 คือมืด(อาจจะหมายถึงมีคนเปิดไฟ หรือค่าเซนเซอร์ตามสภาพจริง)
        # ปรับค่าลอจิกตามที่ฮาร์ดแวร์วัดได้จริง
        is_light_on = (light_value <= 50)
        is_noisy = (sound_value >= 490) # ค่าเสียงดัง
        
        # จัดการแสดงไอคอนสถานะห้อง
        status_emoji = "2-304 "
        if is_light_on: status_emoji += "💡"
        if is_noisy: status_emoji += "🗣️"
        st.sidebar.write(status_emoji)
        
        # การแจ้งเตือน LINE Bot (แจ้งเตือนเฉพาะตอนที่สถานะเปลี่ยนจากปิดเป็นเปิด)
        if is_light_on:
            if not st.session_state.line_notified:
                try:
                    line_bot_api.broadcast(TextSendMessage(text='🚨 แจ้งเตือน: ไฟห้อง 2-304 เปิดอยู่!'))
                    st.session_state.line_notified = True # จำไว้ว่าแจ้งเตือนไปแล้ว
                except Exception as e:
                    st.sidebar.error("LINE Notify Error")
        else:
            st.session_state.line_notified = False # รีเซ็ตสถานะเมื่อไฟปิด

        # ห้องอื่นๆ เป็นค่าจำลองชั่วคราว
        st.sidebar.write("2-306 🗣️💡")
        st.sidebar.write("2-305 🗣️")
        st.sidebar.write("2-307 💡")
        
        # สร้างกราฟมาตรวัดระดับเสียง (Gauge Chart) ด้วย Plotly
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=sound_value,  # ใช้ค่าเสียงจากเซนเซอร์จริงๆ
            mode="gauge+number+delta",
            title={'text': "ระดับเสียง (Sound Level)"},
            delta={'reference': 100},
            gauge={'axis': {'range': [None, 1023]}, # 1023 คือค่าสูงสุดสำหรับ Analog ESP8266/ESP32
                   'steps': [
                       {'range': [0, 250], 'color': "lightgray"},
                       {'range': [250, 490], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Room Status (สถานะดวงไฟ)")
        if light_value >= 70:
            st.write(" หลอดไฟ :🟢 (ปกติ)")
        else:
            st.write(" หลอดไฟ :🔴 (สว่าง/เปิดใช้งาน)")
            
    else:
        st.warning("⏳ กำลังรอข้อมูลจาก Firebase...")

    # หน่วงเวลา 5 วินาที แล้วรีเฟรชหน้าต่างอัตโนมัติ
    time.sleep(5)
    st.rerun() # อัปเดตคำสั่งใหม่ แทนที่ st.experimental_rerun()