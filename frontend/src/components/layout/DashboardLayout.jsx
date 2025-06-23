import React, { useState } from "react";
import { Header, Sidebar } from "../../index";
import { Outlet } from "react-router-dom";
import { motion } from 'framer-motion';

const DashboardLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <>
      <div className="flex h-screen bg-white text-gray-800 dark:bg-[#121212] dark:text-gray-100 transition-colors duration-300">
        <Sidebar isOpen={isSidebarOpen} />
        <div className="flex-1 flex flex-col">
          <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
          <motion.main
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex-1 overflow-y-auto p-6"
          >
            <Outlet />
          </motion.main>
        </div>
      </div>
    </>
  );
}

export default DashboardLayout;
