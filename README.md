# This App is live and can be accessed at
https://doctorconsultationwebapp.streamlit.app/
# Doctor Consultation Web App

A modular Streamlit project for doctor discovery, appointment booking, admin management, and symptom-based suggestions.

## What changed in this version

- Data is stored in `st.session_state`
- The app is split into separate pipelines and page modules
- No database is required
- The project includes separate documentation files for the app structure and pipelines

## Project structure

- `app.py` — Streamlit entry point
- `state/session_store.py` — session-state storage and seeding
- `pipelines/doctor_pipeline.py` — doctor creation, filtering, updating, deletion
- `pipelines/booking_pipeline.py` — booking flow and conflict prevention
- `pipelines/recommendation_pipeline.py` — symptom-to-specialty helper logic
- `ui/pages/` — individual app pages
- `ui/components.py` — reusable UI pieces
- `data/seed_data.py` — initial demo doctors
- `docs/README_MODULES.md` — module overview
- `docs/PIPELINES.md` — pipeline breakdown

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Notes

- Data lives only in the active Streamlit session.
- Refreshing the app keeps the current browser session data.
- Opening a new browser session starts with seed data again.
- Booking conflict protection is handled in the booking pipeline by checking the selected slot before confirming it.
