from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class Station(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str = Field(max_length=200)


def show_station(data: dict) -> None:
    print("===========================")
    try:
        user = Station(**data)
        print("Valid station created:")
        print(f"ID: {user.station_id}")
        print(f"Name: {user.name}")
        print(f"Crew: {user.crew_size} people")
        print(f"Power: {user.power_level}%")
        print(f"Oxygen: {user.oxygen_level}%")
        print(f"Last maintenance: {user.last_maintenance}")

        if user.is_operational:
            print("Status: Operational")
        else:
            print("Status: Not Operational")

    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])

    print()


def main() -> None:
    print("Space Station Data Validation")
    show_station({
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2026-10-13T10:28:00",
        "notes": "Hell yeah, bro, let's do this!",
    })

    show_station({
        "station_id": "ISS002",
        "name": "International Space Station",
        "crew_size": 23,
        "power_level": 99.9,
        "oxygen_level": 92.3,
        "last_maintenance": "2026-10-13T10:28:00",
        "notes": "Catch ya later, fam!",
    })


if __name__ == "__main__":
    main()
