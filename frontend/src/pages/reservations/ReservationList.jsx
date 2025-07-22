import React, { useState } from "react";
import { Header, Sidebar, ReservationsTable, CustomersForm } from "../../index";
import { motion } from "framer-motion";
import { useTranslation } from 'react-i18next';

const ReservationsList = () => {
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
            <h1 className="text-2xl font-bold">{t('reservations_list')}</h1>
          </div>

          {/* Tabla con listado de espacios */}
          <ReservationsTable />

          {/* Formulario para crear o editar espacio */}
          {showForm && (
            <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-start pt-20 z-50">
              <div className="bg-white dark:bg-[#1f1f1f] p-6 rounded-sm shadow-md w-full max-w-xl relative">
                <button
                  onClick={() => setShowForm(false)}
                  className="absolute top-2 right-3 text-gray-600 dark:text-gray-300 hover:text-red-500 text-lg"
                >
                  ×
                </button>
                <CustomersForm onClose={() => setShowForm(false)} />
              </div>
            </div>
          )}
        </motion.main>
      </div>
    </div>
  );
};

export default ReservationsList;
