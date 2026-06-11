from __future__ import annotations

import streamlit as st

from state.session_store import get_bookings
from ui.components import bookings_to_csv


def render() -> None:
    st.header("🧾 Booking Management")
    bookings = get_bookings()

    if not bookings:
        st.info("No bookings yet.")
        return

    st.dataframe(bookings, use_container_width=True)
    st.download_button(
        "Download bookings as CSV",
        bookings_to_csv(bookings),
        "bookings.csv",
        "text/csv",
    )
