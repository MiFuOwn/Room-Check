import random
import time
from dataclasses import dataclass
from typing import Optional

import requests
import streamlit as st

from config import FIREBASE_DB_URL, MOCK_MODE, REQUEST_TIMEOUT_SECONDS


@dataclass
class RoomReading:
    room_id: str
    light: Optional[int]
    sound: Optional[int]
    updated_at_ms: Optional[int]
    stale: bool
    error: Optional[str]

def fetch_rooms(room_ids: list[str]) -> dict[str, RoomReading]:
    """Fetch readings for multiple rooms at once (each still hits fetch_room's
    own 4s cache, so this is cheap to call repeatedly)."""
    return {room_id: fetch_room(room_id) for room_id in room_ids}

def _room_url(room_id: str) -> str:
    return f"{FIREBASE_DB_URL.rstrip('/')}/rooms/{room_id}.json"


def _mock_reading(room_id: str) -> RoomReading:
    light = random.randint(20, 100)
    sound = random.randint(150, 700)
    return RoomReading(
        room_id=room_id,
        light=light,
        sound=sound,
        updated_at_ms=int(time.time() * 1000),
        stale=False,
        error=None,
    )


@st.cache_data(ttl=4, show_spinner=False)
def fetch_room(room_id: str) -> RoomReading:
    if MOCK_MODE:
        return _mock_reading(room_id)

    try:
        resp = requests.get(_room_url(room_id), timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return RoomReading(room_id, None, None, None, stale=True, error=str(exc))

    payload = resp.json() or {}
    light = payload.get("light") if isinstance(payload, dict) else None
    sound = payload.get("sound") if isinstance(payload, dict) else None
    updated_at = payload.get("updated_at") if isinstance(payload, dict) else None

    if light is None and sound is None:
        return RoomReading(room_id, None, None, updated_at, stale=True, error="no_data")

    return RoomReading(room_id, light, sound, updated_at, stale=False, error=None)