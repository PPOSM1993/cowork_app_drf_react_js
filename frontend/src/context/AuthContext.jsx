import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginUser, logoutUser, refreshToken } from '../api/authService';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'));
  const [refreshTokenValue, setRefreshTokenValue] = useState(localStorage.getItem('refresh_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (accessToken) {
        try {
          // Puedes hacer request para obtener perfil o validar token
          setUser({}); // Por ahora vacío, luego puedes obtener datos reales
        } catch {
          logout();
        }
      }
      setLoading(false);
    };
    loadUser();
  }, [accessToken]);

  const login = async (credentials) => {
    try {
      const data = await loginUser(credentials);
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      setAccessToken(data.access);
      setRefreshTokenValue(data.refresh);
      setUser(data.user);
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      await logoutUser(refreshTokenValue);
    } catch (error) {
      console.error('Logout failed:', error);
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setAccessToken(null);
    setRefreshTokenValue(null);
  };

  return (
    <AuthContext.Provider value={{ user, accessToken, login, logout, loading, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
