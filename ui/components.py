from __future__ import annotations

from io import StringIO
import csv
from typing import Any, Dict, List

import streamlit as st


def doctor_card(doctor: Dict[str, Any]) -> None:
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            st.subheader(doctor["name"])
            st.write(f"**Specialization:** {doctor['specialization']}")
            st.write(f"**Experience:** {doctor['experience']} years")
        with c2:
            st.write(f"**Fee:** ₹{doctor['fee']}")
            st.write(f"**Available Slots:** {doctor['available_slots']}")
        with c3:
            available = [slot for slot in doctor.get("slots", []) if not slot.get("is_booked")]
            if available:
                st.write("**Next slot:**")
                st.code(available[0]["slot_time"])
            else:
                st.error("No slots left")


def render_stats(doctors: List[Dict[str, Any]], bookings: List[Dict[str, Any]]) -> None:
    a, b, c = st.columns(3)
    a.metric("Doctors", len(doctors))
    b.metric("Bookings", len(bookings))
    c.metric("Available Slots", sum(doc.get("available_slots", 0) for doc in doctors))


def bookings_to_csv(bookings: List[Dict[str, Any]]) -> bytes:
    buffer = StringIO()
    if bookings:
        writer = csv.DictWriter(buffer, fieldnames=list(bookings[0].keys()))
        writer.writeheader()
        writer.writerows(bookings)
    else:
        buffer.write("")
    return buffer.getvalue().encode("utf-8")
