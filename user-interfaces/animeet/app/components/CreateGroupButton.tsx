"use client";
import Link from "next/link";
import React from "react";

interface Props {
  eventId: number;
}

// TODO: If creategroup page is pushed, change the link
const CreateGroupButton = ({ eventId }: Props) => {
  return (
    <Link href={`/events/${eventId}/create-group`}>
      <button className="btn btn-primary rounded-lg py-2 bg-appWhite text-appPurple font-normal border-appPurple hover:bg-appPurple hover:text-appWhite">
        + Create Group
      </button>
    </Link>
  );
};

export default CreateGroupButton;
