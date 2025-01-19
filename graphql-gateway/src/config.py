# config.py
import os

# if os.environ.get('stage') == 'production-k8s':
#     GROUPS_SERVICE_URL = os.environ.get('groups_service_url_internal')
#     USERS_SERVICE_URL = os.environ.get('users_service_url_internal')
#     EVENTS_SERVICE_URL = os.environ.get('events_service_url_internal')
#     NOTIFICATIONS_SERVICE_URL = os.environ.get('notifications_service_url_internal')
#     PAYMENTS_SERVICE_URL = os.environ.get('payment_service_url_internal')
#     CREATE_GROUP_SERVICE_URL = os.environ.get('create_group_service_url_internal')
#     JOIN_GROUP_SERVICE_URL = os.environ.get('join_group_service_url_internal')
#     MAKE_A_PAYMENT_SERVICE_URL = os.environ.get('make_a_payment_service_url_internal')
# else:
#     GROUPS_SERVICE_URL = 'http://localhost:5000/groups'
#     USERS_SERVICE_URL = 'http://localhost:5000/users'
#     EVENTS_SERVICE_URL = 'http://localhost:5000/events'
#     NOTIFICATIONS_SERVICE_URL = 'http://localhost:5000/notifications'
#     PAYMENTS_SERVICE_URL = 'http://localhost:5000/payments'
#     CREATE_GROUP_SERVICE_URL = 'http://localhost:5000/create-group'
#     JOIN_GROUP_SERVICE_URL = 'http://localhost:5000/join-group'
#     MAKE_A_PAYMENT_SERVICE_URL = 'http://localhost:5000/make-a-payment'

if os.environ.get('stage') == 'production-k8s':
    GROUPS_SERVICE_URL = os.environ.get('groups_service_url_internal')
    USERS_SERVICE_URL = os.environ.get('users_service_url_internal')
    EVENTS_SERVICE_URL = os.environ.get('events_service_url_internal')
    NOTIFICATIONS_SERVICE_URL = os.environ.get('notifications_service_url_internal')
    PAYMENTS_SERVICE_URL = os.environ.get('payment_service_url_internal')
    CREATE_GROUP_SERVICE_URL = os.environ.get('create_group_service_url_internal')
    JOIN_GROUP_SERVICE_URL = os.environ.get('join_group_service_url_internal')
    MAKE_A_PAYMENT_SERVICE_URL = os.environ.get('make_a_payment_service_url_internal')
else:
    GROUPS_SERVICE_URL = 'http://groups:5000'  # service name:port
    USERS_SERVICE_URL = 'http://users:5000'  # service name:port
    EVENTS_SERVICE_URL = 'http://events:5000'  # service name:port
    PAYMENTS_SERVICE_URL = 'http://payments:5000'  # service name:port
    CREATE_GROUP_SERVICE_URL = 'http://create-group:5000'  # service name:port
    JOIN_GROUP_SERVICE_URL = 'http://join-group:5000'  # service name:port
    MAKE_A_PAYMENT_SERVICE_URL = 'http://make-a-payment:5000'
    NOTIFICATIONS_SERVICE_URL = 'http://notifications:5000'  # service name:port