# Room-Check (Smart Room Status Monitoring System)

Room-Check is an IoT (Internet of Things) system that works together with a web application to monitor the status of classrooms or meeting rooms within a building. The system displays data in real time on a dashboard (built with Streamlit), receiving environmental data (light and sound) from hardware sensors via Firebase Realtime Database, and is capable of sending automatic status notifications through a LINE bot.

---

## Key Features

1. **Hardware Sensor Node**: A microcontroller device that reads values from a light sensor (LDR) and a sound sensor, then transmits the data to a wireless database.
2. **Real-time Monitoring**: The web application retrieves data from Firebase and displays room status in real time.
3. **Interactive Dashboard and Visualization**: Rooms are categorized by building, and sound levels are displayed as a gauge chart using the Plotly library.
4. **Smart LINE Notification**: Sends an instant LINE notification when a light is detected as turned on, with a session management system to prevent duplicate message spam.

---

## Project Structure

This project is divided into two main parts: **Software (Web Application)** and **Hardware (Microcontroller Code)**.

```text
Room-check/
│
├── main.py                     # Main file for running the home page / building selection
├── pages/
│   ├── page_1.py               # Dashboard page showing room status and sound level chart
│   └── page_2.py               # Overview page showing room status and sound level chart
├── image/                      # Folder for storing web page images
├── room_check_sensor/
│   └── room_check_sensor.ino   # Code to upload to the ESP8266 / ESP32 board
└── README.md                   # Project documentation and usage guide
```

---

## Part 1: Software (Web Application)

### Installation and Running the Application
1. Install Python (version 3.8 or higher recommended).
2. Open a terminal (or Command Prompt) in this project folder and install the required packages:
   ```bash
   pip install streamlit plotly requests line-bot-sdk
   ```
3. Run the application with the following command:
   ```bash
   streamlit run main.py
   ```
4. The application will automatically open in your browser at `http://localhost:8501`.

### Additional Configuration
- **Firebase**: This code retrieves data from the Realtime Database URL: `https://roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app/data.json`
- **LINE Messaging API**: Set your `Channel Access Token`, obtained from LINE Developers, correctly in the `pages/page_1.py` file so that the application can send notifications successfully.

---

## Part 2: Hardware (Microcontroller Node)

### Required Components
- ESP8266 board (e.g., NodeMCU) or ESP32
- Light sensor (LDR Photoresistor Module)
- Sound sensor (e.g., KY-038 or MAX4466)
- Jumper wires

### Basic Wiring Guide

**For the ESP32 board:**
- **LDR Sensor (Light)** -> connect to pin `34` (Analog)
- **Sound Sensor** -> connect to pin `35` (Analog)

**For the ESP8266 board:**
- Since this board has only one analog pin (A0), the readings must be split as follows:
  - **LDR Sensor** -> connect to pin `A0` (Analog)
  - **Sound Sensor** -> connect to pin `D1` / `GPIO5` (Digital) to detect only whether sound is present or not

*(Note: Carefully check the VCC and GND pins of each sensor to prevent incorrect power supply.)*

### Uploading Code to the Board
1. Open the **Arduino IDE**.
2. Install the **Firebase ESP Client** library by going to `Sketch` -> `Include Library` -> `Manage Libraries...`, searching for `Firebase ESP Client`, and clicking Install.
3. Open the `room_check_sensor/room_check_sensor.ino` file.
4. Edit the following information in the code to match your setup:
   - `WIFI_SSID` and `WIFI_PASSWORD`
   - `API_KEY` (available in the Project Settings menu in Firebase)
5. Select the correct Board and Port, then click **Upload**.

---

## Recent Improvements (Patch Notes)
- **Performance**: Removed the resource-intensive data-fetching loop (`while True` generator) and replaced it with a single data fetch per page refresh (smoother loading, no freezing).
- **Visualization**: The sound gauge chart is now linked to actual sensor data (`sound_value`) instead of using randomly generated numbers (`random`).
- **LINE Anti-Spam Notification**: Added a session state system to track whether a notification has already been sent, preventing the application from repeatedly spamming LINE messages every 5 seconds.
- **Modern Streamlit**: Updated deprecated commands to use the `st.rerun()` function instead.