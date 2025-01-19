"use client";
import Link from "next/link";
import React, { useState } from "react";

const NavBar = () => {
  const [imdenuOpen, setImdenuOpen] = useState(false);
  const toggleMenu = () => {
    setImdenuOpen(!imdenuOpen);
  };

  return (
    <>
      {/* Sidebar */}
      {imdenuOpen && (
        <div className="md:hidden m-0 fixed top-0 right-0 mx-2 z-[999] w-[250] h-screen bg-white shadow-md backdrop-blur-lg">
          <div
            onClick={toggleMenu}
            className="hover:bg-slate-100 w-full m-0  p-3  border-1 cursor-pointer"
          >
            <i className="fa fa-times fa-xl" aria-hidden="true"></i>
          </div>
          <Link
            href="/my-groups"
            className="block hover:bg-slate-100 w-full m-0 p-3"
          >
            My Groups
          </Link>
          <Link href="/" className="block hover:bg-slate-100 w-full m-0 p-3">
            Events
          </Link>
        </div>
      )}

      {/* Navbar */}
      <nav className="grid bg-slate-50 text-xl shadow-md py-2 md:grid-cols-[auto_1fr_1fr] md:justify-items-start w-full items-center justify-items-center grid-cols-1 ">
        {/* Logo */}
        <div className="px-14 text-2xl text-red-500 font-bold">
          <Link href="/">Animeet</Link>
        </div>
        {/* Sidebar Menu*/}
        <div className="p-2 md:hidden cursor-pointer">
          <i
            onClick={toggleMenu}
            className="fas fa-bars text-gray-700 text-2xl"
          ></i>
        </div>
        {/* Search */}
        <div className=" w-full md:col-span-1 col-span-2 px-2">
          <label className="input input-bordered flex items-center gap-2">
            <input type="text" className="grow" placeholder="Search" />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 opacity-70"
            >
              <path
                fillRule="evenodd"
                d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
                clipRule="evenodd"
              />
            </svg>
          </label>
        </div>
        {/* Links */}
        <div className="justify-self-end md:text-[16px] md:flex hidden">
          <Link href="/">Events</Link>
          <Link className="px-10" href="/my-groups">
            My Groups
          </Link>
        </div>
      </nav>
    </>
  );
};

export default NavBar;
