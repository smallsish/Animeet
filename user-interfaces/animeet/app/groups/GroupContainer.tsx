import React from "react";
import GroupCard from "../components/GroupCard";
import { Group } from "@/app/types/Group";
import getUserId from "../users/getUserId";

interface Props {
  groups: Group[]
}

const GroupContainer = async ({groups}: Props) => {
  return (
    <>
      <div className="flex">
        <div className="pt-5 grid sm:grid-cols-[1fr,1fr] gap-6 w-full">
          {groups.length === 0 && (
            <p>No groups found. Please check back later</p>
          )}
          {groups.map((indivGroup: Group) => (
            <GroupCard key={indivGroup.group_id} group={indivGroup} /> 
          ))}
        </div>
      </div>
    </>
  );
};

export default GroupContainer;
