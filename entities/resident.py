#-- resident profile
"""Resident entity module for Civics Concierge."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class ServiceAddress(BaseModel):
    """Represents a resident's primary service address for municipal utilities."""
    street: str
    neighborhood_zone: str  # e.g., 'Historic', 'Industrial', 'Residential-A'
    council_district: int
    trash_pickup_day: str
    model_config = ConfigDict(from_attributes=True)


class MunicipalService(BaseModel):
    """Represents a city service or permit in a resident's history."""
    service_id: str
    service_name: str  # e.g., 'Bulk Trash Pickup', 'Parking Permit'
    status: str       # e.g., 'Completed', 'Pending', 'Active'
    model_config = ConfigDict(from_attributes=True)


class ServiceRequest(BaseModel):
    """Represents a resident's specific service interaction or permit application."""
    request_date: str
    items: List[MunicipalService]
    case_number: str
    model_config = ConfigDict(from_attributes=True)


class NotificationPreferences(BaseModel):
    """Represents a resident's city alert preferences."""
    emergency_alerts: bool = True
    utility_outages: bool = True
    community_events: bool = False
    model_config = ConfigDict(from_attributes=True)


class PropertyProfile(BaseModel):
    """Represents a resident's property details for zoning and permit logic."""
    property_type: str  # e.g., 'Single Family', 'Multi-Unit', 'Business'
    lot_size: str
    historical_status: bool = False
    active_permits: List[str]
    model_config = ConfigDict(from_attributes=True)


class Resident(BaseModel):
    """Represents a city resident."""
    resident_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    residency_start_date: str
    primary_address: ServiceAddress
    service_history: List[ServiceRequest]
    civic_points: int  # Loyalty equivalent for community engagement/volunteering
    notification_preferences: NotificationPreferences
    property_profile: PropertyProfile
    scheduled_inspections: Dict = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """Converts the Resident object to a JSON string."""
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_resident(current_resident_id: str) -> Optional["Resident"]:
        """
        Retrieves a resident based on their ID. 
        In production, this would use DatabaseSessionService for persistence.
        """
        return Resident(
            resident_id=current_resident_id,
            first_name="Alex",
            last_name="Johnson",
            email="alex.johnson@civic-example.gov",
            phone_number="+1-702-555-1212",
            residency_start_date="2022-06-10",
            primary_address=ServiceAddress(
                street="123 City St", 
                neighborhood_zone="Historic", 
                council_district=4, 
                trash_pickup_day="Tuesday"
            ),
            service_history=[
                ServiceRequest(
                    request_date="2024-03-05",
                    case_number="SR-99812",
                    items=[
                        MunicipalService(
                            service_id="prm-111",
                            service_name="Parking Permit - Residential",
                            status="Active",
                        )
                    ],
                )
            ],
            civic_points=45,
            notification_preferences=NotificationPreferences(
                emergency_alerts=True, utility_outages=True, community_events=True
            ),
            property_profile=PropertyProfile(
                property_type="Single Family",
                lot_size="0.25 acres",
                historical_status=True,
                active_permits=["Fence-Repair-2024"],
            ),
            scheduled_inspections={},
        )