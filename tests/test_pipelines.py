from pipelines.booking_pipeline import book_slot
from pipelines.doctor_pipeline import create_doctor_record
from pipelines.recommendation_pipeline import recommend_specialization


def test_double_booking_is_blocked():
    doctors = [create_doctor_record("Dr. Test", "Cardiology", 10, 500, ["2026-05-25 10:00"])]
    bookings = []

    doctor = doctors[0]
    slot_id = doctor["slots"][0]["id"]

    booking1, message1 = book_slot(doctors, bookings, doctor["id"], slot_id, "Alice")
    booking2, message2 = book_slot(doctors, bookings, doctor["id"], slot_id, "Bob")

    assert booking1 is not None
    assert "confirmed" in message1.lower()
    assert booking2 is None
    assert "already booked" in message2.lower()


def test_recommend_specialization_keyword_match():
    assert recommend_specialization("I have chest pain and shortness of breath") == "Cardiology"
