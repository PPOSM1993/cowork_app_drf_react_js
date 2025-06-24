import React, { useState } from "react";
import { Sidebar, Header } from "../../index"; // Asegúrate que estos estén bien importados
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Swal from "sweetalert2";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";

const BranchesForm = () => {



  const { t } = useTranslation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [regions, setRegions] = useState([]);
  const [cities, setCities] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    address: "",
    email: "",
    region: "",
    city: ""
  })
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
            <h1 className="text-2xl font-bold mb-6">{t("title_branches")}</h1>

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
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-100 dark:bg-[#121212]"
                  required
                  placeholder={t("placeholer_spaces")}
                />
              </div>


              <div>
                <label className="block mb-1 font-medium">{t("address_spaces")}</label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-100 dark:bg-[#121212]"
                  required
                  placeholder={t("placeholder_address")}
                />
              </div>


              <div>
                <label className="block mb-1 font-medium">{t("email_branches")}</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-100 dark:bg-[#121212]"
                  required
                  placeholder={t("placeholder_email_branches")}
                />
              </div>

              {/* Región y ciudad */}
              <div>
                <label className="block text-sm font-medium">Región</label>
                <select
                  name="region"
                  value={formData.region ?? ""}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-100 dark:bg-[#121212]"
                >
                  <option value="">Seleccione una región</option>
                  {regions.map((r) => (
                    <option key={r.pk} value={r.pk}>
                      {r.fields.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium">Ciudad</label>
                <select
                  name="city"
                  value={formData.city || ""}
                  onChange={handleChange}
                  className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-100 dark:bg-[#121212]"
                >
                  <option value="">Seleccione una ciudad</option>
                  {cities
                    .filter(c => c.fields.region === parseInt(formData.region))
                    .map(c => (
                      <option key={c.pk} value={c.pk}>
                        {c.fields.name}
                      </option>
                    ))}
                </select>
              </div>

              <div className="flex justify-end gap-4">
                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  className="px-4 py-2 bg-red-500 p-4 rounded hover:bg-red-500 text-black cursor-pointer transition flex items-center space-x-2"
                >
                  <ImCancelCircle />
                  {t("cancel")}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-yellow-400 p-4 rounded hover:bg-yellow-500 text-black cursor-pointer transition flex items-center space-x-2"
                >
                  <CiCirclePlus />
                  <span>
                    {t("save_branch")}
                  </span>
                </button>
              </div>
            </form>
          </main>
        </div>
      </div>
    </>
  );
};

export default BranchesForm;