'use client'

import { setCookie } from 'cookies-next';

interface Props {
    user_id: string
}

export default function UserCookies({user_id}: Props) {
  const handleSetCookie = () => {
    setCookie('user_id', user_id, { maxAge: 60 * 60 * 24 }); // Cookie valid for 1 day
  };

  return (
    <button className='btn btn-primary w-32' onClick={handleSetCookie}>User {user_id}</button>
  );
}
