'use client'
import React from 'react'
import getUserIdClient from '../users/getUserIdClient';
import { BASE_URL, BASE_URL_CLIENT } from '../constants';

interface Props {
    groupId: number;
    eventId: number;
}

async function makePayment(groupId: number, eventId: number) {
    // get the user's userId from the cookie
    const userId = await getUserIdClient();

    // check if user is logged in by checking if the cookie is absent
    if (!userId) {
        window.alert("Please login to join group.");
        return;
    }

    try {
        // send a request to the createPayment composite service to get the stripe url
        const res = await fetch(BASE_URL_CLIENT + "/graphql", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify({
                query: `
                    mutation {
                        makeAPayment(user_id: ${userId}, event_id: ${eventId}, group_id: ${groupId}) {
                            status
                            url
                            event_name
                            price
                            message
                            error
                        }
                    }
                `
            }),
          });
        
          const makePaymentJson = await res.json();
          
          if (!makePaymentJson) {
            window.alert("Couldn't get Json for make payment");
          }

          const error = makePaymentJson.data.makeAPayment.error;

          if (error) {
            window.alert(error);
            return;
          }

          // get payment url from stripe
          const stripeUrl = makePaymentJson.data.makeAPayment.url;
          if (!stripeUrl) {
            window.alert("We're sorry, but this event is sold out.");
            return;
          }

          //Open a new tab and redirect the user to the stripe payment page
          window.open(stripeUrl, "_blank");

          // refresh entire page
          window.location.reload();

    } catch (error) {
        console.error(error);
        window.alert("Couldn't relocate to the payment page.");
    }
}


const PurchaseTicketButton = ({groupId, eventId}: Props) => {
    return (
        <button className="btn btn-primary rounded-sm py-2 bg-appPurple border-0 text-appWhite font-normal" onClick={() => {makePayment(groupId, eventId)}}>
            Make Payment
        </button>
    )
}

export default PurchaseTicketButton