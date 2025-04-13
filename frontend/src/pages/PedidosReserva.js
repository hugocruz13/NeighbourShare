import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'

const ReservarRecurso = ({ match }) => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  

  useEffect(() => {
    const fetchProduct = async () => {
    try {
     const res = await fetch(`http://localhost:8000/api/recursos/${id}`);
     const data = await res.json();
     setProduct(data);
     setLoading(false);
    } catch (error) {
     console.error('Erro ao buscar produto:', error);
     setLoading(false);
     }
    };
    
     fetchProduct();
    }, [id]);

    
    const handleReserve = async () => {

      // Criar o FormData para enviar ao servidor
      const formData = new FormData();
      formData.append('recurso_id', id);
      formData.append('data_inicio', startDate);  // O input já garante o formato YYYY-MM-DD
      formData.append('data_fim', endDate);      // O input já garante o formato YYYY-MM-DD


      try {
        const res = await fetch('http://localhost:8000/api/reserva/pedidosreserva/criar', {
          method: 'POST',
          headers: {
            // Não precisa definir o Content-Type, o browser vai definir automaticamente para multipart/form-data
          },
          body: formData,
          credentials: 'include', // Enviar cookies
        });
     
      if (res.ok) {
       alert('Reserva realizada com sucesso!');
      } else {
       alert('Erro ao realizar reserva.');
      }
      } catch (error) {
       console.error('Erro ao enviar reserva:', error);
       alert('Erro ao enviar reserva.');
      }
      };
    

  return (
    <div style={{ display: 'flex', gap: '16px' }}>
      
      <div>




        <label>Data Início: <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} /></label>
        <label>Data Fim: <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} /></label>
        <button onClick={handleReserve}>Reservar!</button>
      </div>
    </div>
  );
};

export default ReservarRecurso;
