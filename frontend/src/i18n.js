import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  es: {
    translation: {
      welcome: 'Bienvenido',
      login: 'Iniciar Sesión',
      register: 'Registrarse',
      dashboard: 'Tablero',
      clients: 'Clientes',
      reservations: 'Reservas',
      config: 'Configuración',
      profile: 'Perfil',
      title_space: "Espacios",
      listar: "No se encontraron resultados",
      buscador:"Buscar Espacios",
      title_form_spaces: "Registrar Nuevo Espacio",


      // Nuevas secciones y etiquetas del Sidebar
      general: 'General',
      users: 'Usuarios',
      business: 'Negocio',
      communication: 'Comunicación',
      interaction: 'Interacción',
      integrations: 'Integraciones',
      content: 'Contenido',
      button_create_space: " Crear Espacio",

      branches: 'Sucursales',
      resources: 'Recursos',
      spaces: 'Espacios',
      profiles: 'Perfiles',
      authentication: 'Autenticación',
      identity_verification: 'Verificación de Identidad',
      referrals: 'Referidos',
      payments: 'Pagos',
      memberships: 'Membresías',
      reports: 'Reportes',
      chat: 'Chat',
      notifications: 'Notificaciones',
      reviews: 'Reseñas',
      support: 'Soporte',
      recommendations: 'Recomendaciones',
      integrations_label: 'Integraciones',
      api_gateway: 'API Gateway',
      blog: 'Blog',
      name_spaces:"Nombre Espacio",
      placeholer_spaces: "Ingrese Espacio",
      title_description: "Descripcion"
    },
  },
  en: {
    translation: {
      welcome: 'Welcome',
      login: 'Login',
      register: 'Register',
      dashboard: 'Dashboard',
      clients: 'Clients',
      reservations: 'Reservations',
      config: 'Settings',
      profile: 'Profile',
      title_space: 'Spaces',

      general: 'General',
      users: 'Users',
      business: 'Business',
      communication: 'Communication',
      interaction: 'Interaction',
      integrations: 'Integrations',
      content: 'Content',
      button_create_space: " Create Space",
      listar:"No results found",
      buscador:"Searching Spaces",

      branches: 'Branches',
      resources: 'Resources',
      spaces: 'Spaces',
      profiles: 'Profiles',
      authentication: 'Authentication',
      identity_verification: 'Identity Verification',
      referrals: 'Referrals',
      payments: 'Payments',
      memberships: 'Memberships',
      reports: 'Reports',
      chat: 'Chat',
      notifications: 'Notifications',
      reviews: 'Reviews',
      support: 'Support',
      recommendations: 'Recommendations',
      integrations_label: 'Integrations',
      api_gateway: 'API Gateway',
      blog: 'Blog',
      title_form_spaces: "Create New Spaces",
      name_spaces: "Name Spaces",
      placeholer_spaces: "Enter Spaces",
      title_description: "Description"
    },
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'es',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;