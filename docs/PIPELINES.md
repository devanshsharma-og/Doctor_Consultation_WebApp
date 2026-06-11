# Pipelines

## 1. Doctor pipeline
Input:
- doctor name
- specialization
- experience
- fee
- slot list

Output:
- normalized doctor record with slot metadata

## 2. Booking pipeline
Input:
- doctor_id
- slot_id
- user_name

Output:
- booking record if the slot is available
- rejection message if the slot has already been taken

## 3. Recommendation pipeline
Input:
- symptom text

Output:
- suggested specialization
- best matching doctor
- next available slot
