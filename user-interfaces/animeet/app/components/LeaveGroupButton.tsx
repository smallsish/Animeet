'use client'
import React from 'react'
import getUserIdClient from '../users/getUserIdClient';
import { BASE_URL, BASE_URL_CLIENT } from '../constants';
interface Props {
    groupId: number,
    eventId: number
}

async function leaveGroup(groupId: number, eventId: number) {
    const userId = await getUserIdClient();

    if (!userId) {
        window.alert("Could not find user session. Please try logging in again.");
        return;
    }

    try {
      const res = await fetch(BASE_URL_CLIENT + "/graphql", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          query: `
              mutation {
                leaveGroup(user_id: ${userId}, group_id: ${groupId}, event_id: ${eventId}) {
                    message
                    error
                    data {
                    group_id
                    user_id
                    members
                    }
                }
            }
          `
        }),
      });
    
      const leaveGroupJson = await res.json();
      const message = leaveGroupJson.data.leaveGroup.message;
      const error = leaveGroupJson.data.leaveGroup.error;
     
      window.alert(error || message);

      // refresh entire page
      window.location.reload();
    } catch (e) {
      console.error(e);
      return;
    }
    
}

const LeaveGroupButton = ({groupId, eventId}: Props) => {
    return (
        <button className="btn btn-primary rounded-sm py-2 bg-appRed border-0 text-appWhite font-normal" onClick={() => {leaveGroup(groupId, eventId)}}>
            Leave Group
        </button>
    )
}

export default LeaveGroupButton