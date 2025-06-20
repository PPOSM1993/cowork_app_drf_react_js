import React from 'react';
import AppRouter from './routes/AppRouter';
import { AuthProvider } from './index';

function App() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  );
}

export default App;
