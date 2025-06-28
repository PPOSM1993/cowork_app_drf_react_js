import React, { useEffect, useState } from "react";
import { Sidebar, Header } from "../../index";
import { useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Swal from "sweetalert2";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";
import axios from "axios";
import { FaSave } from "react-icons/fa";

const BranchesForm = () => {
  const { t } = useTranslation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const navigate = useNavigate();
  const { id } = useParams();

  const [regions, setRegions] = useState([]);
  const [cities, setCities] = useState([]);
  const [previewImage, setPreviewImage] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    address: "",
    email: "",
    region_id: "",
    city_id: "",
    phone: "",
    image: null,
  });

  useEffect(() => {
    axios.get("/data/regionesData.json").then(res => setRegions(res.data));
    axios.get("/data/ciudadesData.json").then(res => setCities(res.data));
  }, []);

  useEffect(() => {
    if (id) {
      const fetchBranches = async () => {
        try {
          const token = localStorage.getItem("access_token");
          const res = await axios.get(`http://localhost:8000/api/branches/edit/${id}/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          setFormData(res.data);
          if (res.data.image) {
            setPreviewImage(`http://localhost:8000${res.data.image}`);
          }
        } catch (error) {
          console.error("Error al cargar Sucursal:", error);
          Swal.fire("Error", "No se pudo cargar la Sucursal.", "error");
        }
      };
      fetchBranches();
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFormData(prev => ({ ...prev, image: file }));
    if (file) {
      setPreviewImage(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");
      const formDataToSend = new FormData();

      // Asegura que las claves coincidan con lo que espera DRF
      formDataToSend.append("name", formData.name);
      formDataToSend.append("address", formData.address);
      formDataToSend.append("email", formData.email);
      formDataToSend.append("phone", formData.phone);
      formDataToSend.append("region_id", formData.region_id);
      formDataToSend.append("city_id", formData.city_id);

      if (formData.image) {
        formDataToSend.append("image", formData.image);
      }

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      };

      if (id) {
        await axios.put(`http://localhost:8000/api/branches/edit/${id}/`, formDataToSend, config);
      } else {
        await axios.post(`http://localhost:8000/api/branches/create/`, formDataToSend, config);
      }

      Swal.fire({
        title: "Éxito",
        text: `Sucursal ${id ? "actualizada" : "registrada"} correctamente.`,
        icon: "success",
      }).then(() => navigate("/branches"));
    } catch (error) {
      const errorMsg = error.response?.data?.email?.[0] || "Error al guardar.";
      Swal.fire("Error", errorMsg, "error");
    }
  };


  return (
    <div className="flex h-screen bg-white text-gray-800 dark:bg-[#121212] dark:text-gray-100 transition-colors duration-300">
      <Sidebar isOpen={isSidebarOpen} />
      <div className="flex-1 flex flex-col">
        <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        <main className="flex-1 overflow-y-auto p-6">
          <h1 className="text-2xl font-bold mb-6">{t("title_branches")}</h1>

          <form onSubmit={handleSubmit} className="bg-white dark:bg-[#121212] p-6 rounded-lg shadow space-y-4">
            <div>
              <label className="block mb-1 font-medium">{t("name_spaces")}</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder={t("placeholer_spaces")}
                className="w-full p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-[#121212]"
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">{t("address_spaces")}</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
                required
                placeholder={t("placeholder_address")}
                className="w-full p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-[#121212]"
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">{t("email_branches")}</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder={t("placeholder_email_branches")}
                className="w-full p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-[#121212]"
              />
            </div>

            <div>
              <label className="block mb-1 font-medium">{t("phone")}</label>
              <input
                type="text"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder={t("placeholder_phone")}
                className="w-full p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-[#121212]"
              />
            </div>

            <div>
              <label className="block text-sm font-medium">Región</label>
              <select
                name="region"
                value={formData.region || ""}
                onChange={handleChange}
                className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-[#121212]"
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
                className="w-full mt-1 p-2 border rounded-md border-none focus:outline-none focus:ring-2 focus:ring-yellow-500 dark:bg-[#121212]"
              >
                <option value="">Seleccione una ciudad</option>
                {cities
                  .filter((c) => c.fields.region === parseInt(formData.region))
                  .map((c) => (
                    <option key={c.pk} value={c.pk}>
                      {c.fields.name}
                    </option>
                  ))}
              </select>
            </div>

            <div>
              <label className="block mb-1 font-medium">{t("upload_image")}</label>
              <input
                type="file"
                name="image"
                accept="image/*"
                onChange={handleImageChange}
                className="w-full p-2 bg-white border border-none rounded-md dark:bg-[#121212] dark:text-white focus:ring-yellow-500"
              />
              {previewImage && (
                <div className="mt-2">
                  <p className="text-sm text-gray-500">{t("preview")}</p>
                  <img
                    src={previewImage}
                    alt="Vista previa"
                    className="w-48 h-auto mt-1 rounded shadow border border-gray-300"
                  />
                </div>
              )}
            </div>

            <div className="flex justify-end gap-4">
              <button
                type="button"
                onClick={() => navigate(-1)}
                className="px-4 py-2 bg-red-500 p-4 rounded hover:bg-red-600 text-white flex items-center gap-2"
              >
                <ImCancelCircle />
                {t("cancel")}
              </button>

              <button
                type="submit"
                className="px-4 py-2 bg-yellow-400 p-4 rounded hover:bg-yellow-500 text-black flex items-center gap-2"
              >
                <CiCirclePlus />
                {t("save_branch")}
              </button>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
};

export default BranchesForm;
