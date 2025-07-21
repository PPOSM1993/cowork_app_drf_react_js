import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  MdDashboard, MdEventNote, MdPeople, MdSettings, MdBusiness, MdPayment,
  MdChat, MdNotifications, MdReviews, MdSupport, MdIntegrationInstructions,
  MdApi, MdArticle, MdGroup, MdVerified, MdBarChart, MdLocationCity,
  MdExpandLess, MdExpandMore, MdHome
} from 'react-icons/md';
import { AiFillCustomerService } from "react-icons/ai";

import { motion } from 'framer-motion';
import logo from '../../assets/4.png';
import { useTranslation } from 'react-i18next';

const Sidebar = ({ isOpen }) => {
  const { t } = useTranslation();

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
      icon: <MdHome size={22} />, // Tamaño aumentado
      items: [
        { path: '/dashboard', icon: <MdDashboard size={20} />, label: t('dashboard') },
        { path: '/branches', icon: <MdLocationCity size={20} />, label: t('branches') },
        { path: '/resources', icon: <MdSettings size={20} />, label: t('resources') },
        { path: '/spaces', icon: <MdSettings size={20} />, label: t('spaces') },
        { path: '/customers', icon: <AiFillCustomerService size={20} />, label: t('customers') },
      ],
    },
    {
      title: t('users'),
      icon: <MdPeople size={22} />,
      items: [
        { path: '/profiles', icon: <MdGroup size={20} />, label: t('profiles') },
        { path: '/auth', icon: <MdPeople size={20} />, label: t('authentication') },
        { path: '/identity', icon: <MdVerified size={20} />, label: t('identity_verification') },
        { path: '/referrals', icon: <MdPeople size={20} />, label: t('referrals') },
      ],
    },
    {
      title: t('business'),
      icon: <MdBusiness size={22} />,
      items: [
        { path: '/reservations', icon: <MdEventNote size={20} />, label: t('reservations') },
        { path: '/payments', icon: <MdPayment size={20} />, label: t('payments') },
        { path: '/memberships', icon: <MdGroup size={20} />, label: t('memberships') },
        { path: '/reports', icon: <MdBarChart size={20} />, label: t('reports') },
      ],
    },
    {
      title: t('communication'),
      icon: <MdChat size={22} />,
      items: [
        { path: '/chat', icon: <MdChat size={20} />, label: t('chat') },
        { path: '/notifications', icon: <MdNotifications size={20} />, label: t('notifications') },
      ],
    },
    {
      title: t('interaction'),
      icon: <MdReviews size={22} />,
      items: [
        { path: '/reviews', icon: <MdReviews size={20} />, label: t('reviews') },
        { path: '/support', icon: <MdSupport size={20} />, label: t('support') },
        { path: '/recommendations', icon: <MdPeople size={20} />, label: t('recommendations') },
      ],
    },
    {
      title: t('integrations'),
      icon: <MdIntegrationInstructions size={24} />,
      items: [
        { path: '/integrations', icon: <MdIntegrationInstructions size={20} />, label: t('integrations') },
        { path: '/api-gateway', icon: <MdApi size={20} />, label: t('api_gateway') },
      ],
    },
    {
      title: t('content'),
      icon: <MdArticle size={22} />,
      items: [
        { path: '/blog', icon: <MdArticle size={20} />, label: t('blog') },
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

        {sections.map(({ title, items, icon }) => {
          const isOpenSection = openSections[title];

          return (
            <div key={title} className="mt-4">
              {isOpen ? (
                <button
                  onClick={() => toggleSection(title)}
                  className="w-full flex justify-between items-center text-gray-400 uppercase text-md px-2 mb-2 hover:text-yellow-300 transition"
                >
                  <div className="flex items-center gap-3">
                    {icon}
                    <span>{title}</span>
                  </div>
                  {isOpenSection ? <MdExpandLess size={20} /> : <MdExpandMore size={20} />}
                </button>
              ) : (
                <div className="flex justify-center" title={title}>
                  {icon}
                </div>
              )}

              {isOpenSection && (
                <div className="space-y-1">
                  {items.map(({ path, icon, label }) => (
                    <NavLink
                      key={path}
                      to={path}
                      className={({ isActive }) =>
                        `flex items-center gap-3 px-2 py-2 rounded hover:bg-yellow-500/20 transition ${
                          isActive ? 'bg-yellow-500/10' : ''
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
