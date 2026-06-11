from __future__ import annotations

import streamlit as st

from pipelines.doctor_pipeline import create_doctor_record, delete_doctor_by_id, list_doctors, update_doctor_record
from state.session_store import get_bookings, get_doctors
from ui.components import doctor_card


def render() -> None:
    st.header("👨‍⚕️ Admin Panel")
    doctors = get_doctors()

    tab1, tab2 = st.tabs(["Add Doctor", "Manage Doctors"])

    with tab1:
        with st.form("add_doctor_form", clear_on_submit=True):
            name = st.text_input("Doctor Name")
            specialization = st.text_input("Specialization")
            experience = st.number_input("Experience (years)", min_value=0, step=1, value=5)
            fee = st.number_input("Consultation Fee", min_value=0.0, step=50.0, value=500.0)
            slots_text = st.text_area(
                "Available Slots (one per line, e.g. 2026-05-25 10:00)",
                height=160,
            )
            submitted = st.form_submit_button("Add Doctor")
            if submitted:
                if not name.strip() or not specialization.strip():
                    st.error("Name and specialization are required.")
                else:
                    slots = [line.strip() for line in slots_text.splitlines() if line.strip()]
                    if not slots:
                        st.error("At least one slot is required.")
                    else:
                        doctors.append(
                            create_doctor_record(
                                name=name,
                                specialization=specialization,
                                experience=int(experience),
                                fee=float(fee),
                                slots=slots,
                            )
                        )
                        st.success("Doctor added successfully.")
                        st.rerun()

    with tab2:
        filtered_doctors = list_doctors(doctors, search=None)
        if not filtered_doctors:
            st.warning("No doctors found.")
            return

        for doctor in filtered_doctors:
            with st.expander(f"{doctor['name']} — {doctor['specialization']}"):
                with st.form(f"edit_{doctor['id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Name", value=doctor["name"])
                        exp = st.number_input("Experience", min_value=0, step=1, value=int(doctor["experience"]))
                        slots_value = "\n".join([slot["slot_time"] for slot in doctor["slots"]])
                        slots_text = st.text_area("Slots (one per line)", value=slots_value, height=140)
                    with col2:
                        spec = st.text_input("Specialization", value=doctor["specialization"])
                        fee = st.number_input("Fee", min_value=0.0, step=50.0, value=float(doctor["fee"]))
                        st.write(f"Available slots: {doctor['available_slots']}")
                        st.caption("Booked slots are preserved automatically during edits.")
                    update = st.form_submit_button("Save Changes")
                    if update:
                        idx = next((i for i, doc in enumerate(doctors) if doc["id"] == doctor["id"]), None)
                        if idx is None:
                            st.error("Update failed. Doctor not found.")
                        else:
                            doctors[idx] = update_doctor_record(
                                doctor,
                                name=name,
                                specialization=spec,
                                experience=int(exp),
                                fee=float(fee),
                                slots=[line.strip() for line in slots_text.splitlines() if line.strip()],
                            )
                            st.success("Doctor updated.")
                            st.rerun()

                if st.button("Delete Doctor", key=f"del_{doctor['id']}"):
                    removed = delete_doctor_by_id(doctors, doctor["id"])
                    if removed:
                        bookings = get_bookings()
                        bookings[:] = [booking for booking in bookings if booking["doctor_id"] != doctor["id"]]
                        st.success("Doctor deleted.")
                        st.rerun()
