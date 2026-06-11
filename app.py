from __future__ import annotations

import streamlit as st

from state.session_store import initialize_session_store
from ui.pages import assistant, booking, bookings, doctor_listing, home, admin


st.set_page_config(
    page_title="Doctor Consultation Web App",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_session_store()

st.title("🩺 Doctor Consultation Web App")
st.caption("A modular Streamlit app with session-state storage, booking workflows, and AI guidance.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        ["Home", "Admin Panel", "Doctor Listing", "Book Appointment", "Bookings", "AI Assistant"],
        label_visibility="collapsed",
    )

if page == "Home":
    home.render()
elif page == "Admin Panel":
    admin.render()
elif page == "Doctor Listing":
    doctor_listing.render()
elif page == "Book Appointment":
    booking.render()
elif page == "Bookings":
    bookings.render()
elif page == "AI Assistant":
    assistant.render()
