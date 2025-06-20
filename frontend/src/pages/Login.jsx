import { useState } from 'react';
import { useAuth } from '.././index';
import { useNavigate } from 'react-router-dom';
import { MdOutlineLogin } from "react-icons/md";
import Swal from 'sweetalert2'
import logo from '../assets/3.png'
export default function Login() {

  const { login } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Corregimos el campo 'email' a 'username' en el payload
    const payload = {
      username: formData.email, // backend acepta email, username o rut como 'username'
      password: formData.password
    };

    const success = await login(payload);
    setLoading(false);

    if (success) {
      navigate('/dashboard');
    } else {

      Swal.fire({
        icon: 'error',
        title: 'Error de autenticación',
        text: 'Credenciales inválidas. Verifica tu correo o contraseña.',
        confirmButtonColor: '#3085d6'
      });

      //setError('Credenciales inválidas.');
    }
  };

  return (
    <>
      <div className="min-h-screen grid grid-cols-1 md:grid-cols-1 bg-gradient-to-br bg-[#242424]">
        {/* Columna Izquierda - Logo y formulario */}
        <div className="flex flex-col items-center justify-center gap-y-6 p-6">
          <img src={logo} alt="Logo" className="w-3/4 max-w-xs" />

          <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Iniciar Sesión</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Correo electrónico
                </label>
                <input
                  type="text"
                  name="email"
                  placeholder="Ingrese Email, Usuario o RUT"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500"
                />
              </div>

              {/* password */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Contraseña
                </label>
                <input
                  type="password"
                  name="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500"
                />
              </div>

              {/* botón */}
              <button
                type="submit"
                disabled={loading}
                className={`w-full flex items-center justify-center gap-2 p-2 rounded-md transition duration-300 
            ${loading ? 'bg-yellow-600 cursor-not-allowed' : 'bg-yellow-500 hover:bg-yellow-400'} 
            text-white font-semibold`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                    Cargando...
                  </>
                ) : (
                  <>
                    <MdOutlineLogin className="h-5 w-5" />
                    Ingresar
                  </>
                )}
              </button>
            </form>

            <div className="text-center mt-4">
              <a href="/register" className="text-sm text-yellow-500 hover:underline">
                ¿No tienes cuenta? Regístrate
              </a>
            </div>
          </div>
        </div>

        {/* Columna derecha vacía (puedes usarla después si quieres contenido adicional) */}
        <div className="hidden md:block" />
      </div>


    </>
  );
}
