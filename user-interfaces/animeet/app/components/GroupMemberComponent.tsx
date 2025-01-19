import React from "react";

interface Props {
  username: string;
  role: string;
  paymentStatus: string;
}

const GroupMemberComponent = ({ username, role, paymentStatus }: Props) => {
  let color = paymentStatus == "unpaid" ? "text-pink-500" : "text-green-500";

  return (
    <div className="flex flex-col w-auto items-center">
      <img
        src="https://i.pinimg.com/736x/37/3e/af/373eaf6124c2ac96d56096cb5b66f9be.jpg"
        className="rounded-full w-16 h-16 object-cover object-center"
      ></img>
      <span className="font-bold ">{username}</span>
      <span className="text-gray-500 text-sm">
        {role[0].toUpperCase() + role.substring(1).toLowerCase()}
      </span>
      <span className={`${color} text-sm`}>{paymentStatus}</span>
    </div>
  );
};

export default GroupMemberComponent;
