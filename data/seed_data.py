from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


def get_seed_doctors() -> List[Dict[str, Any]]:
    return [
        {
            "id": "seed-cardio-1",
            "name": "Dr. John Doe",
            "specialization": "Cardiology",
            "experience": 12,
            "fee": 800.0,
            "created_at": "2026-05-25T08:00:00",
            "updated_at": "2026-05-25T08:00:00",
            "slots": [
                {"id": "seed-cardio-1-slot-1", "slot_time": "2026-05-25 10:00", "is_booked": False},
                {"id": "seed-cardio-1-slot-2", "slot_time": "2026-05-25 11:00", "is_booked": False},
                {"id": "seed-cardio-1-slot-3", "slot_time": "2026-05-25 12:00", "is_booked": False},
            ],
            "available_slots": 3,
        },
        {
            "id": "seed-derma-1",
            "name": "Dr. Priya Sharma",
            "specialization": "Dermatology",
            "experience": 9,
            "fee": 650.0,
            "created_at": "2026-05-25T08:00:00",
            "updated_at": "2026-05-25T08:00:00",
            "slots": [
                {"id": "seed-derma-1-slot-1", "slot_time": "2026-05-25 14:00", "is_booked": False},
                {"id": "seed-derma-1-slot-2", "slot_time": "2026-05-25 15:00", "is_booked": False},
            ],
            "available_slots": 2,
        },
        {
            "id": "seed-ortho-1",
            "name": "Dr. A. Kumar",
            "specialization": "Orthopedics",
            "experience": 15,
            "fee": 900.0,
            "created_at": "2026-05-25T08:00:00",
            "updated_at": "2026-05-25T08:00:00",
            "slots": [
                {"id": "seed-ortho-1-slot-1", "slot_time": "2026-05-25 16:00", "is_booked": False},
                {"id": "seed-ortho-1-slot-2", "slot_time": "2026-05-26 10:00", "is_booked": False},
            ],
            "available_slots": 2,
        },
        {
            "id": "seed-gm-1",
            "name": "Dr. Meera Singh",
            "specialization": "General Medicine",
            "experience": 7,
            "fee": 500.0,
            "created_at": "2026-05-25T08:00:00",
            "updated_at": "2026-05-25T08:00:00",
            "slots": [
                {"id": "seed-gm-1-slot-1", "slot_time": "2026-05-25 09:00", "is_booked": False},
                {"id": "seed-gm-1-slot-2", "slot_time": "2026-05-25 09:30", "is_booked": False},
            ],
            "available_slots": 2,
        },
    ]
