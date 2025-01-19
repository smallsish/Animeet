"use client";
import { BASE_URL, BASE_URL_CLIENT } from "@/app/constants";
import getUserIdClient from "@/app/users/getUserIdClient";
import { redirect, useParams, useRouter } from "next/navigation";
import React, { useState } from "react";

const page = () => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [maxCapacity, setMaxCapacity] = useState("");
  const { eventID } = useParams();
  const router = useRouter(); // Initialize useRouter

  const createGroup = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const userId = await getUserIdClient();

    if (!userId) {
      window.alert("Please login to create a group.");
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
                  createGroup(
                    event_id: ${eventID}
                    user_id: ${userId}
                    name: "${name}"
                    max_capacity: ${maxCapacity}
                    description: "${description}"
                  ) {
                    message
                    data {
                      group_data {
                        group_id
                        name
                        description
                        max_capacity
                        slots_left
                        event_id
                      }
                      event_data {
                        event_id
                        event_name
                        description
                        time
                        venue
                        entry_fee
                        capacity
                        slots_left
                      }
                    }
                    error
                  }
                }
              `,
        }),
      });

      const resJson = await res.json();
      console.log(resJson);

      if (!resJson.data.createGroup.data) {
        const message = resJson.data.createGroup.message;
        const error = resJson.data.createGroup.error;
        window.alert(error || message);
        return;
      }
      
      const message = resJson.data.createGroup.message;
      const error = resJson.data.createGroup.error;
      const groupId = resJson.data.createGroup.data.group_data.group_id;
      window.alert(error || message);

      if (message == "Group created.") {
        router.push("/groups/" + groupId);
      } else {
        return;
      }
    } catch (error) {
      window.alert(
        "Unable to create a group at this moment. Please try again later."
      );
      console.error("Error creating group:", error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>)  => {
    const inputValue = e.target.value;

    // Allow only letters, numbers, comma, !, ., ?, and spaces
    const filteredValue = inputValue.replace(/[^A-Za-z0-9,!.? ]/g, "");

    setName(filteredValue); // Update state with the filtered value
  };

  const handleChange2 = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const inputValue = e.target.value;

    // Allow only letters, numbers, comma, !, ., ?, and spaces
    const filteredValue = inputValue.replace(/[^A-Za-z0-9,!.? ]/g, "");

    setDescription(filteredValue); // Update state with the filtered value
  };

  return (
    <div className="flex flex-col items-center my-8">
      {/* <h1 className="text-3xl font-bold my-4">Create a Group</h1> */}
      <form onSubmit={createGroup}>
        <div className="card shadow-md  w-[700px] max-w-full pt-4">
          <h1 className="text-3xl font-bold mt-4 px-8">Create a Group</h1>
          <div className="card-body py-4">
            <h2 className="card-title text-slate-500">Group Name</h2>
            <label className="input input-bordered flex items-center gap-2 mb-4">
              <input
                required
                type="text"
                maxLength={32}
                value={name}
                onChange={handleChange}
                className="grow text-md"
                placeholder="Enter group name"
              />
            </label>

            <h2 className="card-title text-slate-500">Capacity</h2>
            <label className="input input-bordered flex items-center gap-2 mb-4">
              <input
                required
                type="number"
                min={1}
                max={50}
                onChange={(e) => setMaxCapacity(e.target.value)}
                pattern="^[1-9][0-9]{0,2}$"
                className="grow text-md"
                placeholder="Enter group capacity"
              />
            </label>

            <h2 className="card-title text-slate-500">Description</h2>
            <textarea
              required
              maxLength={64}
              value={description}
              onChange={handleChange2}
              className="textarea textarea-bordered text-[16px] mb-4  "
              placeholder="Enter group description"
            ></textarea>

            <button
              type="submit"
              className="btn btn-primary rounded-sm my-4 bg-appPurple border-0 text-appWhite font-normal"
            >
              Submit
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default page;
