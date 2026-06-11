from __future__ import annotations

import streamlit as st

from pipelines.doctor_pipeline import get_specializations, list_doctors
from state.session_store import get_doctors
from ui.components import doctor_card


def render() -> None:
    st.header("🔍 Doctor Listing & Filtering")
    doctors = get_doctors()
    specializations = get_specializations(doctors)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        spec = st.selectbox("Specialization", specializations)
    with c2:
        min_exp = st.number_input("Minimum experience", min_value=0, step=1, value=0)
    with c3:
        max_fee = st.number_input("Maximum fee", min_value=0.0, step=50.0, value=5000.0)
    with c4:
        search = st.text_input("Search name/spec")

    filtered = list_doctors(
        doctors,
        specialization=spec,
        min_experience=int(min_exp),
        max_fee=float(max_fee),
        search=search.strip() or None,
    )

    st.write(f"Found **{len(filtered)}** doctor(s).")
    page_size = st.selectbox("Doctors per page", [3, 5, 10], index=1)
    page_num = st.number_input("Page", min_value=1, step=1, value=1)
    start = (page_num - 1) * page_size
    current = filtered[start:start + page_size]

    if not current:
        st.warning("No doctors match the selected filters.")
        return

    for doctor in current:
        doctor_card(doctor)
