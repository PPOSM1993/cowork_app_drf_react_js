import React, { useEffect, useState } from "react";
import { Sidebar, Header } from "../../index";
import { useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Swal from "sweetalert2";
import axios from "axios";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";

const BranchesForm = () => {
  const { t } = useTranslation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const navigate = useNavigate();
  const { id } = useParams();

  const [regions, setRegions] = useState([]);
  const [cities, setCities] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    address: "",
    region: "",
    city: "",
    phone: "",
    email: "",
    image: null,
    is_active: true,
    opening_hours: "",
    latitude: "",
    longitude: "",
    notes: "",
  });

  useEffect(() => {
    axios.get("/data/regionesData.json").then((res) => setRegions(res.data));
    axios.get("/data/ciudadesData.json").then((res) => setCities(res.data));
  }, []);

  useEffect(() => {
    if (id) {
      const fetchBranch = async () => {
        try {
          const token = localStorage.getItem("access_token");
          const res = await axios.get(`http://localhost:8000/api/branches/edit/${id}/`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          setFormData(res.data);
        } catch (error) {
          console.error("Error al cargar sucursal:", error);
          Swal.fire("Error", "No se pudo cargar la sucursal.", "error");
        }
      };
      fetchBranch();
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value, type, checked, files } = e.target;
    if (type === "checkbox") {
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else if (type === "file") {
      setFormData((prev) => ({ ...prev, [name]: files[0] }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    const formToSend = new FormData();
    for (const key in formData) {
      if (formData[key] !== null) {
        formToSend.append(key, formData[key]);
      }
    }

    try {
      if (id) {
        await axios.put(
          `http://localhost:8000/api/branches/edit/${id}/`,
          formToSend,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
      } else {
        await axios.post(
          "http://localhost:8000/api/branches/create/",
          formToSend,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
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
    <div className="flex h-screen bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100">
      <Sidebar isOpen={isSidebarOpen} />
      <div className="flex-1 flex flex-col">
        <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

        <main className="flex-1 overflow-y-auto p-6">
          <h1 className="text-2xl font-bold mb-6">{t("title_branches")}</h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Name */}
            <div>
              <label className="block font-medium">{t("name_spaces")}</label>
              <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="input"
                required
              />
            </div>

            {/* Address */}
            <div>
              <label className="block font-medium">{t("address_spaces")}</label>
              <input
                name="address"
                value={formData.address}
                onChange={handleChange}
                className="input"
                required
              />
            </div>

            {/* Region */}
            <div>
              <label className="block font-medium">Región</label>
              <select name="region" value={formData.region || ""} onChange={handleChange} className="input">
                <option value="">Seleccione región</option>
                {regions.map((r) => (
                  <option key={r.pk} value={r.pk}>
                    {r.fields.name}
                  </option>
                ))}
              </select>
            </div>

            {/* City */}
            <div>
              <label className="block font-medium">Ciudad</label>
              <select name="city" value={formData.city || ""} onChange={handleChange} className="input">
                <option value="">Seleccione ciudad</option>
                {cities
                  .filter((c) => c.fields.region === parseInt(formData.region))
                  .map((c) => (
                    <option key={c.pk} value={c.pk}>
                      {c.fields.name}
                    </option>
                  ))}
              </select>
            </div>

            {/* Phone */}
            <div>
              <label className="block font-medium">Teléfono</label>
              <input name="phone" value={formData.phone} onChange={handleChange} className="input" />
            </div>

            {/* Email */}
            <div>
              <label className="block font-medium">Email</label>
              <input type="email" name="email" value={formData.email} onChange={handleChange} className="input" />
            </div>

            {/* Imagen */}
            <div>
              <label className="block font-medium">Imagen</label>
              <input type="file" name="image" onChange={handleChange} className="input" />
            </div>

            {/* Opening Hours */}
            <div>
              <label className="block font-medium">Horario de apertura</label>
              <input
                name="opening_hours"
                value={formData.opening_hours}
                onChange={handleChange}
                className="input"
              />
            </div>

            {/* Latitud */}
            <div>
              <label className="block font-medium">Latitud</label>
              <input name="latitude" value={formData.latitude} onChange={handleChange} className="input" />
            </div>

            {/* Longitud */}
            <div>
              <label className="block font-medium">Longitud</label>
              <input name="longitude" value={formData.longitude} onChange={handleChange} className="input" />
            </div>

            {/* Notas */}
            <div>
              <label className="block font-medium">Notas</label>
              <textarea name="notes" value={formData.notes} onChange={handleChange} className="input" />
            </div>

            {/* Activo */}
            <div className="flex items-center">
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
                className="mr-2"
              />
              <label className="font-medium">¿Sucursal activa?</label>
            </div>

            {/* Botones */}
            <div className="flex justify-end gap-4 mt-6">
              <button
                type="button"
                onClick={() => navigate(-1)}
                className="bg-red-500 text-white px-4 py-2 rounded flex items-center space-x-2"
              >
                <ImCancelCircle />
                <span>{t("cancel")}</span>
              </button>
              <button
                type="submit"
                className="bg-yellow-400 text-black px-4 py-2 rounded flex items-center space-x-2"
              >
                <CiCirclePlus />
                <span>{t("save_branch")}</span>
              </button>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
};

export default BranchesForm;
