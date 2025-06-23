import React, { useState } from "react";
import { Sidebar, Header } from "../../index"; // Asegúrate que estos estén bien importados
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Swal from "sweetalert2";

const SpacesForm = () => {

  const [formData, setFormData] = useState({
    name: "",
    description: "",
  })

  const { t } = useTranslation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...form, [e.target.name]: e.target.value });
  };


  return (
    <>
      <div className="flex h-screen bg-white text-gray-800 dark:bg-[#121212] dark:text-gray-100 transition-colors duration-300">
        <Sidebar isOpen={isSidebarOpen} />
        <div className="flex-1 flex flex-col">
          <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

          <main className="flex-1 overflow-y-auto p-6">
            <h1 className="text-2xl font-bold mb-6">{t("button_create_space")}</h1>

            <form
              className="bg-white dark:bg-[#121212] p-6 rounded-lg shadow space-y-4"
            >
              <div>
                <label className="block mb-1 font-medium">{t("name_spaces")}</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-100 dark:bg-[#121212]"
                  required
                  placeholder={t("placeholer_spaces")}
                />
              </div>

              <div>
                <label className="block mb-1 font-medium">{t("title_description")}</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-100 dark:bg-[#121212]"
                  rows="4"
                  placeholder="Descripción de la categoría"
                ></textarea>


              </div>

              <div className="flex justify-end gap-4">
                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  className="px-4 py-2 rounded bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500 transition"
                >
                  {t("cancel")}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded bg-yellow-400 text-black hover:bg-yellow-500 transition font-semibold"
                >
                  {t("save")}
                </button>
              </div>
            </form>
          </main>
        </div>
      </div>
    </>
  );
};

export default SpacesForm;