import React from "react";
import MembersList from "./MembersList";
import getUserId from "@/app/users/getUserId";
import JoinGroupButton from "@/app/components/JoinGroupButton";
import LeaveGroupButton from "@/app/components/LeaveGroupButton";
import PurchaseTicketButton from "@/app/components/PurchaseTicketButton";
import { BASE_URL } from "@/app/constants";

interface Props {
  groupId: number;
  eventId: number;
}

async function getGroupUserRecord(groupId: number) {
  // call graphQL to get all groups based on eventId
  try {
    const res = await fetch(BASE_URL + "/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `
              query {
                getOneUserFromGroup(group_id: ${groupId}, user_id: ${await getUserId()}) {
                  message
                  data {
                    group_id
                    user_id
                    role
                    date_joined
                    payment_status
                  }
                  error
                }
              }
          `,
      }),
    });

    const userJson = await res.json();

    if (!userJson) {
      console.log("User json couldn't be retrieved");
      return null;
    }

    return userJson.data.getOneUserFromGroup.data;
  } catch (error) {
    console.log("Server error " + error);
    return null;
  }
}

const BottomPart = async ({ groupId, eventId }: Props) => {
  const user = await getGroupUserRecord(groupId);

  // check if user has joined the group before
  let userInGroup = false;
  if (user) {
    userInGroup = true;
  }

console.log(user);

  return (
    <div className="flex w-full">
      <MembersList groupId={groupId} />
      <div className="font-normal w-[22rem] ml-8 [&_*]:w-[22rem] flex flex-col gap-3">
        {userInGroup ? (
          <>
            {user.payment_status === 'paid' || <PurchaseTicketButton groupId={groupId} eventId={eventId} />}
            <LeaveGroupButton groupId={groupId} eventId={eventId} />
          </>
        ) : (
          <JoinGroupButton groupId={groupId} eventId={eventId} />
        )}
      </div>
    </div>
  );
};

export default BottomPart;
