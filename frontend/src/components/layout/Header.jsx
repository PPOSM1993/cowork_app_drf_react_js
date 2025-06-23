import React, { useEffect, useState } from 'react';
import { FaBars, FaUserCircle, FaMoon, FaSun } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';

const Header = ({ toggleSidebar }) => {

  const { t, i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  const [darkMode, setDarkMode] = useState(() => {
    return (
      localStorage.getItem('theme') === 'dark' ||
      (!localStorage.getItem('theme') &&
        window.matchMedia('(prefers-color-scheme: dark)').matches)
    );
  });

  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  return (
    <header className="bg-white dark:bg-[#121212] dark:text-white shadow-md px-4 py-3 flex justify-between items-center transition-colors duration-300">
      {/* Botón menú lateral */}
      <button
        onClick={toggleSidebar}
        className="text-gray-700 dark:text-white hover:text-yellow-500 dark:hover:text-yellow-400 transition"
      >
        <FaBars size={20} />
      </button>

      {/* Controles */}
      <div className="flex items-center gap-4">
        {/* Botón dark mode */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="text-gray-700 dark:text-yellow-300 hover:text-yellow-500 dark:hover:text-yellow-400 transition"
          aria-label="Toggle dark mode"
        >
          {darkMode ? <FaSun size={18} /> : <FaMoon size={18} />}
        </button>

        {/* Selector de idioma */}
        <select
          className="border text-sm rounded px-2 py-1 dark:bg-gray-800 dark:text-white"
          onChange={(e) => changeLanguage(e.target.value)}
          defaultValue={i18n.language}

        >
          <option value="es">🇪🇸 Español</option>
          <option value="en">🇬🇧 English</option>
        </select>

        {/* Perfil */}
        <button className="flex items-center gap-2 px-3 py-1 bg-yellow-400 text-black rounded hover:bg-yellow-500 transition font-medium text-sm">
          <FaUserCircle />
          {t('profile')}
        </button>

      </div>
    </header>
  );
};

export default Header;