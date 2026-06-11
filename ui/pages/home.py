from __future__ import annotations

import streamlit as st

from state.session_store import get_bookings, get_doctors
from ui.components import render_stats


def render() -> None:
    st.header("Home")
    doctors = get_doctors()
    bookings = get_bookings()

    render_stats(doctors, bookings)

    st.markdown(
        """
        ### What this app does
        - Admins can onboard, edit, and delete doctors
        - Users can browse and filter doctors
        - Users can book consultation slots
        - Booking conflicts are handled in the session-state pipeline
        - AI helper can suggest a specialization and the best matching doctor
        """
    )

    st.info("Data is stored in `st.session_state`, so it stays available for the active browser session.")
