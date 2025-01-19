import { notFound } from "next/navigation";
import EventCard from "./components/EventCard";
import Link from "next/link";
import { BASE_URL } from "./constants";

interface Event {
  event_id: number;
  event_name: string;
  venue: string;
  entry_fee: number;
  time: string;
  description: string;
  capacity: number;
  slots_left: number;
}

export default async function Home() {
  let events: Event[];
  // GET Events
  try {
    const res = await fetch(BASE_URL + "/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `
            query {
              listEvents {
                message
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
        `,
      }),
    });
    const data = await res.json();
    events = data.data.listEvents.data;
    // events = data.data.events;
  } catch (e) {
    events = [];
  }

  console.log(events);

  return (
    <main className="md:px-14 px-4">
      {/* Section header */}
      <h1 className="pt-5 pb-2 text-3xl font-bold">Events</h1>

      {/* Subheader */}
      <h2 className="pb-2 text-xl font-semibold text-slate-500">
        Featured events
      </h2>

      {/* Cards */}
      {events.length === 0 && <p>No events found. Please check back later</p>}
      <div className="sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4 grid grid-cols-1 w-full">
        {events.map((event) => (
          <Link href={`/events/${event.event_id}`}>
            <EventCard
              key={event.event_id}
              event_id={event.event_id}
              name={event.event_name}
              dayOfMonth={new Date(event.time).getUTCDate()}
              month={new Date(event.time)
                .toLocaleString("en-US", { month: "short" })
                .toUpperCase()}
              location={event.venue}
            />
          </Link>
        ))}
      </div>

      {/* Subheader */}
      <h2 className="pt-5 pb-2 text-xl font-semibold text-slate-500">
        Events $30 and under{" "}
      </h2>

      {/* Cards */}
      {(events.length === 0 ||
        events.filter((event) => event.entry_fee <= 30).length === 0) && (
        <p>No events found. Please check back later</p>
      )}
      <div className="sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4 grid grid-cols-1 w-full">
        {events
          .filter((event) => event.entry_fee <= 30)
          .map((event) => (
            <Link href={`/events/${event.event_id}`}>
              <EventCard
                key={event.event_id}
                event_id={event.event_id}
                name={event.event_name}
                dayOfMonth={new Date(event.time).getUTCDate()}
                month={new Date(event.time)
                  .toLocaleString("en-US", { month: "short" })
                  .toUpperCase()}
                location={event.venue}
              />
            </Link>
          ))}
      </div>
    </main>
  );
}
