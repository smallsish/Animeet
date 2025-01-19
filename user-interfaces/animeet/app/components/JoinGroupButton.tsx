"use client";
import React from "react";
import getUserIdClient from "../users/getUserIdClient";
import { BASE_URL, BASE_URL_CLIENT } from "../constants";

interface Props {
  groupId: number;
  eventId: number;
}

async function joinGroup(groupId: number, eventId: number) {
  const userId = await getUserIdClient();

  if (!userId) {
    window.alert("Please login to join group.");
    return;
  }

  try {
    const res = await fetch(BASE_URL_CLIENT + "/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        query: `
                    mutation {
                        joinGroupComposite(user_id: ${userId}, group_id: ${groupId}, event_id: ${eventId}) {
                            message
                            error
                            data {
                                joined
                                group_id
                                user_id
                                role
                                status
                                members
                            }
                        }
                    }
                `,
      }),
    });

    const joinGroupJson = await res.json();
    console.log(joinGroupJson);
    const message = joinGroupJson.data.joinGroupComposite.message;
    const error = joinGroupJson.data.joinGroupComposite.error;

    window.alert(error || message);

    // refresh entire page
    window.location.reload();
  } catch (error) {
    console.error("Error joining group:", error);
  }
}

const JoinGroupButton = ({ groupId, eventId }: Props) => {
  return (
    <button
      className="btn btn-primary rounded-sm py-2 bg-appPurple border-0 text-appWhite font-normal"
      onClick={() => {
        joinGroup(groupId, eventId);
      }}
    >
      Join Group
    </button>
  );
};

export default JoinGroupButton;
