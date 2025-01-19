import Link from "next/link";
import React from "react";

const page = async () => {
  return (
    // Header
    <main className="md:px-14 px-4">
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-70px)]">
        <h1 className="text-3xl font-bold ">
          Your payment failed!
        </h1>
        <p className="mt-4 text-md">
        Please try again later.
        </p>
        <Link href="/">
        <button className="btn btn-primary rounded-sm py-2 mt-6 bg-appPurple border-0 text-appWhite font-normal">
                Return to Home
            </button>
        </Link>
      </div>
    </main>
  );
};

export default page;
