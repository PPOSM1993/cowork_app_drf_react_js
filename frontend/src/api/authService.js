import axios from 'axios';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/authentication';

export const loginUser = async (credentials) => {
  const res = await axios.post(`${API}/login/`, credentials);
  return res.data;
};

export const registerUser = async (data) => {
  const res = await axios.post(`${API}/register/`, data);
  return res.data;
};

export const logoutUser = async (refreshToken) => {
  const res = await axios.post(`${API}/logout/`, { refresh: refreshToken });
  return res.data;
};

export const refreshToken = async (token) => {
  const res = await axios.post(`${API}/token/refresh/`, { refresh: token });
  return res.data;
};
