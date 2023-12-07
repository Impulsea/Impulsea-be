from services.healthcheck import HealthCheck
from services.activities import Activities
from services.db.address import AddressService
from db.session import session_maker


def healthcheck() -> HealthCheck:
    return HealthCheck()


def get_activities_service() -> Activities:
    address_service = AddressService(
        session=session_maker()
    )
    return Activities(
        address_service=address_service
    )
