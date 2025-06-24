import { useState } from 'react';
import { useAuth } from '.././index';
import { useNavigate } from 'react-router-dom';
import { MdOutlineLogin } from "react-icons/md";
import Swal from 'sweetalert2'
import logo from '../assets/3.png'

const Login = () => {

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
        <div className="flex flex-col items-center justify-center gap-y-6 subir">
          <img src={logo} alt="Logo" className="w-3/4 max-w-xs" />

          <div className="w-full max-w-md bg-[#242424] p-8 subir-form">
            <h2 className="text-2xl font-bold mb-6 text-center text-white">Iniciar Sesión</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-white">
                  Correo electrónico
                </label>
                <input
                  type="text"
                  name="email"
                  placeholder="Ingrese Email, Usuario o RUT"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500 text-black"
                />
              </div>

              {/* password */}
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

              {/* botón */}
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
                    <MdOutlineLogin className="h-5 w-5" />
                    Ingresar
                  </>
                )}
              </button>
            </form>

            <div className="text-center mt-4">
              <a href="/register" className="text-sm text-white hover:underline">
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

export default Login;