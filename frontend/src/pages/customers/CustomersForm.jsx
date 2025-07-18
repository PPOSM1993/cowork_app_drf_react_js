import React, { useEffect, useState } from "react";
import { Sidebar, Header } from "../../index";
import { useNavigate, useParams } from "react-router-dom";
import Swal from "sweetalert2";
import axios from "axios";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";

const CustomersForm = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const navigate = useNavigate();
    const { id } = useParams();

    const [regions, setRegions] = useState([]);
    const [cities, setCities] = useState([]);

    const [formData, setFormData] = useState({
        customer_type: "individual",
        first_name: "",
        last_name: "",
        company_name: "",
        tax_id: "",
        business_activity: "",
        email: "",
        phone: "",
        address: "",
        region: "",
        city: "",
        country: "Chile",
        website: "",
        notes: "",
        is_active: true,
    });

    useEffect(() => {
        axios.get("/src/pages/customers/json/regions.json").then((res) => setRegions(res.data));
        axios.get("/src/pages/customers/json/cities.json").then((res) => setCities(res.data));
    }, []);

    useEffect(() => {
        if (id) {
            const fetchCustomer = async () => {
                const token = localStorage.getItem("access_token");
                try {
                    const res = await axios.get(`http://localhost:8000/api/customers/${id}/`, {
                        headers: { Authorization: `Bearer ${token}` },
                    });
                    setFormData(res.data);
                } catch (error) {
                    Swal.fire("Error", "No se pudo cargar el cliente.", "error");
                }
            };
            fetchCustomer();
        }
    }, [id]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("access_token");

        try {
            if (id) {
                await axios.put(`http://localhost:8000/api/customers/${id}/`, formData, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                Swal.fire("Cliente actualizado", "", "success").then(() => navigate("/customers"));
            } else {
                await axios.post(`http://localhost:8000/api/customers/`, formData, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                Swal.fire("Cliente creado", "", "success").then(() => navigate("/customers"));
            }
        } catch (error) {
            Swal.fire("Error", "Revisa los datos ingresados", "error");
        }
    };

    return (
        <div className="flex h-screen bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100">
            <Sidebar isOpen={isSidebarOpen} />
            <div className="flex-1 flex flex-col">
                <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
                <main className="flex-1 overflow-y-auto p-6">
                    <h1 className="text-2xl font-bold mb-6">{id ? "Editar Cliente" : "Crear Cliente"}</h1>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Tipo */}
                        <div>
                            <label className="block font-medium">Tipo de Cliente</label>
                            <select
                                name="customer_type"
                                value={formData.customer_type}
                                onChange={handleChange}
                                className="input"
                            >
                                <option value="individual">Persona Natural</option>
                                <option value="company">Empresa</option>
                            </select>
                        </div>

                        {/* Campos comunes */}
                        {formData.customer_type === "company" ? (
                            <div>
                                <label className="block font-medium">Nombre de la Empresa</label>
                                <input
                                    type="text"
                                    name="company_name"
                                    value={formData.company_name}
                                    onChange={handleChange}
                                    className="input"
                                />
                            </div>
                        ) : (
                            <>
                                <div>
                                    <label className="block font-medium">Nombre</label>
                                    <input
                                        type="text"
                                        name="first_name"
                                        value={formData.first_name}
                                        onChange={handleChange}
                                        className="input"
                                    />
                                </div>
                                <div>
                                    <label className="block font-medium">Apellido</label>
                                    <input
                                        type="text"
                                        name="last_name"
                                        value={formData.last_name}
                                        onChange={handleChange}
                                        className="input"
                                    />
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block font-medium">RUT / Tax ID</label>
                            <input
                                type="text"
                                name="tax_id"
                                value={formData.tax_id}
                                onChange={handleChange}
                                className="input"
                                required
                            />
                        </div>

                        <div>
                            <label className="block font-medium">Giro / Actividad</label>
                            <input
                                type="text"
                                name="business_activity"
                                value={formData.business_activity || ""}
                                onChange={handleChange}
                                className="input"
                            />
                        </div>

                        <div>
                            <label className="block font-medium">Correo Electrónico</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email || ""}
                                onChange={handleChange}
                                className="input"
                            />
                        </div>

                        <div>
                            <label className="block font-medium">Teléfono</label>
                            <input
                                type="text"
                                name="phone"
                                value={formData.phone || ""}
                                onChange={handleChange}
                                className="input"
                            />
                        </div>

                        <div>
                            <label className="block font-medium">Dirección</label>
                            <input
                                type="text"
                                name="address"
                                value={formData.address || ""}
                                onChange={handleChange}
                                className="input"
                            />
                        </div>

                        {/* Región */}
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

                        {/* Ciudad */}
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
                        <div>
                            <label className="block font-medium">Sitio Web</label>
                            <input
                                type="url"
                                name="website"
                                value={formData.website || ""}
                                onChange={handleChange}
                                className="input"
                            />
                        </div>

                        <div>
                            <label className="block font-medium">Notas</label>
                            <textarea
                                name="notes"
                                value={formData.notes || ""}
                                onChange={handleChange}
                                className="input"
                            />
                        </div>

                        <div className="flex items-center">
                            <input
                                type="checkbox"
                                name="is_active"
                                checked={formData.is_active}
                                onChange={handleChange}
                                className="mr-2"
                            />
                            <label className="font-medium">¿Cliente activo?</label>
                        </div>

                        {/* Botones */}
                        <div className="flex justify-end gap-4 mt-6">
                            <button
                                type="button"
                                onClick={() => navigate(-1)}
                                className="bg-red-500 text-white px-4 py-2 rounded flex items-center space-x-2"
                            >
                                <ImCancelCircle />
                                <span>Cancelar</span>
                            </button>
                            <button
                                type="submit"
                                className="bg-yellow-400 text-black px-4 py-2 rounded flex items-center space-x-2"
                            >
                                <CiCirclePlus />
                                <span>{id ? "Guardar Cambios" : "Crear Cliente"}</span>
                            </button>
                        </div>
                    </form>
                </main>
            </div>
        </div>
    );
};

export default CustomersForm;
