import Image from 'next/image';
import { UserCircle } from 'lucide-react';
import Link from 'next/link';


export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50  bg-white shadow-md">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between h-16">
        <div className="flex items-center">
          <Link href="/" className="flex-shrink-0 flex items-center">
            <div className="flex-shrink-0 flex items-center">
                <Image
                    src="/assets/images/samay.png"
                    alt="SAMAY"
                    width={55}
                    height={40}
                    className="rounded-lg p-2 rounded-full"
                />
              <span className="text-xl font-bold text-gray-800">SAMAY</span>
            </div>
          </Link>
          <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
            <Link href="/" className="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
              Home
            </Link>
            {/* Add more nav items as needed */}
          </div>
        </div>
        <div className="flex items-center">
          {/* Add any right-side nav items here */}
          <UserCircle size={32} />
         
        </div>
      </div>
    </div>
  </nav>
  );
} 


