import requests
import streamlit as st

from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_TARGET_USER_ID, REQUEST_TIMEOUT_SECONDS

_LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"


def is_configured() -> bool:
    return bool(LINE_CHANNEL_ACCESS_TOKEN and LINE_TARGET_USER_ID)


def send_line_message(text: str) -> bool:
    if not is_configured():
        return False

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    }
    body = {
        "to": LINE_TARGET_USER_ID,
        "messages": [{"type": "text", "text": text}],
    }
    try:
        resp = requests.post(_LINE_PUSH_URL, headers=headers, json=body, timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        st.warning(f"LINE notification failed: {exc}")
        return False


def notify_once(session_key: str, message: str) -> None:
    if not st.session_state.get(session_key, False):
        if send_line_message(message):
            st.session_state[session_key] = True


def disarm(session_key: str) -> None:
    st.session_state[session_key] = False