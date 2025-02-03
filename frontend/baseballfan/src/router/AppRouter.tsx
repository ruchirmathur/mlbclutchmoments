// src/routes/AppRouter.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import WebPage from '../pages/Web';
import AudioPage from '../pages/Audio.js';

const AppRouter: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AudioPage />} />
        <Route path="/web" element={<WebPage/>} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
