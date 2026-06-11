# Module Overview

## state/session_store.py
Creates and manages the app's session-state store. This is the only place where the Streamlit session keys are defined.

## pipelines/doctor_pipeline.py
Contains the doctor CRUD pipeline:
- create doctor
- update doctor
- delete doctor
- filter and sort doctors
- compute available slot counts

## pipelines/booking_pipeline.py
Contains the booking pipeline:
- validate inputs
- prevent double booking
- create booking records
- keep doctor slot counts in sync

## pipelines/recommendation_pipeline.py
Contains the AI helper pipeline:
- symptom keyword matching
- specialization recommendations
- doctor ranking
- next available slot detection

## ui/pages/
Each file renders one Streamlit page so the app stays easy to maintain and extend.
