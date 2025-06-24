import React, { useState } from "react";
import { Header, Sidebar, BranchesTable } from "../../index";
import { motion } from "framer-motion";
import { useTranslation } from 'react-i18next';

const BranchesList = () => {
  const { t } = useTranslation();

  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [showForm, setShowForm] = useState(false); // Controla el formulario

  return (
    <div className="flex h-screen bg-white text-gray-800 dark:bg-[#121212] dark:text-gray-100 transition-colors duration-300">
      <Sidebar isOpen={isSidebarOpen} />
      <div className="flex-1 flex flex-col">
        <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

        <motion.main
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex-1 overflow-y-auto p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold">{t('branches')}</h1>
          </div>
          <BranchesTable />
        </motion.main>
      </div>
    </div>
  );
};

export default BranchesList;
