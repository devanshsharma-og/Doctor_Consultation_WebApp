from __future__ import annotations

import uuid
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pipelines.doctor_pipeline import recompute_available_slots, utc_now


def create_booking_record(
    doctor: Dict[str, Any],
    slot: Dict[str, Any],
    user_name: str,
) -> Dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "doctor_id": doctor["id"],
        "doctor_name": doctor["name"],
        "specialization": doctor["specialization"],
        "slot_id": slot["id"],
        "slot_time": slot["slot_time"],
        "user_name": user_name.strip(),
        "booked_at": utc_now(),
    }


def find_slot(doctor: Dict[str, Any], slot_id: str) -> Optional[Dict[str, Any]]:
    for slot in doctor.get("slots", []):
        if slot["id"] == slot_id:
            return slot
    return None


def book_slot(
    doctors: List[Dict[str, Any]],
    bookings: List[Dict[str, Any]],
    doctor_id: str,
    slot_id: str,
    user_name: str,
) -> Tuple[Optional[Dict[str, Any]], str]:
    if not user_name or not user_name.strip():
        return None, "Please enter a valid user name."

    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if not doctor:
        return None, "Doctor not found."

    slot = find_slot(doctor, slot_id)
    if not slot:
        return None, "Selected slot does not exist."

    if slot.get("is_booked"):
        return None, "That slot was already booked."

    slot["is_booked"] = True
    booking = create_booking_record(doctor, slot, user_name)
    bookings.append(booking)

    # Update counters on the doctor record.
    for idx, doc in enumerate(doctors):
        if doc["id"] == doctor_id:
            doctors[idx] = recompute_available_slots(doctor)
            break

    return booking, "Booking confirmed."


def list_bookings(bookings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(bookings, key=lambda item: item.get("booked_at", ""), reverse=True)
