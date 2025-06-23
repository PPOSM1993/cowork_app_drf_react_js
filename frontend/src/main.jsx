import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'
import App from './App.jsx'
import './i18n'; // <-- Importante

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div className="min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white">
      <App />
    </div>
  </React.StrictMode>
);