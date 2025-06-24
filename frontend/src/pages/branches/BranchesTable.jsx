import React, { useEffect, useState } from "react";
import axios from "axios";
import DataTable from "react-data-table-component";
import { Link, useNavigate } from "react-router-dom";
import { FaPen, FaPlus } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import Swal from "sweetalert2";
import { useTranslation } from 'react-i18next';

const BranchesTable = () => {
    const { t } = useTranslation();
    const [branch, setBranch] = useState([]);
    const [filterText, setFilterText] = useState("");
    const [perPage, setPerPage] = useState(10);
    const navigate = useNavigate();
    const [isDark, setIsDark] = useState(document.documentElement.classList.contains("dark"));

    // Detecta cambios en el modo oscuro (por ejemplo, cuando el usuario cambia el tema)
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
            },
        },
        rows: {
            style: {
                backgroundColor: isDark ? "#121212" : "#ffffff",
                color: isDark ? "#e5e5e5" : "#111827",
            },
        },
        headRow: {
            style: {
                backgroundColor: isDark ? "#121212" : "#f3f4f6",
                color: isDark ? "#ffffff" : "#111827",
            },
        },
        headCells: {
            style: {
                color: isDark ? "#f9f9f9" : "#121212",
                fontWeight: "bold",
            },
        },
        cells: {
            style: {
                color: isDark ? "#121212" : "#121212",
            },
        },
        pagination: {
            style: {
                backgroundColor: isDark ? "#121212" : "#ffffff",
                color: isDark ? "#ffffff" : "#111827",
            },
        },
    };

    const fetchBranch = async (q = "") => {
        const token = localStorage.getItem("access_token");
        const res = await axios.get(`http://localhost:8000/api/branches/search/?q=${q}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        setBranch(res.data);
    };

    useEffect(() => {
        fetchBranch();
    }, []);

    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            fetchBranch(filterText);
        }, 300);
        return () => clearTimeout(delayDebounce);
    }, [filterText]);

    const handleDelete = async (id) => {
        const confirm = await Swal.fire({
            title: "¿Estás seguro?",
            text: "Esta Sucursal será eliminada permanentemente.",
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
                await axios.delete(`http://localhost:8000/api/branches/delete/${id}/`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                Swal.fire("Eliminado", "Sucursal eliminada correctamente.", "success");
                fetchBranch();
            } catch (error) {
                console.error("Error al eliminar:", error);
                Swal.fire("Error", "No se pudo eliminar la Sucursal.", "error");
            }
        }
    };

    const handleEdit = (id) => {
        navigate(`/branches/edit/${id}`);
    };

    const columns = [
        {
            name: "Sucursal",
            selector: row => row.name,
            sortable: true,
        },
        {
            name: "Direccion",
            selector: row => row.address,
            sortable: true,
        },
        {
            name: "Telefono",
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
                        className="bg-yellow-500 text-black px-3 py-3 rounded text-xs sm:text-sm cursor-pointer hover:bg-yellow-600 transition"
                        title="Editar"
                    >
                        <FaPen />
                    </button>
                    <button
                        onClick={() => handleDelete(row.id)}
                        className="bg-red-500 text-white px-3 py-3 rounded text-xs sm:text-sm cursor-pointer hover:bg-red-600 transition"
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
        <div className="p-4 bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100 rounded-xl shadow transition-colors duration-300 border border-none">
            <input
                type="text"
                placeholder={t('buscador')}
                className="w-full max-w-md px-4 py-2 mb-4 border border-none rounded-xl bg-white dark:bg-[#121212] dark:text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500"
                value={filterText}
                onChange={(e) => setFilterText(e.target.value)}
            />

            <DataTable
                columns={columns}
                data={branch}
                pagination
                paginationPerPage={perPage}
                paginationRowsPerPageOptions={[5, 10, 25, 50, 100]}
                onChangeRowsPerPage={setPerPage}
                highlightOnHover
                responsive
                striped
                noDataComponent={t('listar')}
                customStyles={customStyles}
                className={`${isDark ? "text-white" : "text-black"}`}
            />

            <div className="mt-4 text-right">
                <Link to="/branches/create">
                    <button className="bg-yellow-400 text-black p-3 rounded-md shadow hover:bg-yellow-500 transition flex items-center space-x-2">
                        <FaPlus />
                        <span>{t('button_new_branches')}</span>
                    </button>
                </Link>
            </div>
        </div>
    );
};

export default BranchesTable;
