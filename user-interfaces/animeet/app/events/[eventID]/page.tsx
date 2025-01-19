import React from "react";
import GroupContainer from "../../groups/GroupContainer";
import IndividualEvent from "../IndividualEvent";
import BackButton from "../../components/BackButton";
import CreateGroupButton from "../../components/CreateGroupButton";
import getEvent from "@/app/fetches/getEvent";
import { BASE_URL } from "@/app/constants";



async function getGroupsByEvent(event_id: number) {
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
              getGroupsByEventId(event_id: ${event_id}) {
                message
                data {
                  group_id
                  event_id
                  name
                  description
                  max_capacity
                  slots_left
                }
              }
            }
        `,
      }),
    });
    const resJson = await res.json();
    return resJson;
  } catch (error) {
    console.log(error);
    return null;
  }
}

const page = async ({ params }: { params: Promise<{ eventID: string }> }) => {
  // get event id from url
  const eventIdRes = (await params).eventID;
  const eventId = parseInt(eventIdRes);

  // Get event details based on event id (returns res.json())
  const eventRes = await getEvent(eventId);

  // Handle error calling
  if (!eventRes) {
    return <p>Unable to retrieve event. Please try again later</p>;
  }

  // Handle success
  const eventDetails = eventRes.data.getEvent.data;

  // Get all groups from event
  const groupRes = await getGroupsByEvent(eventId);
  if (!groupRes) {
    return <p>Unable to retrieve groups. Please try again later</p>;
  }

  let groupList = groupRes.data.getGroupsByEventId.data;
  // if there is no group inside event, use an empty array
  if (groupList === null) {
    groupList = [];
  }

  return (
    <>
      <BackButton link="/" />
      <div className="flex justify-center w-full pt-8 pb-12">
        <div className="flex flex-col">
          <span className="text-5xl font-bold">{eventDetails.event_name}</span>
          <span className="text-2xl">Tickets remaining: {eventDetails.slots_left}/{eventDetails.capacity}</span>
          <IndividualEvent
            description={eventDetails.description}
            date={eventDetails.time}
            venue={eventDetails.venue}
            entry_fee={eventDetails.entry_fee}
          />
          <div className="CreateGroupButtonWrapper flex justify-between mr-5">
            <span className="text-3xl font-bold">Groups</span>
            <CreateGroupButton eventId={eventId} />
          </div>
          <GroupContainer groups={groupList} />
        </div>
      </div>
    </>
  );
};

export default page;
