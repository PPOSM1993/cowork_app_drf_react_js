import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Swal from "sweetalert2";
import { Sidebar, Header, axiosInstance } from "../../index";
import { useTranslation } from "react-i18next";
import { CiCirclePlus } from "react-icons/ci";
import { ImCancelCircle } from "react-icons/im";
const ReservationsForm = () => {
    const navigate = useNavigate();
    const { id } = useParams(); // Si es edición
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const { t } = useTranslation();
    const [formData, setFormData] = useState({
        customer: "",
        space: "",
        start_datetime: "",
        end_datetime: "",
        status: "pending",
        payment_status: "unpaid",
        payment_method: "",
        reservation_type: "hourly",
        total_price: 0,
        discount_amount: 0,
        tax_amount: 0.19,
        billing_reference: "",
        notes: "",
        internal_notes: ""
    });

    const [customers, setCustomers] = useState([]);
    const [spaces, setSpaces] = useState([]);

    useEffect(() => {
        fetchCustomers();
        fetchSpaces();
        if (id) fetchReservation();
    }, [id]);

    const fetchCustomers = async () => {
        const res = await axiosInstance.get("/customers/");
        setCustomers(res.data.results || res.data); // Ajusta según tu paginación
    };

    const fetchSpaces = async () => {
        const res = await axiosInstance.get("/spaces/");
        setSpaces(res.data.results || res.data);
    };

    const fetchReservation = async () => {
        const res = await axiosInstance.get(`/reservations/${id}/`);
        setFormData(res.data);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (id) {
                await axiosInstance.put(`/reservations/${id}/`, formData);
                Swal.fire("Reservación actualizada", "", "success");
            } else {
                await axiosInstance.post("/reservations/", formData);
                Swal.fire("Reservación creada", "", "success");
            }
            navigate("/reservations");
        } catch (error) {
            console.error("Error:", error);
            Swal.fire("Error", "Revisa los datos ingresados", "error");
        }
    };

    return (
        <div className="flex h-screen bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100">
            <Sidebar isOpen={isSidebarOpen} />
            <div className="flex-1 flex flex-col">
                <Header toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
                <main className="flex-1 overflow-y-auto p-6">
                    <h2 className="text-xl font-bold mb-4">{id ? "Editar" : "Nueva"} Reservación</h2>
                    <form onSubmit={handleSubmit} className="space-y-4">

                        <div>
                            <label className="block font-medium">Cliente</label>
                            {/* Cliente */}
                            <select
                                name="customer_id"
                                value={formData.customer_id || ''}
                                onChange={handleChange}
                                className="input"
                                required
                            >
                                <option value="">Seleccione Cliente</option>
                                {customers.map((c) => (
                                    <option key={c.id} value={c.id}>
                                        {c.first_name} {c.last_name}
                                    </option>
                                ))}
                            </select>

                        </div>

                        <div>
                            <label className="block font-medium">Espacio</label>
                            {/* Espacio */}
                            <select name="space" value={formData.space} onChange={handleChange} required
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input">
                                <option value="">Selecciona un espacio</option>
                                {spaces.map(s => (
                                    <option key={s.id} value={s.id}>{s.name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block font-medium">Fecha de inicio</label>
                            {/* Fechas */}
                            <input type="datetime-local" name="start_datetime" value={formData.start_datetime || ""} onChange={handleChange} required
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input" />
                        </div>

                        <div>
                            <label className="block font-medium">Fecha Termino</label>
                            <input type="datetime-local" name="end_datetime" value={formData.end_datetime || ""} onChange={handleChange} required
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input" />
                        </div>

                        <div>
                            <label className="block font-medium">Estado</label>

                            {/* Estado y pagos */}
                            <select name="status" value={formData.status} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input">
                                <option value="pending">Pendiente</option>
                                <option value="confirmed">Confirmada</option>
                                <option value="cancelled">Cancelada</option>
                                <option value="completed">Completada</option>
                                <option value="no_show">No Asistió</option>
                            </select>
                        </div>

                        <div>
                            <label className="block font-medium">Estado Pago</label>

                            <select name="payment_status" value={formData.payment_status} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input">
                                <option value="unpaid">No Pagada</option>
                                <option value="paid">Pagada</option>
                                <option value="refunded">Reembolsada</option>
                            </select>
                        </div>

                        <div>
                            <label className="block font-medium">Medio de Pago</label>
                            <select name="payment_method" value={formData.payment_method || ""} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input">
                                <option value="">Método de Pago</option>
                                <option value="credit_card">Tarjeta Crédito</option>
                                <option value="debit_card">Tarjeta Débito</option>
                                <option value="cash">Efectivo</option>
                                <option value="bank_transfer">Transferencia</option>
                                <option value="paypal">PayPal</option>
                                <option value="other">Otro</option>
                            </select>
                        </div>

                        <div>
                            <label className="block font-medium">Monto</label>
                            {/* Montos */}
                            <input type="number" name="total_price" placeholder="Total" value={formData.total_price} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input" />
                        </div>

                        <div>
                            <label className="block font-medium">Descuento</label>
                            <input type="number" name="discount_amount" placeholder="Descuento" value={formData.discount_amount} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input" />
                        </div>

                        <div>
                            <label className="block font-medium">Impuesto</label>
                            <input type="number" name="tax_amount" placeholder="Impuesto" value={formData.tax_amount} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input" />
                        </div>

                        <div>
                            <label className="block font-medium">Referencias de Facturacion</label>
                            {/* Campos adicionales */}
                            <input type="text" name="billing_reference" placeholder="Referencia de Facturación" value={formData.billing_reference || ""} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input" />
                        </div>

                        <div>
                            <label className="block font-medium">Notas Publicas</label>
                            <textarea name="notes" placeholder="Notas públicas" value={formData.notes || ""} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input"></textarea>
                        </div>

                        <div>
                            <label className="block font-medium">Notas Interas</label>

                            <textarea name="internal_notes" placeholder="Notas internas" value={formData.internal_notes || ""} onChange={handleChange}
                                className="w-full p-2 bg-white dark:bg-[#1e1e1e] input"></textarea>
                        </div>





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

export default ReservationsForm;
