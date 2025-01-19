import React from "react";
import UserButton from "./UserButton";
import { BASE_URL } from "../constants";

async function getUsersList() {
  // const url = process.env.graphql_service_url_internal || "http://graphql:5000";
  // call graphQL to get list of users
  try {
    const res = await fetch(BASE_URL + "/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query:
          "query { listUsers { data { user_id username } error { message } }}",
      }),
    });

    const resJson = await res.json();
    return resJson;
  } catch (e) {
    console.log(e);
    return null;
  }
}
const UserPage = async () => {
  const usersListRes = await getUsersList();

  // if fetch returns an error
  if (!usersListRes) {
    return <p>Could not fetch users.</p>;
  }

  const usersList = usersListRes.data.listUsers.data; // to get the users array

  if (!usersList) {
    return <p>{usersListRes.data.listUsers.data}</p>;
  }

  // for each user in usersList, return a button
  return (
    <div className="flex flex-col gap-4 p-8">
      {usersList.map((user: { user_id: string; username: string }) => (
        <UserButton key={user.user_id} user_id={user.user_id} />
      ))}
    </div>
  );
};

export default UserPage;
