import requests
from ..config import USERS_SERVICE_URL

# Query Resolvers
def resolve_health_check(_, info):
    response = requests.get(f"{USERS_SERVICE_URL}/health")
    return response.json()

def resolve_get_user(_, info, user_id):
    response = requests.get(f"{USERS_SERVICE_URL}/users/{user_id}")
    if response.status_code == 200:
        data = response.json()
        user_data = data.get("user", {})
        return {
            "data": {
                "user_id": user_data.get("id"),
                "username": user_data.get("username"),
                "email": data.get("email"),
                "dob": data.get("dateOfBirth")
            },
            "error": None
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve user.")
        return {
            "data": None,
            "error": {"message": error_message}
        } 

def resolve_list_users(_, info):
    response = requests.get(f"{USERS_SERVICE_URL}/users")
    if response.status_code == 200:
        users_data = response.json()
        return {
            "data": [
                {
                    "user_id": user.get("id"),
                    "username": user.get("username")
                }
                for user in users_data
            ],
            "error": None
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve users.")
        return {
            "data": None,
            "error": {"message": error_message}
        }