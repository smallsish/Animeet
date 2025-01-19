import callFetch from "./fetchTemplate";

// fetch group json from backend
export default async function getEvent(event_id: number) {
  const query = `
             query {
              getEvent(event_id: ${event_id}) {
                message
                error
                data {
                  event_id
                  event_name
                  venue
                  entry_fee
                  capacity
                  slots_left
                  description
                  time
                }
              }
            }
  
          `;

  const resJson = await callFetch(query);

  // Handle [Call error] and [Call success w/ error output]
  if (!resJson || resJson.data.getEvent.error) {
    console.log(resJson?.data.getEvent.error);
    return null;
  }
  return resJson;
}
