from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Any


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")
        if not any(
            member.rank in (Rank.captain, Rank.commander)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Captain or Commander"
            )
        if self.duration_days > 365:
            experienced = sum(
                member.years_experience >= 5
                for member in self.crew
            )

            if experienced / len(self.crew) < 0.5:
                raise ValueError(
                    "Long missions require at least 50% experienced crew"
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def mission(data: dict[str, Any]) -> None:
    print("===========================")
    try:
        user = SpaceMission(**data)
        print("Valid mission created:")
        print(f"Mission: {user.mission_name}")
        print(f"ID: {user.mission_id}")
        print(f"Destination: {user.destination}")
        print(f"Duration: {user.duration_days} days")
        print(f"Budget: {user.budget_millions}")
        print(f"Crew size: {len(user.crew)}")
        print("Crew members: ")
        for member in user.crew:
            print(f"- {member.name} ({member.rank}) - {member.specialization}")
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))
    print()


def main() -> None:
    print("Space Mission Crew Validation")
    data1 = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": datetime(2027, 5, 1),
        "duration_days": 900,
        "crew": [
            {
                "member_id": "C001",
                "name": "Sarah Connor",
                "rank": "commander",
                "age": 80,
                "specialization": "Mission Command",
                "years_experience": 10
            },
            {
                "member_id": "C002",
                "name": "John Smith",
                "rank": "lieutenant",
                "age": 30,
                "specialization": "Navigation",
                "years_experience": 6
            },
            {
                "member_id": "C003",
                "name": "Alice Johnson",
                "rank": "officer",
                "age": 25,
                "specialization": "Engineering",
                "years_experience": 2
            }
        ],
        "budget_millions": 2500.0
    }
    mission(data1)
    data2 = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": datetime(2027, 5, 1),
        "duration_days": 900,
        "crew": [
            {
                "member_id": "C001",
                "name": "Sarah Connor",
                "rank": "cadet",
                "age": 35,
                "specialization": "Mission Command",
                "years_experience": 10
            },
            {
                "member_id": "C002",
                "name": "John Smith",
                "rank": "lieutenant",
                "age": 30,
                "specialization": "Navigation",
                "years_experience": 6
            },
            {
                "member_id": "C003",
                "name": "Alice Johnson",
                "rank": "officer",
                "age": 25,
                "specialization": "Engineering",
                "years_experience": 2
            }
        ],
        "budget_millions": 2500.0
    }
    mission(data2)


if __name__ == "__main__":
    main()
