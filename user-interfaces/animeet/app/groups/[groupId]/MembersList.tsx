import React from "react";
import GroupMemberComponent from "../../components/GroupMemberComponent";
import { BASE_URL } from "@/app/constants";

interface Props {
  groupId: number;
}
const MembersList = async ({ groupId }: Props) => {
  // fetch groups/id/users/ json from backend
  async function getGroupUserEntries() {
    try {
      const res = await fetch(BASE_URL + "/graphql", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: `
              query {
                getAllUsersFromGroup(group_id: ${groupId}) {
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
          `
        }),
      });
      
      const groupUserRes = await res.json();
      const groupUser = groupUserRes.data.getAllUsersFromGroup.data;
console.log(groupUser);
      return groupUser;

    } catch (error) {
      console.log(error);
      return [];
    }
  }

  // fetch groups/id/users/ json from backend
  async function getUser(userId: string) {
    try {
      const res = await fetch(BASE_URL + "/graphql", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: `
              query {
                getUser(user_id: ${userId}) {
                  data {
                    user_id
                    username
                    email
                    dob
                  }
                  error {
                    message
                  }
                }
              }
          `
        }),
      });
      
      const userRes = await res.json();
      const user = userRes.data.getUser.data;
      return user;
    } catch (error) {
      console.log(error);
      return null;
    }
  }

  // store the user ids in a variable
  const groupUserIds = await getGroupUserEntries();

  let users = await Promise.all(
    groupUserIds.map(
      async (groupUserId: {
        date_joined: string;
        group_id: number;
        payment_status: string;
        role: string;
        user_id: string;
      }) => {
        let user = await getUser(groupUserId.user_id);

        // if user is null, return 
        if (!user) {
          console.log("User " + groupUserId.user_id + " couldn't be fetched.");
          return;
        }
        user["role"] = groupUserId.role;
        user["paymentStatus"] = groupUserId.payment_status;
        return user;
      }
    )
  );

  return (
    <div className="w-[32rem]">
      <span className="font-bold text-2xl my-6">Members</span>
      <div className="grid grid-cols-5 gap-2">
        {
        users.map(
          (currentUser: {
            user_id: string;
            username: string;
            email:string;
            dob: string;
            role: string;
            paymentStatus: string;
          }) => {
            // if user is null, return 
            if (!currentUser) {
              console.log("User couldn't be mapped.");
              return;
            }

            return (
              <GroupMemberComponent
                key={currentUser.user_id}
                username={currentUser.username}
                role={currentUser.role}
                paymentStatus={currentUser.paymentStatus}
              />
            );
          }
        )}
      </div>
    </div>
  );
};

export default MembersList;
