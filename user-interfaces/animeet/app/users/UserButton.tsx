'use client'

import Link from 'next/link'
import React from 'react'
import UserCookies from './UserIdCookie'

interface Props {
    user_id: string
}

const UserButton = ({user_id}: Props) => {
  return (
    <>
        <Link href="/">
            <UserCookies user_id={user_id} />
        </Link>
    </>
  )
}

export default UserButton