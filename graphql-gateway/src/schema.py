from ariadne import load_schema_from_path, make_executable_schema, ObjectType

# Import resolvers
from .resolvers.health_check_resolvers import resolve_health_check
from .resolvers.event_resolvers import (
    resolve_get_event,
    resolve_list_events,
    resolve_create_event,
    resolve_update_event_details,
    resolve_update_event_slots,
    resolve_delete_event
)
from .resolvers.payment_resolvers import (
    resolve_get_payment,
    resolve_list_payments,
    resolve_create_checkout_session,
    resolve_refund_payment,
    resolve_delete_payment,
    resolve_add_payment
)
from .resolvers.user_resolvers import resolve_get_user, resolve_list_users
from .resolvers.group_resolvers import (
    resolve_get_group_by_id,
    resolve_list_groups,
    resolve_delete_group,
    resolve_get_all_users_in_group,
    resolve_get_one_user_in_group,
    resolve_get_all_group_users,
    resolve_get_all_groups_from_user,
    resolve_get_payment_status_in_group,
    resolve_delete_user_from_group,
    resolve_patch_group_user,
    resolve_get_groups_by_event_id,
)
from .resolvers.notification_resolvers import resolve_publish_notification
from .resolvers.create_group_resolvers import resolve_create_group_composite
from .resolvers.join_group_resolvers import resolve_join_group_composite, resolve_leave_group
from .resolvers.make_a_payment_resolvers import resolve_make_a_payment

# Load schemas from .graphql files
type_defs = (
    load_schema_from_path("src/schema/health-check.graphql") +
    load_schema_from_path("src/schema/events.graphql") +
    load_schema_from_path("src/schema/payments.graphql") +
    load_schema_from_path("src/schema/group-user.graphql") +
    load_schema_from_path("src/schema/users.graphql") +
    load_schema_from_path("src/schema/groups.graphql") +
    load_schema_from_path("src/schema/notifications.graphql") +
    load_schema_from_path("src/schema/create-group.graphql") +
    load_schema_from_path("src/schema/join-group.graphql") +
    load_schema_from_path("src/schema/make-a-payment.graphql")
)

# Define Query type resolvers.
query = ObjectType("Query")
query.set_field("healthCheck", resolve_health_check)
query.set_field("getEvent", resolve_get_event)
query.set_field("listEvents", resolve_list_events)
query.set_field("getPayment", resolve_get_payment)
query.set_field("listPayments", resolve_list_payments)
query.set_field("getUser", resolve_get_user)
query.set_field("listUsers", resolve_list_users)
query.set_field("getGroup", resolve_get_group_by_id)
query.set_field("listGroups", resolve_list_groups)
query.set_field("getAllGroupUsers", resolve_get_all_group_users)
query.set_field("getAllUsersFromGroup", resolve_get_all_users_in_group)
query.set_field("getOneUserFromGroup", resolve_get_one_user_in_group)
query.set_field("getGroupsByEventId", resolve_get_groups_by_event_id)
query.set_field("getAllGroupsFromUser", resolve_get_all_groups_from_user)
query.set_field("getPaymentStatusInGroup", resolve_get_payment_status_in_group)

# Define Mutation type resolvers
mutation = ObjectType("Mutation")
mutation.set_field("createEvent", resolve_create_event)
mutation.set_field("updateEventDetails", resolve_update_event_details)
mutation.set_field("updateEventSlots", resolve_update_event_slots)
mutation.set_field("deleteEvent", resolve_delete_event)
mutation.set_field("createCheckoutSession", resolve_create_checkout_session)
mutation.set_field("refundPayment", resolve_refund_payment)
mutation.set_field("deletePayment", resolve_delete_payment)
mutation.set_field("addPayment", resolve_add_payment)
mutation.set_field("deleteGroup", resolve_delete_group)
mutation.set_field("removeUserFromGroup", resolve_delete_user_from_group)
mutation.set_field("updateUserInGroup", resolve_patch_group_user)
mutation.set_field("publishNotification", resolve_publish_notification)
mutation.set_field("createGroup", resolve_create_group_composite)
mutation.set_field("joinGroupComposite", resolve_join_group_composite)
mutation.set_field("leaveGroup", resolve_leave_group)
mutation.set_field("makeAPayment", resolve_make_a_payment)

# Make the executable schema
schema = make_executable_schema(type_defs, query, mutation)