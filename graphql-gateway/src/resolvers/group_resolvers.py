import requests
from ..config import GROUPS_SERVICE_URL

# Query Resolvers for Group
def resolve_health_check(_, info):
    response = requests.get(f"{GROUPS_SERVICE_URL}/health")
    return response.json()

def resolve_get_group_by_id(_, info, group_id):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups/{group_id}")
    if response.status_code == 200:
        group_data = response.json()
        return {
            "data": group_data["data"],
            "message": "Group retrieved successfully."
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve group.")
        return {
            "data": None,
            "message": error_message
        }

def resolve_list_groups(_, info):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups")
    if response.status_code == 200:
        groups_data = response.json()
        if "data" in groups_data:
            # Transform the list of groups to match the schema
            groups_list = [
                {
                    "group_id": group["group_id"],
                    "event_id": group["event_id"],
                    "name": group["name"],
                    "description": group["description"],
                    "max_capacity": int(group["max_capacity"]),
                    "slots_left": int(group["slots_left"])
                }
                for group in groups_data["data"]
            ]
            return {
                "data": groups_list,
                "message": "Groups retrieved successfully."
            }
        else:
            return {
                "data": [],
                "message": "No groups available."
            }
    else:
        error_message = response.json().get("message", "Failed to retrieve groups.")
        return {
            "data": None,
            "message": error_message
        }

# Mutation Resolvers for Group
# def resolve_create_group(_, info, name, max_capacity, description):
#     payload = {
#         "name": name,
#         "max_capacity": max_capacity,
#         "slots_left": max_capacity - 1,
#         "description": description
#     }
#     response = requests.post(f"{GROUPS_SERVICE_URL}/groups", json=payload)
#     if response.status_code == 201:
#         group_data = response.json()
#         return {
#             "message": "Group created successfully.",
#             "error": None,
#             "data": group_data["data"]
#         }
#     else:
#         error_message = response.json().get("message", "Failed to create group.")
#         return {
#             "message": "Failed to create group.",
#             "error": error_message,
#             "data": None
#         }

# attempt at fixing create group function    
# def resolve_new_group(_, info, event_id, user_id, name, max_capacity, description=None):
#     # Prepare the payload
#     payload = {
#         "event_id": event_id,
#         "user_id": user_id,
#         "name": name,
#         "max_capacity": max_capacity,
#         "description": description
#     }

#     try:
#         # Call the /groups endpoint with the new group data
#         response = requests.post(f"{GROUPS_SERVICE_URL}/groups", json=payload)

#         # Check if the response was successful
#         if response.status_code == 201:
#             group_data = response.json().get("data", {})
#             return {
#                 "message": "Group created successfully.",
#                 "error": None,
#                 "data": group_data
#             }
#         else:
#             error_message = response.json().get("message", "Unable to create group.")
#             return {
#                 "message": "Failed to create group.",
#                 "error": error_message,
#                 "data": None
#             }
#     except Exception as e:
#         # Handle any exceptions that occur during the request
#         return {
#             "message": "Failed to create group due to an exception.",
#             "error": str(e),
#             "data": None
#         }


def resolve_delete_group(_, info, group_id):
    response = requests.delete(f"{GROUPS_SERVICE_URL}/groups/{group_id}")
    if response.status_code == 200:
        return {
            "message": "Group deleted successfully.",
            "error": None,
            "data": {"group_id": group_id}
        }
    else:
        error_message = response.json().get("message", "Failed to delete group.")
        return {
            "message": "Failed to delete group.",
            "error": error_message,
            "data": None
        }

# Query Resolvers for GroupUser
def resolve_get_all_users_in_group(_, info, group_id):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups/{group_id}/users")
    if response.status_code == 200:
        users_data = response.json()
        if "data" in users_data:
            # Transform the list of users to match the GroupUser schema
            users_list = [
                {
                    "group_id": user["group_id"],
                    "user_id": user["user_id"],
                    "role": user["role"],
                    "date_joined": user["date_joined"],
                    "payment_status": user["payment_status"]
                }
                for user in users_data["data"]
            ]
            return {
                "data": users_list,
                "message": "Users retrieved successfully.",
                "error": None
            }
        else:
            return {
                "data": [],
                "message": "No users found in the group.",
                "error": None
            }
    else:
        error_message = response.json().get("message", "Failed to retrieve users.")
        return {
            "data": None,
            "message": error_message,
            "error": error_message
        }

def resolve_get_groups_by_event_id(_, info, event_id):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups?event_id={event_id}")
    if response.status_code == 200:
        groups_data = response.json()
        if "data" in groups_data:
            groups_list = [
                {
                    "group_id": group["group_id"],
                    "event_id": group["event_id"],
                    "name": group["name"],
                    "description": group["description"],
                    "max_capacity": int(group["max_capacity"]),
                    "slots_left": int(group["slots_left"])
                }
                for group in groups_data["data"]
            ]
            return {
                "data": groups_list,
                "message": "Groups retrieved successfully for the given event ID."
            }
        else:
            return {
                "data": [],
                "message": "No groups found for the given event ID."
            }
    else:
        error_message = response.json().get("message", "Failed to retrieve groups.")
        return {
            "data": None,
            "message": error_message
        }

def resolve_get_one_user_in_group(_, info, group_id, user_id):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups/{group_id}/users/{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        return {
            "data": user_data["data"],
            "message": "User retrieved successfully.",
            "error": None
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve user.")
        return {
            "data": None,
            "message": error_message,
            "error": error_message
        }

def resolve_get_all_group_users(_, info):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups/users")
    if response.status_code == 200:
        users_data = response.json()
        return {
            "data": users_data["data"],
            "message": "All group users retrieved successfully.",
            "error": None
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve all group users.")
        return {
            "data": None,
            "message": error_message,
            "error": error_message
        }

def resolve_get_all_groups_from_user(_, info, user_id):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups/users/{user_id}")
    if response.status_code == 200:
        groups_data = response.json()
        return {
            "message": "All groups for user retrieved successfully.",
            "error": None,
            "data": groups_data["data"]
        }
    else:
        error_message = groups_data.get("message", "Failed to retrieve all groups for user.")
        return {
            "data": None,
            "message": error_message,
            "error": error_message
        }
    
def resolve_get_payment_status_in_group(_, info, group_id, user_id):
    response = requests.get(f"{GROUPS_SERVICE_URL}/groups/{group_id}/users/{user_id}/payment-status")

    if response.status_code == 200:
        payment_data = response.json()
        return {
            "data": payment_data,
            "error": None,
            "message": "Payment status retrieved successfully." 
        }
        
    elif response.status_code == 404:
        return {
            "data": None,
            "message": "User not found in this group.",
            "error": "User not found in this group."
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve payment status.")
        return {
            "data": None,
            "message": error_message,
            "error": error_message
        }

def resolve_delete_user_from_group(_, info, group_id, user_id):
    response = requests.delete(f"{GROUPS_SERVICE_URL}/groups/{group_id}/users/{user_id}")
    if response.status_code == 200:
        return {
            "message": "User removed from group successfully.",
            "error": None,
            "data": {"group_id": group_id, "user_id": user_id}
        }
    else:
        error_message = response.json().get("message", "Failed to remove user from group.")
        return {
            "message": "Failed to remove user from group.",
            "error": error_message,
            "data": None
        }

def resolve_patch_group_user(_, info, group_id, user_id, payment_status=None, role=None):
    payload = {}
    if payment_status is not None:
        payload["payment_status"] = payment_status
    if role is not None:
        payload["role"] = role
    response = requests.patch(f"{GROUPS_SERVICE_URL}/groups/{group_id}/users/{user_id}", json=payload)
    if response.status_code == 200:
        updated_user_data = response.json()
        return {
            "message": "Group user updated successfully.",
            "error": None,
            "data": updated_user_data["data"]
        }
    else:
        error_message = response.json().get("message", "Failed to update group user.")
        return {
            "message": "Failed to update group user.",
            "error": error_message,
            "data": None
        }
