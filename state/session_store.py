from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

import streamlit as st

from data.seed_data import get_seed_doctors

STORE_KEY = "doctor_consultation_store"


def _default_store() -> Dict[str, Any]:
    return {
        "doctors": [],
        "bookings": [],
        "meta": {
            "seeded": False,
        },
    }


def get_store() -> Dict[str, Any]:
    if STORE_KEY not in st.session_state:
        st.session_state[STORE_KEY] = _default_store()
    return st.session_state[STORE_KEY]


def reset_store(seed: bool = True) -> None:
    st.session_state[STORE_KEY] = _default_store()
    if seed:
        seed_demo_data()


def initialize_session_store(seed: bool = True) -> None:
    store = get_store()
    if seed and not store.get("meta", {}).get("seeded", False):
        seed_demo_data()


def seed_demo_data() -> None:
    store = get_store()
    if store["doctors"]:
        store["meta"]["seeded"] = True
        return

    store["doctors"] = deepcopy(get_seed_doctors())
    store["bookings"] = []
    store["meta"]["seeded"] = True


def get_doctors() -> List[Dict[str, Any]]:
    return get_store()["doctors"]


def get_bookings() -> List[Dict[str, Any]]:
    return get_store()["bookings"]


def set_doctors(doctors: List[Dict[str, Any]]) -> None:
    get_store()["doctors"] = doctors


def set_bookings(bookings: List[Dict[str, Any]]) -> None:
    get_store()["bookings"] = bookings


def app_stats() -> Dict[str, int]:
    store = get_store()
    doctors = store["doctors"]
    bookings = store["bookings"]
    available_slots = sum(doc.get("available_slots", 0) for doc in doctors)
    return {
        "doctors": len(doctors),
        "bookings": len(bookings),
        "available_slots": available_slots,
    }
