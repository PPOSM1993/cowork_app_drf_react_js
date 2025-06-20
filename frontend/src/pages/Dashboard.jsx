import React from 'react';
import { useAuth } from '../index';

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl mb-4">Bienvenido, {user?.first_name || user?.email}</h1>
      <button onClick={logout} className="bg-red-500 text-white px-4 py-2 rounded">
        Cerrar sesión
      </button>
    </div>
  );
}
