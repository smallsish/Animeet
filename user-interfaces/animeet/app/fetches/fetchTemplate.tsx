import { BASE_URL } from "../constants";

export default async function callFetch(query: string) {
    try {
      const res = await fetch(BASE_URL + "/graphql", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query
        }),
      });

      const resJson = await res.json();
      return resJson;
    } catch (e) {
        console.log(e);
        return null;
    }
}