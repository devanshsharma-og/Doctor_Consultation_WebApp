from __future__ import annotations

import uuid
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id(prefix: str = "") -> str:
    base = str(uuid.uuid4())
    return f"{prefix}{base}" if prefix else base


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


def normalize_slots(slots: List[str]) -> List[str]:
    cleaned: List[str] = []
    seen = set()
    for raw in slots:
        slot = normalize_text(raw)
        if not slot or slot in seen:
            continue
        cleaned.append(slot)
        seen.add(slot)
    return cleaned


def doctor_sort_key(doctor: Dict[str, Any]):
    return (-int(doctor.get("experience", 0)), float(doctor.get("fee", 0.0)), doctor.get("name", ""))


def recompute_available_slots(doctor: Dict[str, Any]) -> Dict[str, Any]:
    updated = deepcopy(doctor)
    updated["available_slots"] = sum(1 for slot in updated.get("slots", []) if not slot.get("is_booked"))
    return updated


def create_doctor_record(
    name: str,
    specialization: str,
    experience: int,
    fee: float,
    slots: List[str],
) -> Dict[str, Any]:
    slot_times = normalize_slots(slots)
    created_at = utc_now()
    doctor_id = new_id("doc-")
    return {
        "id": doctor_id,
        "name": normalize_text(name),
        "specialization": normalize_text(specialization),
        "experience": int(experience),
        "fee": float(fee),
        "created_at": created_at,
        "updated_at": created_at,
        "slots": [
            {
                "id": new_id("slot-"),
                "slot_time": slot_time,
                "is_booked": False,
            }
            for slot_time in slot_times
        ],
        "available_slots": len(slot_times),
    }


def update_doctor_record(
    doctor: Dict[str, Any],
    name: Optional[str] = None,
    specialization: Optional[str] = None,
    experience: Optional[int] = None,
    fee: Optional[float] = None,
    slots: Optional[List[str]] = None,
) -> Dict[str, Any]:
    updated = deepcopy(doctor)
    if name is not None:
        updated["name"] = normalize_text(name)
    if specialization is not None:
        updated["specialization"] = normalize_text(specialization)
    if experience is not None:
        updated["experience"] = int(experience)
    if fee is not None:
        updated["fee"] = float(fee)

    if slots is not None:
        cleaned_slots = normalize_slots(slots)
        booked_times = {slot["slot_time"] for slot in updated.get("slots", []) if slot.get("is_booked")}
        preserved_booked = [deepcopy(slot) for slot in updated.get("slots", []) if slot.get("is_booked")]
        new_slots: List[Dict[str, Any]] = []

        for slot_time in cleaned_slots:
            if slot_time in booked_times:
                existing = next(slot for slot in preserved_booked if slot["slot_time"] == slot_time)
                new_slots.append(existing)
            else:
                new_slots.append(
                    {
                        "id": new_id("slot-"),
                        "slot_time": slot_time,
                        "is_booked": False,
                    }
                )

        updated["slots"] = new_slots

    updated["updated_at"] = utc_now()
    return recompute_available_slots(updated)


def list_doctors(
    doctors: List[Dict[str, Any]],
    specialization: Optional[str] = None,
    min_experience: Optional[int] = None,
    max_fee: Optional[float] = None,
    search: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results = [recompute_available_slots(doc) for doc in doctors]

    if specialization and specialization != "All":
        results = [d for d in results if d.get("specialization") == specialization]

    if min_experience is not None:
        results = [d for d in results if int(d.get("experience", 0)) >= int(min_experience)]

    if max_fee is not None:
        results = [d for d in results if float(d.get("fee", 0.0)) <= float(max_fee)]

    if search:
        query = search.lower().strip()
        results = [
            d
            for d in results
            if query in d.get("name", "").lower() or query in d.get("specialization", "").lower()
        ]

    return sorted(results, key=doctor_sort_key)


def get_doctor_by_id(doctors: List[Dict[str, Any]], doctor_id: str) -> Optional[Dict[str, Any]]:
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return recompute_available_slots(doctor)
    return None


def delete_doctor_by_id(doctors: List[Dict[str, Any]], doctor_id: str) -> bool:
    initial_len = len(doctors)
    doctors[:] = [doctor for doctor in doctors if doctor["id"] != doctor_id]
    return len(doctors) < initial_len


def get_specializations(doctors: List[Dict[str, Any]]) -> List[str]:
    specializations = sorted({doctor.get("specialization", "") for doctor in doctors if doctor.get("specialization")})
    return ["All"] + specializations
