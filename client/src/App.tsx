import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import LoginPage from './LoginPage';
import ColivingsPage from './ColivingsPage';
import CreateColiving from './CreateColiving';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Bienvenido a Dev_Forge</h1>
        <nav>
          <Link to="/login">
            <button>Iniciar sesión</button>
          </Link>
          <Link to="/colivings">
            <button>Ver Colivings</button>
          </Link>
          <Link to="/create-coliving">
            <button>Crear Coliving</button>
          </Link>
        </nav>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/colivings" element={<ColivingsPage />} />
          <Route path="/create-coliving" element={<CreateColiving />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
