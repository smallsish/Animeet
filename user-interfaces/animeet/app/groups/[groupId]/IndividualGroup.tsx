import React from "react";
import { Group } from "../../types/Group";
import DetailsCard from "../../components/DetailsCard";
import getEvent from "@/app/fetches/getEvent";

interface Props {
  details: string;
  eventId: number;
}

const IndividualGroup = async ({ details, eventId }: Props) => {
  // Get event details based on event id (returns res.json())
  const eventRes = await getEvent(eventId);

  // Handle error calling
  if (!eventRes) {
    return <p>Unable to retrieve event. Please try again later</p>;
  }

  // Handle success
  const eventDetails = eventRes.data.getEvent.data;

  return (
    <div className="flex flex-col sm:flex-row items-center">
      <div className="card bg-base-100 w-[32rem] h-80 shadow-lg">
        <figure className="rounded-box w-full h-full">
          <img
            src="https://preview.redd.it/new-jujutsu-kaisen-illustration-for-juju-fest-2024-event-v0-bxbbid4ci00d1.jpeg?width=1080&crop=smart&auto=webp&s=0d0f5932ae7660b2373982c3e9e483e86067db05"
            alt="jjk event"
            className="w-full h-full object-cover object-center"
          />
        </figure>
      </div>
      <DetailsCard
        details={details}
        date={eventDetails.time}
        location={eventDetails.venue}
        price={eventDetails.entry_fee}
      />
    </div>
  );
};

export default IndividualGroup;
