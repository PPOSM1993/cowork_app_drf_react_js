import React, { useEffect, useState } from "react";
import { Sidebar, Header, axiosInstance } from "../../index";
import { useNavigate, useParams } from "react-router-dom";
import Swal from "sweetalert2";
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
        // Carga JSON locales
        import("./json/regions.json").then((res) => setRegions(res.default));
        import("./json/cities.json").then((res) => setCities(res.default));
    }, []);

    useEffect(() => {
        if (id) {
            axiosInstance.get(`customers/${id}/`)
                .then((res) => setFormData(res.data))
                .catch(() => Swal.fire("Error", "No se pudo cargar el cliente.", "error"));
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

        try {
            if (id) {
                await axiosInstance.put(`customers/${id}/`, formData);
                Swal.fire("Cliente actualizado", "", "success").then(() => navigate("/customers"));
            } else {
                await axiosInstance.post("customers/", formData);
                Swal.fire("Cliente creado", "", "success").then(() => navigate("/customers"));
            }
        } catch {
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

                        <div>
                            <label>Tipo de Cliente</label>
                            <select name="customer_type" value={formData.customer_type} onChange={handleChange} className="input">
                                <option value="individual">Persona Natural</option>
                                <option value="company">Empresa</option>
                            </select>
                        </div>

                        {formData.customer_type === "company" ? (
                            <div>
                                <label>Nombre de la Empresa</label>
                                <input name="company_name" value={formData.company_name} onChange={handleChange} className="input" />
                            </div>
                        ) : (
                            <>
                                <div>
                                    <label>Nombre</label>
                                    <input name="first_name" value={formData.first_name} onChange={handleChange} className="input" />
                                </div>
                                <div>
                                    <label>Apellido</label>
                                    <input name="last_name" value={formData.last_name} onChange={handleChange} className="input" />
                                </div>
                            </>
                        )}

                        <div>
                            <label>RUT / Tax ID</label>
                            <input name="tax_id" value={formData.tax_id} onChange={handleChange} className="input" required />
                        </div>

                        <div>
                            <label>Correo Electrónico</label>
                            <input name="email" value={formData.email || ""} onChange={handleChange} className="input" />
                        </div>

                        <div>
                            <label>Teléfono</label>
                            <input name="phone" value={formData.phone || ""} onChange={handleChange} className="input" />
                        </div>

                        <div>
                            <label>Dirección</label>
                            <input name="address" value={formData.address || ""} onChange={handleChange} className="input" />
                        </div>

                        <div>
                            <label>Región</label>
                            <select name="region" value={formData.region || ""} onChange={handleChange} className="input">
                                <option value="">Seleccione región</option>
                                {regions.map((r) => (
                                    <option key={r.pk} value={r.pk}>{r.fields.name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label>Ciudad</label>
                            <select name="city" value={formData.city || ""} onChange={handleChange} className="input">
                                <option value="">Seleccione ciudad</option>
                                {cities
                                    .filter((c) => c.fields.region === parseInt(formData.region))
                                    .map((c) => (
                                        <option key={c.pk} value={c.pk}>{c.fields.name}</option>
                                    ))}
                            </select>
                        </div>

                        <div>
                            <label>Notas</label>
                            <textarea name="notes" value={formData.notes || ""} onChange={handleChange} className="input" />
                        </div>

                        <div className="flex items-center">
                            <input type="checkbox" name="is_active" checked={formData.is_active} onChange={handleChange} />
                            <label>¿Cliente activo?</label>
                        </div>

                        <div className="flex justify-end gap-4 mt-6">
                            <button type="button" onClick={() => navigate(-1)} className="bg-red-500 text-white px-4 py-2 rounded">
                                <ImCancelCircle /> Cancelar
                            </button>
                            <button type="submit" className="bg-yellow-400 text-black px-4 py-2 rounded">
                                <CiCirclePlus /> {id ? "Guardar Cambios" : "Crear Cliente"}
                            </button>
                        </div>

                    </form>
                </main>
            </div>
        </div>
    );
};

export default CustomersForm;
