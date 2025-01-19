import React from 'react'

interface Props {
    details: string,
    date: string,
    location: string,
    price: number 
}

const DetailsCard = ({details, date, location, price}: Props) => {
  return (
    <div className="card bg-base-100 w-[32rem] h-80 shadow-lg m-5 sm:w-96">
        <div className="card-body py-2 px-5 border-b-2">
            <h2 className="card-title">Description</h2>
            <p>
                {details}
            </p>
        </div>
        <div className="card-body py-2 px-5 flex flex-col text-base justify-center">
            <div className="eventDate flex">
                <img src="/calendar.png" className="w-5 h-5 mr-3"></img>
                <span>{date}</span>
            </div>  

            <div className="eventLocation flex">
                <img src="/location.png" className="w-5 h-5 mr-3"></img>
                <span>{location}</span>
            </div>

            <div className="eventPrice flex">
                <img src="/price.png" className="w-5 h-5 mr-3"></img>
                <span>{price}</span>
            </div>
        </div>

    </div>
  )
}

export default DetailsCard