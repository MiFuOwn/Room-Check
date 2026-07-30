import streamlit as st

from config import BUILDINGS, LIGHT_ON_THRESHOLD, SOUND_LOUD_THRESHOLD
from utils.firebase_client import fetch_rooms
from utils.icons import HOME, icon_html
from utils.theme import inject_base_css

st.set_page_config(page_title="Overview | Room-Check", page_icon="◻", layout="wide")
inject_base_css()

st.sidebar.markdown(
    f"<div class='sidebar-brand'>{icon_html(HOME)} Room-Check</div>",
    unsafe_allow_html=True,
)
st.sidebar.page_link("main.py", label="Home")
st.sidebar.page_link("pages/page_1.py", label="Room dashboard")
st.sidebar.write("---")

st.markdown("<div class='swiss-header'>Overview</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='swiss-subheader'>สถานะทุกห้องทุกตึกในหน้าเดียว</div>",
    unsafe_allow_html=True,
)

for building_name, room_ids in BUILDINGS.items():
    st.markdown(f"<div class='overview-building'>{building_name}</div>", unsafe_allow_html=True)

    if not room_ids:
        st.caption("Not yet instrumented")
        continue

    readings = fetch_rooms(room_ids)

    header_html = (
        '<div class="overview-row header">'
        '<div>Room</div><div>Light</div><div>Sound</div><div>Status</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    for room_id in room_ids:
        r = readings[room_id]
        if r.light is None or r.sound is None:
            row_html = (
                '<div class="overview-row">'
                f'<div>{room_id}</div><div>—</div><div>—</div>'
                '<div><span class="status-badge">offline</span></div>'
                '</div>'
            )
            st.markdown(row_html, unsafe_allow_html=True)
            continue

        is_light_on = r.light <= LIGHT_ON_THRESHOLD
        is_noisy = r.sound >= SOUND_LOUD_THRESHOLD
        light_cls = "alert" if is_light_on else "ok"
        sound_cls = "alert" if is_noisy else "ok"
        overall_cls = "alert" if (is_light_on or is_noisy) else "ok"
        overall_text = "attention" if (is_light_on or is_noisy) else "normal"

        row_html = (
            '<div class="overview-row">'
            f'<div>{room_id}</div>'
            f'<div><span class="status-badge {light_cls}">{"on" if is_light_on else "off"}</span></div>'
            f'<div><span class="status-badge {sound_cls}">{"loud" if is_noisy else "quiet"}</span></div>'
            f'<div><span class="status-badge {overall_cls}">{overall_text}</span></div>'
            '</div>'
        )
        st.markdown(row_html, unsafe_allow_html=True)