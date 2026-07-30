import plotly.graph_objects as go
import streamlit as st

from config import (
    AUTO_REFRESH_SECONDS,
    BUILDINGS,
    LIGHT_ON_THRESHOLD,
    SOUND_LOUD_THRESHOLD,
    SOUND_MAX,
)
from utils.firebase_client import fetch_room
from utils.icons import BULB, DOOR, HOME, SPEAKER, icon_html
from utils.notify import disarm, notify_once
from utils.theme import inject_base_css

st.set_page_config(page_title="Room Dashboard | Room-Check", page_icon="◻", layout="wide")
inject_base_css()

st.sidebar.markdown(
    f"<div class='sidebar-brand'>{icon_html(HOME)} Room-Check</div>",
    unsafe_allow_html=True,
)
st.sidebar.page_link("main.py", label="Home")
st.sidebar.write("---")

all_rooms = [room for rooms in BUILDINGS.values() for room in rooms]
if not all_rooms:
    st.warning("No rooms are configured yet. Add rooms to BUILDINGS in config.py.")
    st.stop()

st.sidebar.markdown(
    f"<div class='sidebar-brand'>{icon_html(DOOR)} Room selection</div>",
    unsafe_allow_html=True,
)
selected_room = st.sidebar.selectbox("Select room", all_rooms, label_visibility="collapsed")
st.sidebar.write("---")


@st.fragment(run_every=AUTO_REFRESH_SECONDS)
def render_room_dashboard(room_id: str) -> None:
    reading = fetch_room(room_id)

    st.markdown(
        f"<div class='swiss-header'>{icon_html(DOOR)} Room {room_id}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='swiss-subheader'>Live light &amp; sound monitoring</div>", unsafe_allow_html=True)

    if reading.error or reading.light is None or reading.sound is None:
        st.warning(f"No live data for room {room_id} yet. Check the sensor node is powered on.")
        st.sidebar.markdown("<div class='swiss-label'>Status</div>", unsafe_allow_html=True)
        st.sidebar.info(f"{room_id}: waiting for data")
        return

    is_light_on = reading.light <= LIGHT_ON_THRESHOLD
    is_noisy = reading.sound >= SOUND_LOUD_THRESHOLD

    st.sidebar.markdown("<div class='swiss-label'>Live status</div>", unsafe_allow_html=True)
    status_bits = []
    if is_light_on:
        status_bits.append("light on")
    if is_noisy:
        status_bits.append("loud")
    st.sidebar.info(f"{room_id}: {', '.join(status_bits) if status_bits else 'normal'}")

    alert_key = f"notified_{room_id}"
    if is_light_on:
        notify_once(alert_key, f"Alert: the light in room {room_id} is on.")
    else:
        disarm(alert_key)

    col1, col2, col3 = st.columns([1, 1, 1.4])

    with col1:
        css_class = "alert" if is_light_on else "ok"
        st.markdown(
            f"""<div class="metric-card {css_class}">
                <div class="metric-title-row">
                    {icon_html(BULB, css_class)}
                    <span class="metric-title">Light status</span>
                </div>
                <div class="metric-value {css_class}">{'On' if is_light_on else 'Normal (off)'}</div>
                <div class="metric-footnote">Sensor reading: {reading.light} / 100</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with col2:
        css_class = "alert" if is_noisy else "ok"
        st.markdown(
            f"""<div class="metric-card {css_class}">
                <div class="metric-title-row">
                    {icon_html(SPEAKER, css_class)}
                    <span class="metric-title">Sound level</span>
                </div>
                <div class="metric-value {css_class}">{'Loud' if is_noisy else 'Normal'}</div>
                <div class="metric-footnote">Sensor reading: {reading.sound} / {SOUND_MAX}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with col3:
        fig = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=reading.sound,
                mode="gauge+number",
                title={"text": "Sound level", "font": {"size": 16, "color": "#1A1A1A"}},
                gauge={
                    "axis": {"range": [0, SOUND_MAX], "tickcolor": "#808080"},
                    "bar": {"color": "#1A1A1A"},
                    "bgcolor": "white",
                    "borderwidth": 1,
                    "bordercolor": "#E5E5E0",
                    "steps": [
                        {"range": [0, SOUND_LOUD_THRESHOLD * 0.6], "color": "#EAF3EE"},
                        {"range": [SOUND_LOUD_THRESHOLD * 0.6, SOUND_LOUD_THRESHOLD], "color": "#FBF3E4"},
                        {"range": [SOUND_LOUD_THRESHOLD, SOUND_MAX], "color": "#FBEAE8"},
                    ],
                    "threshold": {"line": {"color": "#C0392B", "width": 3}, "thickness": 0.75, "value": SOUND_LOUD_THRESHOLD},
                },
            )
        )
        fig.update_layout(height=240, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={"color": "#1A1A1A"})
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.caption(f"Auto-refreshing every {AUTO_REFRESH_SECONDS}s · this panel only.")


render_room_dashboard(selected_room)