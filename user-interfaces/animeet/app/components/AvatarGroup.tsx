import React from "react";
import { BASE_URL } from "../constants";

interface Props {
  event_id: number;
}

interface Group {
  group_id: number;
  event_id: number;
  name: string;
  current_pax: number;
  capacity: number;
  description: string;
}

const AvatarGroup = async (props: Props) => {
  let groups: Group[] = [];

  try {

    const res = await fetch(BASE_URL + "/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `
                query {
                  getGroupsByEventId(event_id: ${props.event_id}) {
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

    const data = await res.json();
    groups = data?.data.getGroupsByEventId.data || [];
    // groups = data?.data || [];
  } catch (e) {
    console.log(e);
  }

  return (
    <div className="avatar-group -space-x-2 rtl:space-x-reverse">
      {/* <div className="avatar border-2">
        <div className="w-6 ">
          <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
        </div>
      </div> */}
      {groups.slice(0, 3).map((group) => (
        <div className="avatar placeholder border-2">
          <div className="bg-neutral text-neutral-content w-6">
            <span className="text-xs">{group.name.charAt(0)}</span>
          </div>
        </div>
      ))}
      {groups.length > 3 && (
        <div className="avatar placeholder border-2">
          <div className="bg-neutral text-neutral-content w-6">
            <span className="text-xs">+{groups.length - 3}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default AvatarGroup;
