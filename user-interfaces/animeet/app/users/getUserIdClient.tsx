'use client';

import { getCookie, hasCookie } from 'cookies-next';

export default async function getUserIdClient() {
    if (!(await hasCookie('user_id'))) {
        return "1000";
    }

    const user = await getCookie('user_id');
    return user as string;
}