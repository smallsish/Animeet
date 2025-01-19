import callFetch from "./fetchTemplate";

// fetch group json from backend
export default async function getGroup(group_id: number) {
  const query = `
              query {
                getGroup(group_id: ${group_id}) {
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
  
          `;

  const resJson = await callFetch(query);

  // Handle [Call error] and [Call success w/ error output]
  if (!resJson || !resJson.data.getGroup.data) {
    console.log(resJson?.data.getGroup.message);
    return null;
  }
  return resJson;
}
