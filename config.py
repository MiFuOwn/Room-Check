"""
Central configuration for Room-Check.

All environment-specific values (URLs, tokens, thresholds) live here so the
rest of the app never hard-codes secrets or magic numbers. Values are read
from Streamlit secrets (`.streamlit/secrets.toml`) with sane fallbacks so the
app still runs locally even if secrets.toml doesn't exist yet.
"""
from __future__ import annotations

import streamlit as st


def _get_secret(section: str, key: str, default: str) -> str:
    """Read st.secrets[section][key], falling back to `default` if the
    secrets file doesn't exist, the section is missing, or the key is missing.
    """
    try:
        return st.secrets.get(section, {}).get(key, default)
    except Exception:
        return default


# ---------------------------------------------------------------------------
# Firebase Realtime Database
# ---------------------------------------------------------------------------
FIREBASE_DB_URL: str = _get_secret(
    "firebase",
    "database_url",
    "https://roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app",
)

# ---------------------------------------------------------------------------
# LINE Messaging API (optional - notifications are skipped if not configured)
# ---------------------------------------------------------------------------
LINE_CHANNEL_ACCESS_TOKEN: str = _get_secret("line", "channel_access_token", "")
LINE_TARGET_USER_ID: str = _get_secret("line", "target_user_id", "")

# ---------------------------------------------------------------------------
# Buildings & Rooms
# ---------------------------------------------------------------------------
# One source of truth for the building/room hierarchy. Add or remove rooms
# here only -- the UI (home page + sidebar) is generated from this dict.
# NOTE: room ids below for Building 7/9/12 are placeholders following the
# same naming pattern as Building 2. Replace with your actual room numbers.
BUILDINGS: dict[str, list[str]] = {
    "Building 2": ["2-304", "2-305", "2-306", "2-307", "2-308", "2-310", "2-311", "2-312"],
    "Building 7": ["7-201", "7-202", "7-203", "7-204"],
    "Building 9": ["9-101", "9-102", "9-103", "9-104"],
    "Building 12": ["12-501", "12-502", "12-503", "12-504"],
}

# ---------------------------------------------------------------------------
# Sensor thresholds
# ---------------------------------------------------------------------------
LIGHT_ON_THRESHOLD: int = 50       # <= this value (0-100 scale) means the light is considered ON
SOUND_LOUD_THRESHOLD: int = 490    # >= this value (0-1023 scale) means the room is considered noisy
SOUND_MAX: int = 1023

# ---------------------------------------------------------------------------
# App behaviour
# ---------------------------------------------------------------------------
AUTO_REFRESH_SECONDS: int = 5
REQUEST_TIMEOUT_SECONDS: float = 4.0

# ตั้งเป็น True เพื่อจำลองค่าแสง/เสียงโดยไม่ต้องต่อ Firebase จริง
# (เหมาะสำหรับทดสอบ UI ก่อนมีฮาร์ดแวร์จริง)
MOCK_MODE: bool = True