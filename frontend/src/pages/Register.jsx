import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import logo from '../assets/3.png';
import { HiOutlineUserAdd } from "react-icons/hi";

const Register = () => {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        rut: '',
        password: '',
        password2: '',
        accepted_terms: false
    });

    const [loading, setLoading] = useState(false);

    const handleChange = e => {
        const { name, value, type, checked } = e.target;
        setFormData({ ...formData, [name]: type === 'checkbox' ? checked : value });
    };

    const handleSubmit = async e => {
        e.preventDefault();
        setLoading(true);

        if (formData.password !== formData.password2) {
            Swal.fire({
                icon: 'warning',
                title: 'Contraseñas no coinciden',
                confirmButtonColor: '#ffcc36'
            });
            setLoading(false);
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/api/authentication/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await res.json();

            if (res.ok) {
                Swal.fire({
                    icon: 'success',
                    title: '¡Registro exitoso!',
                    text: 'Revisa tu correo para confirmar tu cuenta.',
                    confirmButtonColor: '#ffcc36'
                });
                navigate('/login');
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al registrar',
                    text: data?.detail || 'Verifica los campos e intenta nuevamente.',
                    confirmButtonColor: '#ffcc36'
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error de red',
                text: 'No se pudo conectar con el servidor.',
                confirmButtonColor: '#ffcc36'
            });
        }

        setLoading(false);
    };

    return (
        <div className="min-h-screen grid grid-cols-1 md:grid-cols-1 bg-[#242424]">
            {/* Columna Izquierda - Logo y formulario */}
            <div className="flex flex-col items-center justify-center gap-y-6 p-2 subir">
                <img src={logo} alt="Logo" className="w-3/4 max-w-xs" />

                <div className="w-full max-w-md bg-[#242424] p-8">
                    <h2 className="text-2xl font-bold mb-6 text-center text-white subir-form">Crear Usuario</h2>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="first_name" className="block text-sm font-medium text-white">
                                Nombre
                            </label>
                            <input
                                name="first_name"
                                type="text"
                                placeholder="Nombre"
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black"
                            />
                        </div>
                        <div>
                            <label htmlFor="last_name" className="block text-sm font-medium text-white">
                                Apellido
                            </label>
                            <input
                                name="last_name"
                                type="text"
                                placeholder="Apellido"
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black" />
                        </div>


                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-white">
                                Nombre de Usuario
                            </label>
                            <input
                                name="username"
                                type="text"
                                placeholder="Usuario"
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black" />
                        </div>


                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-white">
                                Correo electrónico
                            </label>
                            <input
                                type="email"
                                name="email"
                                placeholder="Ingrese Email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black"
                            />
                        </div>

                        <div>
                            <label htmlFor="rut" className="block text-sm font-medium text-white">
                                RUT
                            </label>
                            <input
                                name="rut"
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black"
                                type="text"
                                placeholder="RUT (12345678-9)"
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-white">
                                Contraseña
                            </label>
                            <input
                                type="password"
                                name="password"
                                placeholder="••••••••"
                                value={formData.password}
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black"
                            />
                        </div>

                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-white">
                                Confirmar Contraseña
                            </label>
                            <input
                                name="password2"
                                type="password"
                                placeholder="Confirmar contraseña"
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black"
                            />
                        </div>



                        <div className="flex items-center text-sm text-white">
                            <input type="checkbox" name="accepted_terms" checked={formData.accepted_terms} onChange={handleChange} className="mr-2" />
                            <label>
                                Acepto los <a href="#" className="text-yellow-500 underline">términos y condiciones</a>
                            </label>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className={`w-full flex items-center justify-center gap-2 p-2 rounded-md transition duration-300 
            ${loading ? 'bg-[#ffcc36] cursor-pointer' : 'bg-[#ffcc36] hover:bg-[#ffcc36]'} 
            text-black font-semibold`}
                        >
                            {loading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                                    </svg>
                                    Cargando...
                                </>
                            ) : (
                                <>
                                    <HiOutlineUserAdd className="h-5 w-5" />
                                    Registrando Usuario
                                </>
                            )}
                        </button>
                    </form>

                    <div className="text-center mt-4">
                        <a href="/login" className="text-sm text-white hover:underline">
                            ¿Ya tienes cuenta? Inicia sesión
                        </a>
                    </div>
                </div>
            </div>

            {/* Columna derecha vacía (si se desea usar luego) */}
            <div className="hidden md:block" />
        </div>
    );
};

export default Register;
