import React from "react";
import GroupContainer from "../groups/GroupContainer";
import getUserId from "../users/getUserId";
import { BASE_URL } from "../constants";

async function getAllGroupsFromUser(userId: string) {
  try {
    const res = await fetch(BASE_URL + "/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `
            query {
              getAllGroupsFromUser(user_id: ${userId}) {
                data {
                  group_id
                  event_id
                  name
                  description
                  max_capacity
                  slots_left
                }
                message
                error
              }
            }
        `,
      }),
    });
    const resJson = await res.json();
    return resJson;
  } catch (error) {
    console.log("Server error:", error);
    return null;
  }
}

const page = async () => {
  // will default to 1000 if userId not intialized
  const userId = await getUserId();

  // fetch json from graphQL
  const groupJson = await getAllGroupsFromUser(userId);

  if (!groupJson) {
    console.log("Failed to fetch");
    return <p>An error occured in retrieving groups. Please try again later</p>;
  }

  const groups = groupJson.data.getAllGroupsFromUser.data;

  // If group list is null, show error
  if (!groups) {
    try {
      return <p>{groupJson.data.getAllGroupsFromUser.message}</p>;
    } catch (error) {
      console.log(error);
      return;
    }
  }

  return (
    // Header
    <main className="md:px-14 px-4">
      <h1 className="pt-5 text-3xl font-bold col-span-2">My Groups</h1>
      <GroupContainer groups={groups} />
    </main>
  );
};

export default page;
