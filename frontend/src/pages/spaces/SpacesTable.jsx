import React, { useEffect, useState } from "react";
import axios from "axios";
import DataTable from "react-data-table-component";
import { Link, useNavigate } from "react-router-dom";
import { FaPen, FaPlus } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import Swal from "sweetalert2";
import { useTranslation } from 'react-i18next';
import { axiosInstance } from '../../index'

const SpacesTable = () => {
    const { t } = useTranslation();
    const [spaces, setSpaces] = useState([]);
    const [filterText, setFilterText] = useState("");
    const [perPage, setPerPage] = useState(10);
    const navigate = useNavigate();
    const [isDark, setIsDark] = useState(document.documentElement.classList.contains("dark"));
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const observer = new MutationObserver(() => {
            setIsDark(document.documentElement.classList.contains("dark"));
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class'],
        });

        return () => observer.disconnect();
    }, []);


    const customStyles = {
        table: {
            style: {
                backgroundColor: isDark ? "#121212" : "#ffffff",
                borderRadius: 0,
            },
        },
        headRow: {
            style: {
                backgroundColor: isDark ? "#121212" : "#f3f4f6", // mismo fondo que fila 3
            },
        },
        headCells: {
            style: {
                color: isDark ? "#ffffff" : "#000000", // texto blanco en dark
                fontWeight: "bold",
            },
        },
        rows: {
            style: {
                backgroundColor: isDark ? "#121212" : "#ffffff",
                color: "#000000", // texto negro por defecto
            },
        },
        cells: {
            style: {
                color: "#000000", // override en fila 3 más abajo
            },
        },
        pagination: {
            style: {
                backgroundColor: isDark ? "#121212" : "#ffffff",
                color: isDark ? "#ffffff" : "#000000",
            },
        },
    };




        const fetchSpaces = async (q = "") => {
        setLoading(true);
        try {
            const res = await axiosInstance.get(`/spaces/search/?q=${q}`);
            setSpaces(res.data);
        } catch (error) {
            console.error("Error al cargar espacios:", error);
            Swal.fire("Error", "No se pudieron cargar los Espacios.", "error");
        } finally {
            setLoading(false);
        }
    };


    useEffect(() => {
        fetchSpaces();
    }, []);

    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            fetchSpaces(filterText);
        }, 300);
        return () => clearTimeout(delayDebounce);
    }, [filterText]);

    const handleDelete = async (id) => {
        const confirm = await Swal.fire({
            title: "¿Estás seguro?",
            text: "Este Espacio será eliminada permanentemente.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar",
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
        });

        if (confirm.isConfirmed) {
            try {
                const token = localStorage.getItem("access_token");
                await axios.delete(`http://localhost:8000/api/spaces/delete/${id}/`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                Swal.fire("Eliminado", "Espacio eliminado correctamente.", "success");
                fetchSpaces();
            } catch (error) {
                console.error("Error al eliminar:", error);
                Swal.fire("Error", "No se pudo eliminar Espacio.", "error");
            }
        }
    };

    const handleEdit = (id) => {
        navigate(`/spaces/edit/${id}`);
    };

    const columns = [
        {
            name: "Espacio",
            selector: row => row.name,
            sortable: true,
        },
        {
            name: "Dirección",
            selector: row => row.address,
            sortable: true,
        },
        {
            name: "Teléfono",
            selector: row => row.phone,
            sortable: true,
        },
        {
            name: "Email",
            selector: row => row.email,
            sortable: true,
        },
        {
            name: "Opciones",
            cell: row => (
                <div className="flex items-center space-x-2 justify-end">
                    <button
                        onClick={() => handleEdit(row.id)}
                        className="bg-yellow-500 text-black px-3 py-3 text-xs sm:text-sm cursor-pointer hover:bg-yellow-600 transition"
                        title="Editar"
                    >
                        <FaPen />
                    </button>
                    <button
                        onClick={() => handleDelete(row.id)}
                        className="bg-red-500 text-white px-3 py-3 text-xs sm:text-sm cursor-pointer hover:bg-red-600 transition"
                        title="Eliminar"
                    >
                        <MdDelete />
                    </button>
                </div>
            ),
            ignoreRowClick: true,
        },
    ];

    return (
        <div className="p-4 bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100 shadow transition-colors duration-300 border">
            <input
                type="text"
                placeholder={t('buscador')}
                className="w-full max-w-md px-4 py-2 mb-4 border border-none bg-white dark:bg-[#121212] dark:text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500"
                value={filterText}
                onChange={(e) => setFilterText(e.target.value)}
            />


            <DataTable
                columns={columns}
                data={spaces}
                pagination
                paginationPerPage={perPage}
                paginationRowsPerPageOptions={[5, 10, 25, 50, 100]}
                onChangeRowsPerPage={setPerPage}
                highlightOnHover
                responsive
                striped
                noDataComponent={t("listar")}
                customStyles={customStyles}
                progressPending={loading}
                conditionalRowStyles={[
                    {
                        when: (row, index) => isDark && index === 2, // tercera fila
                        style: {
                            color: "#ffffff", // texto blanco
                            backgroundColor: "#121212", // asegura fondo igual que cabecera
                        },
                    },
                ]}
                className="text-black"
            />


            <div className="mt-4 text-right">
                <Link to="/spaces/create">
                    <button className="bg-yellow-400 text-black p-3 shadow hover:bg-yellow-500 transition flex items-center space-x-2">
                        <FaPlus />
                        <span>{t('button_new_branches')}</span>
                    </button>
                </Link>
            </div>
        </div>
    );
};

export default SpacesTable;
