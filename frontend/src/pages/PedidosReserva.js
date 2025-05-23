import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "../styles/PedidosReserva.css";
import Navbar2 from "../components/Navbar2.jsx";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Input from '../components/Input.jsx';
import Button from '../components/Button.jsx';

const ReservarRecurso = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/recursos/${id}`, {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
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
    const formData = new FormData();
    formData.append('recurso_id', id);
    formData.append('data_inicio', startDate);
    formData.append('data_fim', endDate);

    try {
      const res = await fetch('http://localhost:8000/api/reserva/pedidosreserva/criar', {
        method: 'POST',
        body: formData,
        credentials: 'include',
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

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!product) {
    return <div>Erro ao carregar o produto.</div>;
  }

return (
  <>
  <Navbar2 />
  <div className="reservar-page">
    
    <div className="reservar-container">
      
      <div className="reservar-left">
        <img src={product.Image} alt={product.name} />
      </div>
    </div>

      <div className="reservar-right">
        <div className="reservar-details">
          <h2>Nome: {product.Nome}</h2>
          <h2>Descrição: {product.Categoria_.DescCategoria}</h2>
          <h2>Caução: {product.Caucao}€</h2>
        </div>

        <label className="reservar-label">
          Data Início:
          <Input value={startDate} onChange={(e) => setStartDate(e.target.value)} type="date" variant="geral" />
        </label>

        <label className="reservar-label">
          Data Fim:
          <Input value={endDate} onChange={(e) => setEndDate(e.target.value)} type="date" variant="geral" />
        </label>

        <div className="reservar-buttons">
          <button className="reservar-button" onClick={handleReserve}>Reservar</button>
        </div>
      </div>
    <ToastContainer />
  </div>
  </>
);
};

export default ReservarRecurso;
