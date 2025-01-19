import requests
from ..config import (
    CREATE_GROUP_SERVICE_URL,
    JOIN_GROUP_SERVICE_URL,
    MAKE_A_PAYMENT_SERVICE_URL,
    PAYMENTS_SERVICE_URL,
    GROUPS_SERVICE_URL,
    NOTIFICATIONS_SERVICE_URL,
    EVENTS_SERVICE_URL,
    USERS_SERVICE_URL
)

# Define the mapping between service names and their health endpoints
SERVICE_URLS = {
    "createGroup": f"{CREATE_GROUP_SERVICE_URL}/health",
    "joinGroup": f"{JOIN_GROUP_SERVICE_URL}/health",
    "makePayment": f"{MAKE_A_PAYMENT_SERVICE_URL}/health",
    "payments": f"{PAYMENTS_SERVICE_URL}/health",
    "groups": f"{GROUPS_SERVICE_URL}/health",
    "notifications": f"{NOTIFICATIONS_SERVICE_URL}/health",
    "events": f"{EVENTS_SERVICE_URL}/health",
    "users": f"{USERS_SERVICE_URL}/health",
}

def resolve_health_check(_, info, service):
    # Retrieve the URL for the requested service
    url = SERVICE_URLS.get(service)
    if not url:
        # Return a response if the service is not recognized
        return {
            "service": service,
            "status": "unknown",
            "message": "Service not recognized"
        }

    # Perform the health check request
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return {
                "service": service,
                "status": "healthy",
                "message": response.json().get("message", "Service is healthy")
            }
        else:
            return {
                "service": service,
                "status": "unhealthy",
                "message": response.json().get("message", "Service is not healthy")
            }
    except requests.RequestException as e:
        # Handle exceptions if the service is unreachable or any other error occurs
        return {
            "service": service,
            "status": "unreachable",
            "message": str(e)
        }
