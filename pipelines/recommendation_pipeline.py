from __future__ import annotations

from typing import Any, Dict, List, Optional


SPECIALIZATION_KEYWORDS: Dict[str, str] = {
    "chest pain": "Cardiology",
    "heart": "Cardiology",
    "palpitation": "Cardiology",
    "rash": "Dermatology",
    "skin": "Dermatology",
    "acne": "Dermatology",
    "headache": "Neurology",
    "migraine": "Neurology",
    "seizure": "Neurology",
    "vision": "Ophthalmology",
    "eye": "Ophthalmology",
    "bone": "Orthopedics",
    "joint": "Orthopedics",
    "knee": "Orthopedics",
    "stomach": "Gastroenterology",
    "digestion": "Gastroenterology",
    "fever": "General Medicine",
    "cough": "General Medicine",
}


def recommend_specialization(symptoms: str) -> str:
    text = (symptoms or "").lower()
    for keyword, specialization in SPECIALIZATION_KEYWORDS.items():
        if keyword in text:
            return specialization
    return "General Medicine"


def rank_doctors(doctors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        doctors,
        key=lambda d: (
            -int(d.get("experience", 0)),
            float(d.get("fee", 0.0)),
            -int(d.get("available_slots", 0)),
            d.get("name", ""),
        ),
    )


def suggest_best_doctor(
    doctors: List[Dict[str, Any]],
    specialization: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    candidates = doctors
    if specialization:
        candidates = [doctor for doctor in doctors if doctor.get("specialization") == specialization]
    if not candidates:
        return None
    return rank_doctors(candidates)[0]


def next_available_slot(doctor: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for slot in doctor.get("slots", []):
        if not slot.get("is_booked"):
            return slot
    return None
