'use client'
import Link from 'next/link';
import React from 'react'

interface Props {
    groupId: number;
}

const ViewGroupButton = ({groupId}: Props) => {
    return (
        <Link href={`/groups/${groupId}`}>
            <button className="btn btn-primary rounded-sm py-2 bg-appPurple border-0 text-appWhite font-normal">
                View Group
            </button>
        </Link>
    )
}

export default ViewGroupButton
