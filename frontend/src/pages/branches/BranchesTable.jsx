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
    const [showForm, setShowForm] = useState(false); // Controla el formulario
    const [book, setBook] = useState([]);
    const [filterText, setFilterText] = useState("");
    const [perPage, setPerPage] = useState(10);
    const navigate = useNavigate();

    const fetchBook = async (q = "") => {
        const token = localStorage.getItem("access_token");
        const res = await axios.get(`http://localhost:8000/api/spaces/search/?q=${q}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        setBook(res.data);
    };

    useEffect(() => {
        fetchBook();
    }, []);

    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            fetchBook(filterText);
        }, 300);
        return () => clearTimeout(delayDebounce);
    }, [filterText]);


    const handleDelete = async (id) => {
        const confirm = await Swal.fire({
            title: "¿Estás seguro?",
            text: "Este cliente será eliminado permanentemente.",
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
                await axios.delete(`http://localhost:8000/api/books/delete/${id}/`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                Swal.fire("Eliminado", "Libro eliminado correctamente.", "success");
                fetchBook();
            } catch (error) {
                console.error("Error al eliminar:", error);
                Swal.fire("Error", "No se pudo eliminar el libro.", "error");
            }
        }
    };

    const handleEdit = (id) => {
        navigate(`/spaces/edit/${id}`);
    };

    const columns = [

        {
            name: "Libros",
            selector: row => row.title,
            sortable: true,
        },

        {
            name: "Autor",
            selector: row => row.author.name,
            sortable: true,
        },

        {
            name: "ISBN",
            selector: row => row.isbn,
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
            //allowOverflow: false,
            //button: true,
        },
    ];

    return (
        <div className="p-4 bg-white dark:bg-[#121212] text-gray-800 dark:text-gray-100 rounded-xl shadow transition-colors duration-300">
            <input
                type="text"
                placeholder={t('buscador')}
                className="w-full max-w-md px-4 py-2 mb-4 border rounded-xl bg-white dark:bg-[#2a2a2a] dark:text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500"
                value={filterText}
                onChange={(e) => setFilterText(e.target.value)}
            />

            <DataTable
                columns={columns}
                data={book}
                pagination
                paginationPerPage={perPage}
                paginationRowsPerPageOptions={[5, 10, 25, 50, 100]}
                onChangeRowsPerPage={setPerPage}
                highlightOnHover
                responsive
                striped
                noDataComponent={t('listar')}
                className="min-w-full table-auto border border-gray-200 text-sm sm:text-base"
            />

            <div className="mt-4 text-right">
                <Link to="/branches/create">
                    <button className="bg-yellow-400 text-black p-3 rounded-md shadow hover:bg-yellow-500 transition flex items-center space-x-2">
                        <FaPlus />
                        <span>{t('button_create_space')}</span>
                    </button>
                </Link>
            </div>
            {/* Formulario para crear o editar espacio */}
            {showForm && (
                <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-start pt-20 z-50">
                    <div className="bg-white dark:bg-[#1f1f1f] text-gray-800 dark:text-gray-100 p-6 rounded-lg shadow-md w-full max-w-xl relative transition-colors duration-300">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg font-bold">{t('button_create_space')}</h2>
                            <button
                                onClick={() => setShowForm(false)}
                                className="text-red-500 hover:text-red-700 font-bold text-xl"
                                title="Cerrar"
                            >
                                &times;
                            </button>
                        </div>
                        <SpacesForm onClose={() => setShowForm(false)} />
                    </div>
                </div>
            )}

        </div>
    );
};


export default BranchesTable;