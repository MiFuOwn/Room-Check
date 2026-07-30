import streamlit as st
from utils.icons import BUILDING, OVERVIEW, icon_html

from config import BUILDINGS, LIGHT_ON_THRESHOLD, SOUND_LOUD_THRESHOLD
from utils.firebase_client import fetch_rooms
from utils.theme import inject_base_css

st.set_page_config(page_title="Room-Check | Smart Campus", page_icon="◻", layout="wide")
inject_base_css()

st.markdown("<div class='swiss-header'>Room-Check</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='swiss-subheader'>ระบบตรวจสอบและจัดการสถานะห้องเรียนแบบเรียลไทม์</div>",
    unsafe_allow_html=True,
)

col_left, col_center, col_right = st.columns([1, 3, 1])
with col_center:
    st.image("images/Homepage1.jfif", width=880)

st.write("")
st.markdown("<div class='swiss-label'>Select building</div>", unsafe_allow_html=True)
st.write("")

building_names = list(BUILDINGS.keys())
columns = st.columns(len(building_names))

for col, name in zip(columns, building_names):
    room_ids = BUILDINGS[name]
    caption = f"{len(room_ids)} rooms monitored" if room_ids else "Not yet instrumented"

    light_count = noisy_count = 0
    if room_ids:
        readings = fetch_rooms(room_ids)
        for r in readings.values():
            if r.light is not None and r.light <= LIGHT_ON_THRESHOLD:
                light_count += 1
            if r.sound is not None and r.sound >= SOUND_LOUD_THRESHOLD:
                noisy_count += 1

    badges = ""
    if room_ids:
        light_cls = "alert" if light_count else "ok"
        sound_cls = "alert" if noisy_count else "ok"
        badges = (
            '<div class="badge-row">'
            f'<span class="status-badge {light_cls}">Light {light_count}</span>'
            f'<span class="status-badge {sound_cls}">Loud {noisy_count}</span>'
            '</div>'
        )

    with col:
        card_html = (
            '<a href="/page_1" target="_self" style="text-decoration:none;">'
            '<div class="building-card">'
            f'{icon_html(BUILDING)}'
            f'<div class="building-name">{name}</div>'
            f'<div class="building-caption">{caption}</div>'
            f'{badges}'
            '</div>'
            '</a>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

st.write("---")
st.markdown(
    '<a href="/page_2" target="_self" style="text-decoration:none;">'
    '<div class="overview-cta">'
    f'{icon_html(OVERVIEW, "accent")}'
    '<div>'
    '<div class="overview-cta-title">View overview of all rooms</div>'
    '<div class="overview-cta-caption">เห็นทุกห้องทุกตึกในหน้าเดียว</div>'
    '</div>'
    '<div class="overview-cta-arrow">&#8594;</div>'
    '</div>'
    '</a>',
    unsafe_allow_html=True,
)
st.caption("Data is read live from Firebase Realtime Database.")