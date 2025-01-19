import { getCookie, hasCookie } from 'cookies-next';
import { cookies } from 'next/headers';

export default async function getUserId() {
    if (!(await hasCookie('user_id', { cookies }))) {
        return "1000";
    }

    const user = await getCookie('user_id', { cookies });
    return user as string;
}

