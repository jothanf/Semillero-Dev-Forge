import React, { useState } from 'react';
import axios from 'axios';

const CreateColiving = () => {
  const [nombre, setNombre] = useState('');
  const [direccion, setDireccion] = useState('');
  const [telefono, setTelefono] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const coliving = {
      nombre_coliving: nombre,
      direccion: direccion,
      telefono: telefono,
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/colivings/api/v1/coliving/', coliving, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Coliving creado:', response.data);
      setRespuesta('Coliving creado correctamente.');
      setError('');
    } catch (error) {
      console.error('Error al crear el coliving:', error);
      setRespuesta('');
      setError('Error al crear el coliving.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Nombre del Coliving:</label>
        <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
      </div>
      <div>
        <label>Dirección:</label>
        <input type="text" value={direccion} onChange={(e) => setDireccion(e.target.value)} required />
      </div>
      <div>
        <label>Teléfono:</label>
        <input type="number" value={telefono} onChange={(e) => setTelefono(e.target.value)} required />
      </div>
      <button type="submit">Crear Coliving</button>

      {respuesta && <p>{respuesta}</p>}
      {error && <p>{error}</p>}
    </form>
  );
};

export default CreateColiving;
