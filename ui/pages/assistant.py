from __future__ import annotations

import streamlit as st

from pipelines.doctor_pipeline import list_doctors
from pipelines.recommendation_pipeline import next_available_slot, recommend_specialization, suggest_best_doctor
from state.session_store import get_doctors
from ui.components import doctor_card


def render() -> None:
    st.header("🤖 AI Assistant")
    symptoms = st.text_area("Describe symptoms")

    if st.button("Recommend specialization"):
        specialization = recommend_specialization(symptoms)
        st.success(f"Recommended specialization: {specialization}")

        doctors = get_doctors()
        candidates = list_doctors(doctors, specialization=specialization)
        best = suggest_best_doctor(candidates, specialization=specialization)

        if best:
            st.subheader("Suggested doctor")
            doctor_card(best)
            slot = next_available_slot(best)
            if slot:
                st.write("Suggested next available slot:")
                st.code(slot["slot_time"])
            else:
                st.warning("No available slots for this specialization.")
        else:
            st.warning("No matching doctors found.")
