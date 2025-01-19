import React from "react";
import {Group} from '../types/Group'
import ViewGroupButton from "./ViewGroupButton";

interface Props {
  group: Group
}

const GroupCard = ({group}: Props) => {
console.log("gid" + group.group_id);
  return (
    <div className="card card-side bg-base-100 w-auto h-40 shadow-lg">
      <figure>
        <img
          className="w-full h-full object-cover object-center"
          src="https://i.redd.it/plqg3rt7xvw71.jpg"
          alt="Group image"
        />
      </figure>
      <div className="card-body py-2 px-5">
        <div className="membersContainer flex justify-end items-center">
          <img src="/personIcon.png" className="w-5 h-5 mr-1" />
          <span className="memberNumber text-base font-semibold text-appPurple">{group.max_capacity - group.slots_left}/{group.max_capacity}</span>
        </div>
        <h2 className="card-title text-lg">{group.name}</h2>
        <p className="text-sm">{group.description}</p>
        <div className="card-actions justify-end">
            <ViewGroupButton groupId={group.group_id}/>
        </div>
      </div>
    </div>
  );
};

export default GroupCard;
