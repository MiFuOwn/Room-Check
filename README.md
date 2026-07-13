# Room-Check (ระบบตรวจสอบสถานะห้องอัจฉริยะ)

Room-Check เป็นระบบ IoT (Internet of Things) ควบคู่กับเว็บแอปพลิเคชันที่ใช้สำหรับตรวจสอบสถานะของห้องเรียนหรือห้องประชุมต่างๆ ภายในอาคาร ระบบจะแสดงผลแบบ Real-time บน Dashboard (สร้างด้วย Streamlit) โดยรับข้อมูลสภาพแวดล้อม (แสงและเสียง) จากฮาร์ดแวร์เซนเซอร์ผ่าน Firebase Realtime Database และมีความสามารถในการส่งข้อความแจ้งเตือนสถานะผ่าน LINE บอตอัตโนมัติ

---

## 🌟 ฟีเจอร์หลัก (Features)

1. **Hardware Sensor Node**: ชุดไมโครคอนโทรลเลอร์อ่านค่าจากเซนเซอร์แสง (LDR) และเซนเซอร์เสียง (Sound Sensor) แล้วส่งข้อมูลขึ้นฐานข้อมูลไร้สาย
2. **Real-time Monitoring**: เว็บแอปพลิเคชันดึงข้อมูลจาก Firebase มาแสดงสถานะของห้องแบบเรียลไทม์
3. **Interactive Dashboard & Visualization**: มีการแบ่งหมวดหมู่อาคาร และแสดงระดับเสียงออกมาเป็นกราฟเกจ (Gauge Chart) ด้วยไลบรารี Plotly
4. **Smart LINE Notification**: แจ้งเตือนผ่าน LINE ทันทีเมื่อตรวจพบการเปิดไฟ โดยมีระบบ Session ป้องกันการสแปมข้อความซ้ำซ้อน

---

## 🛠️ โครงสร้างของโปรเจกต์ (Project Structure)

โปรเจกต์นี้แบ่งออกเป็น 2 ส่วนหลัก คือ **Software (เว็บแอปพลิเคชัน)** และ **Hardware (โค้ดสำหรับไมโครคอนโทรลเลอร์)**

```text
Room-check/
│
├── main.py                     # ไฟล์หลักสำหรับรันหน้า Homepage เลือกอาคาร
├── pages/
│   └── page_1.py               # หน้า Dashboard แสดงสถานะห้องและกราฟระดับเสียง
├── image/                      # โฟลเดอร์สำหรับเก็บรูปภาพหน้าเว็บ
├── room_check_sensor/
│   └── room_check_sensor.ino   # โค้ดสำหรับอัปโหลดลงบอร์ด ESP8266 / ESP32
└── README.md                   # คู่มืออธิบายโปรเจกต์และวิธีการใช้งาน
```

---

## 💻 ส่วนที่ 1: Software (Web Application)

### 📦 การติดตั้งและการรันแอปพลิเคชัน
1. ติดตั้ง Python (แนะนำเวอร์ชัน 3.8 ขึ้นไป)
2. เปิด Terminal (หรือ Command Prompt) ในโฟลเดอร์โปรเจกต์นี้ แล้วติดตั้งแพ็กเกจที่จำเป็น:
   ```bash
   pip install streamlit plotly requests line-bot-sdk
   ```
3. รันแอปพลิเคชันด้วยคำสั่ง:
   ```bash
   streamlit run main.py
   ```
4. ระบบจะเปิดหน้าเว็บแอปพลิเคชันขึ้นมาที่ `http://localhost:8501` อัตโนมัติ

### ⚙️ การตั้งค่าระบบเพิ่มเติม
- **Firebase**: โค้ดจะดึงข้อมูลผ่าน URL ของ Realtime Database: `https://roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app/data.json`
- **LINE Messaging API**: ให้ตั้งค่า `Channel Access Token` ที่คุณได้รับจาก LINE Developers ให้ถูกต้องในไฟล์ `pages/page_1.py` เพื่อให้แอปพลิเคชันส่งข้อความแจ้งเตือนได้สำเร็จ

---

## 🔌 ส่วนที่ 2: Hardware (Microcontroller Node)

### 🛠️ อุปกรณ์ที่ใช้
- บอร์ด ESP8266 (เช่น NodeMCU) หรือ ESP32
- เซนเซอร์แสง (LDR Photoresistor Module)
- เซนเซอร์เสียง (Sound Sensor Module เช่น KY-038 หรือ MAX4466)
- สายไฟ (Jumper Wires)

### ⚡ การต่อวงจร (Wiring Guide) เบื้องต้น

**สำหรับบอร์ด ESP32:**
- **LDR Sensor (แสง)** -> ต่อเข้าขา `34` (Analog)
- **Sound Sensor (เสียง)** -> ต่อเข้าขา `35` (Analog)

**สำหรับบอร์ด ESP8266:**
- เนื่องจากมีขา Analog (A0) เพียงขาเดียว เราจึงต้องแบ่งการอ่านค่าดังนี้:
  - **LDR Sensor** -> ต่อเข้าขา `A0` (Analog)
  - **Sound Sensor** -> ต่อเข้าขา `D1` / `GPIO5` (Digital) เพื่อตรวจจับแค่ว่ามีเสียงดังหรือไม่ดัง

*(หมายเหตุ: ตรวจสอบขา VCC และ GND ของเซนเซอร์ให้ดี ระวังการจ่ายไฟผิดสเปค)*

### 💻 การติดตั้งโค้ดลงบอร์ด
1. เปิดโปรแกรม **Arduino IDE**
2. ติดตั้งไลบรารี **Firebase ESP Client** โดยไปที่ `Sketch` -> `Include Library` -> `Manage Libraries...` แล้วค้นหา `Firebase ESP Client` กด Install
3. เปิดไฟล์ `room_check_sensor/room_check_sensor.ino` ขึ้นมา
4. แก้ไขข้อมูลเหล่านี้ในโค้ดให้เป็นของคุณ:
   - `WIFI_SSID` และ `WIFI_PASSWORD`
   - `API_KEY` (หาได้จากเมนู Project settings ของ Firebase)
5. เลือก Board และ Port ที่ถูกต้อง แล้วกด **Upload**

---

## 🐞 สิ่งที่ได้รับการปรับปรุงในเวอร์ชันล่าสุด (Patch Notes)
- 🚀 **Performance**: ยกเลิกการวนลูปดึงข้อมูล (`while True` Generator) ที่กินทรัพยากร เปลี่ยนเป็นการดึงข้อมูล 1 ครั้งต่อการรีเฟรชหน้าเว็บ (โหลดลื่นขึ้น ไม่ค้าง)
- 📈 **Visualization**: กราฟหน้าปัดเสียงตอนนี้เชื่อมโยงข้อมูลจริง (`sound_value`) จากเซนเซอร์ แทนที่จะเป็นการสุ่มตัวเลข (`random`)
- 💬 **Anti-Spam LINE Notify**: เพิ่มระบบ Session State เพื่อจำว่าแจ้งเตือนไปแล้ว ป้องกันปัญหาแอปสแปมข้อความส่งเข้า LINE รัวๆ ทุก 5 วินาที
- ♻️ **Modern Streamlit**: อัปเดตคำสั่งเก่าที่ยกเลิกใช้งาน เปลี่ยนไปใช้ฟังก์ชัน `st.rerun()` แทน