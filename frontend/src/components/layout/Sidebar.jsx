import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  MdDashboard, MdEventNote, MdPeople, MdSettings, MdBusiness, MdPayment,
  MdChat, MdNotifications, MdReviews, MdSupport, MdIntegrationInstructions,
  MdApi, MdArticle, MdGroup, MdVerified, MdBarChart, MdLocationCity,
  MdExpandLess, MdExpandMore, MdHome
} from 'react-icons/md';

import { motion } from 'framer-motion';
import logo from '../../assets/4.png';
import { useTranslation } from 'react-i18next';

const Sidebar = ({ isOpen }) => {
  const { t } = useTranslation();

  // Estado para manejar qué secciones están abiertas
  const [openSections, setOpenSections] = useState({});

  const toggleSection = (title) => {
    setOpenSections(prev => ({
      ...prev,
      [title]: !prev[title]
    }));
  };

  const sections = [

    {
      title: t('general'),
      icon: <MdHome />, // ⬅️ ícono para la sección
      items: [
        { path: '/dashboard', icon: <MdDashboard />, label: t('dashboard') },
        { path: '/branches', icon: <MdLocationCity />, label: t('branches') },
        { path: '/resources', icon: <MdSettings />, label: t('resources') },
        { path: '/spaces', icon: <MdSettings />, label: t('spaces') }
        ,
      ],
    },

    {
      title: t('users'),
      items: [
        { path: '/profiles', icon: <MdGroup />, label: t('profiles') },
        { path: '/auth', icon: <MdPeople />, label: t('authentication') },
        { path: '/identity', icon: <MdVerified />, label: t('identity_verification') },
        { path: '/referrals', icon: <MdPeople />, label: t('referrals') },
      ],
    },
    {
      title: t('business'),
      items: [
        { path: '/reservations', icon: <MdEventNote />, label: t('reservations') },
        { path: '/payments', icon: <MdPayment />, label: t('payments') },
        { path: '/memberships', icon: <MdGroup />, label: t('memberships') },
        { path: '/reports', icon: <MdBarChart />, label: t('reports') },
      ],
    },
    {
      title: t('communication'),
      items: [
        { path: '/chat', icon: <MdChat />, label: t('chat') },
        { path: '/notifications', icon: <MdNotifications />, label: t('notifications') },
      ],
    },
    {
      title: t('interaction'),
      items: [
        { path: '/reviews', icon: <MdReviews />, label: t('reviews') },
        { path: '/support', icon: <MdSupport />, label: t('support') },
        { path: '/recommendations', icon: <MdPeople />, label: t('recommendations') },
      ],
    },
    {
      title: t('integrations'),
      items: [
        { path: '/integrations', icon: <MdIntegrationInstructions />, label: t('integrations') },
        { path: '/api-gateway', icon: <MdApi />, label: t('api_gateway') },
      ],
    },
    {
      title: t('content'),
      items: [
        { path: '/blog', icon: <MdArticle />, label: t('blog') },
      ],
    },
  ];

  return (
    <>
      <motion.aside
        animate={{ width: isOpen ? 240 : 64 }}
        className="bg-[#121212] text-white p-4 space-y-4 overflow-y-auto scroll-smooth shadow-lg h-screen hide-scrollbar"
      >
        <div className="text-xl font-bold text-yellow-400 px-2">
          <img src={logo} alt="Logo" />
        </div>

        {sections.map(({ title, items }) => {
          const isOpenSection = openSections[title];

          return (
            <div key={title} className="mt-4">
              {isOpen && (
                <button
                  onClick={() => toggleSection(title)}
                  className="w-full flex justify-between items-center text-gray-400 uppercase text-md px-2 mb-2 hover:text-yellow-300 transition"
                >
                  <span> {title}</span>
                  {isOpenSection ? <MdExpandLess size={20} /> : <MdExpandMore size={20} />}
                </button>
              )}

              {isOpenSection && (
                <div className="space-y-1">
                  {items.map(({ path, icon, label }) => (
                    <NavLink
                      key={path}
                      to={path}
                      className={({ isActive }) =>
                        `flex items-center gap-3 px-2 py-2 rounded hover:bg-yellow-500/20 transition ${isActive ? 'bg-yellow-500/10' : ''
                        }`
                      }
                    >
                      {icon}
                      {isOpen && <span>{label}</span>}
                    </NavLink>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </motion.aside>
    </>
  );
};

export default Sidebar;
