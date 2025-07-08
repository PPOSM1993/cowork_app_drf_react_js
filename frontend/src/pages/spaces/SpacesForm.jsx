import React, { useEffect, useState } from "react";
import { Sidebar, Header } from "../../index";
import { useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Swal from "sweetalert2";
import axios from "axios";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";

const SpacesForm = () => {
  const { t } = useTranslation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const navigate = useNavigate();
  const { id } = useParams();

  const [branches, setBranches] = useState([]);
  const [tags, setTags] = useState([]);
  const [amenities, setAmenities] = useState([]);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    type: "shared",
    capacity: 1,
    price_per_hour: "",
    price_per_day: "",
    price_per_month: "",
    branch_id: "",
    amenities_ids: [],
    tags_ids: [],
    max_simultaneous_reservations: 1,
    latitude: "",
    longitude: "",
    is_available: true,
    image: null,
    rules: "",
    cancellation_policy: "",
    notes: "",
    access_24_7: false,
    accessible_for_disabled: false,
    has_special_equipment: false,
  });

useEffect(() => {
  const fetchData = async () => {
    const token = localStorage.getItem("access_token");
    const headers = { Authorization: `Bearer ${token}` };

    const [branchRes, tagsRes, amenitiesRes] = await Promise.all([
      axios.get("http://localhost:8000/api/branches/", { headers }),
      axios.get("http://localhost:8000/api/spaces/tags/"),
      axios.get("http://localhost:8000/api/spaces/amenities/"),
    ]);

    setBranches(branchRes.data);
    setTags(tagsRes.data.results || []);
    setAmenities(amenitiesRes.data.results || []); // 👈 FIX AQUÍ
  };

  fetchData();
}, []);



  useEffect(() => {
    if (id) {
      const fetchSpace = async () => {
        try {
          const token = localStorage.getItem("access_token");
          const res = await axios.get(`http://localhost:8000/api/spaces/spaces/${id}/`, {
            headers: { Authorization: `Bearer ${token}` },
          });

          const data = res.data;
          setFormData({
            ...data,
            branch_id: data.branch?.id || "",
            amenities_ids: data.amenities?.map(a => a.id) || [],
            tags_ids: data.tags?.map(t => t.id) || [],
          });
        } catch (error) {
          Swal.fire("Error", "No se pudo cargar el espacio.", "error");
        }
      };
      fetchSpace();
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

  const handleMultiSelect = (e, name) => {
    const selected = Array.from(e.target.selectedOptions).map((opt) => Number(opt.value));
    setFormData((prev) => ({ ...prev, [name]: selected }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    const formToSend = new FormData();
    for (const key in formData) {
      const value = formData[key];
      if (Array.isArray(value)) {
        value.forEach((v) => formToSend.append(key, v));
      } else if (value !== null && value !== undefined) {
        formToSend.append(key, value);
      }
    }

    try {
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      };

      if (id) {
        await axios.put(`http://localhost:8000/api/spaces/spaces/${id}/`, formToSend, config);
        Swal.fire("Actualizado", "Espacio actualizado correctamente", "success");
      } else {
        await axios.post("http://localhost:8000/api/spaces/", formToSend, config);
        Swal.fire("Creado", "Espacio creado correctamente", "success");
      }

      navigate("/spaces");
    } catch (error) {
      Swal.fire("Error", "No se pudo guardar el espacio", "error");
    }
  };

  return (
    <div className="flex h-screen bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100">
      <Sidebar isOpen={isSidebarOpen} />
      <div className="flex-1 flex flex-col">
        <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        <main className="flex-1 overflow-y-auto p-6">
          <h1 className="text-2xl font-bold mb-6">
            {id ? t("Editar Espacio") : t("Crear Espacio")}
          </h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Campos de texto */}
            {[
              { label: "Nombre", name: "name" },
              { label: "Descripción", name: "description", textarea: true },
              { label: "Capacidad", name: "capacity", type: "number" },
              { label: "Precio por hora", name: "price_per_hour", type: "number" },
              { label: "Precio por día", name: "price_per_day", type: "number" },
              { label: "Precio por mes", name: "price_per_month", type: "number" },
              { label: "Latitud", name: "latitude" },
              { label: "Longitud", name: "longitude" },
              { label: "Notas", name: "notes", textarea: true },
              { label: "Reglas", name: "rules", textarea: true },
              { label: "Política de cancelación", name: "cancellation_policy", textarea: true },
            ].map(({ label, name, textarea, type }) => (
              <div key={name}>
                <label className="block font-medium">{label}</label>
                {textarea ? (
                  <textarea name={name} value={formData[name]} onChange={handleChange} className="input" />
                ) : (
                  <input
                    name={name}
                    type={type || "text"}
                    value={formData[name]}
                    onChange={handleChange}
                    className="input"
                  />
                )}
              </div>
            ))}

            {/* Tipo */}
            <div>
              <label className="block font-medium">Tipo de Espacio</label>
              <select name="type" value={formData.type} onChange={handleChange} className="input">
                <option value="shared">Espacio Compartido</option>
                <option value="private">Oficina Privada</option>
                <option value="meeting">Sala de Reuniones</option>
                <option value="event">Espacio para Eventos</option>
              </select>
            </div>

            {/* Branch */}
            <div>
              <label className="block font-medium">Sucursal</label>
              <select name="branch_id" value={formData.branch_id} onChange={handleChange} className="input">
                <option value="">Seleccione sucursal</option>
                {branches.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Tags */}
            <div>
              <label className="block font-medium">Etiquetas</label>
              <select multiple value={formData.tags_ids} onChange={(e) => handleMultiSelect(e, "tags_ids")} className="input">
                {tags.map((tag) => (
                  <option key={tag.id} value={tag.id}>
                    {tag.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Amenities */}
            <div>
              <label className="block font-medium">Amenidades</label>
              <select multiple value={formData.amenities_ids} onChange={(e) => handleMultiSelect(e, "amenities_ids")} className="input">
                {amenities.map((amenity) => (
                  <option key={amenity.id} value={amenity.id}>
                    {amenity.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Imagen */}
            <div>
              <label className="block font-medium">Imagen</label>
              <input type="file" name="image" onChange={handleChange} className="input" />
            </div>

            {/* Checkboxes */}
            {[
              { name: "is_available", label: "¿Disponible?" },
              { name: "access_24_7", label: "Acceso 24/7" },
              { name: "accessible_for_disabled", label: "Accesible para personas con discapacidad" },
              { name: "has_special_equipment", label: "Tiene equipamiento especial" },
            ].map(({ name, label }) => (
              <div className="flex items-center" key={name}>
                <input type="checkbox" name={name} checked={formData[name]} onChange={handleChange} className="mr-2" />
                <label className="font-medium">{label}</label>
              </div>
            ))}

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
                <span>{id ? "Actualizar" : "Crear"}</span>
              </button>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
};

export default SpacesForm;
