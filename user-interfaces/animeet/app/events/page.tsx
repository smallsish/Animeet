import React from 'react'
import GroupContainer from '../groups/GroupContainer'
import IndividualEvent from './IndividualEvent'
import BackButton from '../components/BackButton'

const EventPage = () => {
  return (
    <>
      <BackButton link="/"/>
      <div className="flex justify-center w-full pt-8">
          <div className="flex flex-col">
              <span className="text-5xl font-bold">JJK Anime Expo</span>
              {/* <IndividualEvent /> */}
              {/* <GroupContainer /> */}
          </div>
      </div>
    </>
  )
}

export default EventPage