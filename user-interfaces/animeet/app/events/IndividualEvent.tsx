import React from "react";
import DetailsCard from "../components/DetailsCard";

interface Props {
  description: string,
  date: string,
  venue: string,
  entry_fee: number,
}

const IndividualEvent = ({description, date, venue, entry_fee}: Props) => {
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
        details={description}
        date={date}
        location={venue}
        price={entry_fee}
      />
    </div>
  );
};

export default IndividualEvent;
