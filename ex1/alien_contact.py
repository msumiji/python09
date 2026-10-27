from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELE = "telepathic"

class Station(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15, pattern=r"^AC")
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str = Field(max_length=200)
    is_verified: bool = False

    @model_validator(mode='after')
    def baka(self) -> "Station":
        if (
            self.contact_type == ContactType.PHYSICAL
            and self.is_verified == False
        ):
            raise ValueError(
                "physical contact report must be verified"
            )
        if (
            self.contact_type == ContactType.TELE
            and self.witness_count < 3
        ):
            raise ValueError(
                "telepathic contact requires at least 3 witnesses"
            )
        if (
            self.signal_strength >7.0
            and not self.message_received
        ):
            raise ValueError(
                "Strong signals should include received messages"
            )
        return self

def alien(data: dict) -> None:
    print("===========================")
    try:
        user = Station(**data)
        print("Valid contact report:")
        print(f"ID: {user.contact_id}")
        print(f"Type: {user.contact_type.value}")
        print(f"Signal: {user.signal_strength}/10")
        print(f"Duration: {user.duration_minutes} minutes")
        print(f"Witnesses: {user.witness_count}")
        print(f"Message: '{user.message_received}'")

    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))

    print()


def main() -> None:
    print("Alien Contact Log Validation")
    alien({
        "contact_id": "AC_2024_001",
        "timestamp": "2026-10-13T10:28:00",
        "location": "Area 51, Nevada",
        "contact_type": ContactType.RADIO,
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli"
    })
    alien({
        "contact_id": "AC_2024_001",
        "timestamp": "2026-10-13T10:28:00",
        "location": "Area 51, Nevada",
        "contact_type": ContactType.TELE,
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 2,
        "message_received": "Greetings from Zeta Reticuli"
    })

if __name__ == "__main__":
    main()
