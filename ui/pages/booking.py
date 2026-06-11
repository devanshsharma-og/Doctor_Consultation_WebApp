from __future__ import annotations

import streamlit as st

from pipelines.booking_pipeline import book_slot
from pipelines.doctor_pipeline import list_doctors
from state.session_store import get_bookings, get_doctors


def render() -> None:
    st.header("📅 Book Consultation Slot")
    doctors = get_doctors()
    bookings = get_bookings()

    if not doctors:
        st.warning("No doctors available.")
        return

    doc_map = {
        f"{doctor['name']} — {doctor['specialization']} (₹{doctor['fee']})": doctor
        for doctor in list_doctors(doctors)
    }
    selected_label = st.selectbox("Choose doctor", list(doc_map.keys()))
    selected_doctor = doc_map[selected_label]
    available_slots = [slot for slot in selected_doctor["slots"] if not slot["is_booked"]]

    if not available_slots:
        st.error("This doctor has no available slots.")
        return

    st.write("Available slots:")
    slot_labels = {slot["slot_time"]: slot for slot in available_slots}
    slot_choice = st.radio("Select slot", list(slot_labels.keys()), horizontal=False)
    user_name = st.text_input("Your name")

    if st.button("Confirm Booking"):
        booking, message = book_slot(
            doctors=doctors,
            bookings=bookings,
            doctor_id=selected_doctor["id"],
            slot_id=slot_labels[slot_choice]["id"],
            user_name=user_name,
        )
        if booking:
            st.success(message)
            st.json(booking)
            st.balloons()
        else:
            st.error(message)
