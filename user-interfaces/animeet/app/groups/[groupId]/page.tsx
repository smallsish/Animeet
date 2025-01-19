import React from "react";
import IndividualGroup from "./IndividualGroup";
import BottomPart from "./BottomPart";
import BackButton from "@/app/components/BackButton";
import getGroup from "@/app/fetches/getGroup";

const GroupPage = async ({
  params,
}: {
  params: Promise<{ groupId: string }>;
}) => {
  // get group id from url
  const groupIdRes = (await params).groupId;
  const groupId = parseInt(groupIdRes);

  // store the group details in a variable
  const groupRes = await getGroup(groupId);

  if (!groupRes) {
    return <p>Unable to retrieve group. Please try again later.</p>;
  }

  const group = groupRes.data.getGroup.data;

  // return frontend
  return (
    <>
      <BackButton link="/" />
      <div className="flex justify-center w-full pt-8 pb-12">
        <div className="flex flex-col">
          <span className="text-5xl font-bold">{group.name}</span>
          <IndividualGroup details={group.description} eventId={group.event_id} />
          <BottomPart groupId={groupId} eventId={group.event_id} />
        </div>
      </div>
    </>
  );
};

export default GroupPage;
