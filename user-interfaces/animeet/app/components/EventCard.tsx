import React from "react";
import AvatarGroup from "./AvatarGroup";

interface Props {
  event_id: number;
  name: string;
  dayOfMonth: number;
  month: string;
  location: string;
}

// Events: Name, Date, Location | Groups: Number of Groups
const EventCard = (props: Props) => {
  return (
    <div className="card bg-base-100 2xl:w-56 w-full shadow-xl hover:cursor-pointer hover:scale-110">
      <figure className="relative h-32">
        <img
          src="https://onecms-res.cloudinary.com/image/upload/s--nAlfP5b6--/f_auto,q_auto/c_fill,g_auto,h_622,w_830/v1/mediacorp/tdy/image/2023/11/26/20231126_llt_afa-7.jpg?itok=a870K5K-"
          alt="Shoes"
        />
        <div className="absolute top-2 right-2 flex justify-end text-appPurple text-sm font-bold">
          <div className="bg-white/80 rounded-[10px] h-auto w-auto px-1">
            <p className="mx-2 mt-2 text-center font-bold text-[18px]">
              {props.dayOfMonth}
            </p>
            <p className="mx-2 text-center font-medium text-[10px]">{props.month}</p>
          </div>
        </div>
      </figure>
      <div className="card-body px-3 py-2 gap-0">
        <h2 className="card-title text-[16px]">
          {props.name}
          {/* <div className="badge badge-secondary">NEW</div> */}
        </h2>
        {/* <p>If a dog chews shoes whose shoes does he choose?</p>
         */}
        <AvatarGroup event_id={props.event_id}/>
        <div className="card-actions justify-start">
          <p className="text-[13px] font-bold text-slate-600 pt-1">
            Location: {props.location}
          </p>
          {/* <div className="badge badge-outline">Fashion</div> */}
          {/* <div className="badge badge-outline">Products</div> */}
        </div>
      </div>
    </div>
  );
};

export default EventCard;
