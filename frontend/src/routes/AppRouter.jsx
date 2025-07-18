import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import {
  Login,
  Register,
  useAuth,
  Dashboard,
  SpacesList,
  SpacesForm,
  BranchesForm,
  BranchesList,
  CustomersForm
} from '.././index.js'

export default function AppRouter() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <div>Cargando...</div>;

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/register"
          element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/spaces"
          element={isAuthenticated ? <SpacesList /> : <Navigate to="/spaces" />}
        />
        <Route
          path="/spaces/create"
          element={isAuthenticated ? <SpacesForm /> : <Navigate to="/spaces" />}
        />

        <Route
          path="/spaces/edit/:id"
          element={isAuthenticated ? <SpacesForm /> : <Navigate to="/spaces" />}
        />

        <Route
          path="/branches"
          element={isAuthenticated ? <BranchesList /> : <Navigate to="/spaces" />}
        />
        <Route
          path="/branches/create"
          element={isAuthenticated ? <BranchesForm /> : <Navigate to="/branches" />}
        />
        <Route
          path="/branches/edit/:id"
          element={isAuthenticated ? <BranchesForm /> : <Navigate to="/branches" />}
        />

        <Route
          path="/customers/create"
          element={isAuthenticated ? <CustomersForm /> : <Navigate to="/customers" />}
        />

        <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />

      </Routes>
    </BrowserRouter>
  );
}
