import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "../styles/ListaPedidosReserva.css";
import Navbar2 from "../components/Navbar2.js";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ReservarRecurso = ({ match }) => {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [idPedido, setIDPedido] = useState('');
  const [comoSolicitante, setComoSolicitante] = useState([]); // data[1]
  const [comoDono, setComoDono] = useState([]);               // data[0]

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/reserva/pedidosreserva/lista', {
          method: 'GET',
          credentials: 'include' 
        });
        const data = await res.json();
        console.log(data);
        setComoDono(data[0]);         // Dono → pedidos recebidos
        setComoSolicitante(data[1]);  // Solicitante → pedidos que fez
      } catch (error) {
        console.error('Erro ao buscar pedidos de reserva:', error);
      }
    };

    fetchReservations();
  }, []);

  const handleReserve = async (PedidoReservaID) => {
    try {
      const res = await fetch(`http://localhost:8000/api/reserva/criar?pedido_reserva_id=${PedidoReservaID}`, {
        method: 'POST',
        credentials: 'include', // Enviar cookies
      });
      console.log(res);
   
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
  
  const handleReject = async (PedidoReservaID) => {
    try {
      const res = await fetch(`http://localhost:8000/api/reserva/pedidosreserva/recusar?pedido_reserva_id=${PedidoReservaID}`, {
        method: 'POST',
        credentials: 'include', // Enviar cookies
      });
      console.log(res);

      if (res.ok) {
        alert('Pedido de reserva recusado com sucesso!');
      } else {
        alert('Erro ao recusar pedido de reserva.');
      }
    } catch (error) {
      console.error('Erro ao recusar pedido de reserva:', error);
      alert('Erro ao recusar pedido de reserva.');
    }
  };
  
  const pedidosEmAnaliseSolicitante = Array.isArray(comoSolicitante) ? comoSolicitante.filter(reservation => reservation.EstadoPedidoReserva === "Em análise") : [];
  const pedidosEmAnaliseDono = Array.isArray(comoDono) ? comoDono.filter(reservation => reservation.EstadoPedidoReserva === "Em análise") : [];

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        <div className='fundoListaPedidosReserva'>
          <p className='tituloPedidosReserva'>Os Meus Pedidos de Reserva Feitos</p>
          {pedidosEmAnaliseSolicitante.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>N° Pedido Reserva</th>
                  <th>Nome Recurso</th>
                  <th>Dono</th>
                  <th>Data Inicio</th>
                  <th>Data Fim</th>
                  <th>Estado Pedido</th>
                </tr>
              </thead>
              <tbody>
                {pedidosEmAnaliseSolicitante.map((reservation) => (
                  <tr key={reservation.PedidoReservaID}>
                    <td>{reservation.PedidoReservaID}</td>
                    <td>{reservation.RecursoNome}</td>
                    <td>{reservation.NomeDono}</td>
                    <td>{reservation.DataInicio}</td>
                    <td>{reservation.DataFim}</td>
                    <td>{reservation.EstadoPedidoReserva}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum pedido de reserva encontrado.</p>
          )}
        </div>

        <div className='fundoListaPedidosReserva'>
          <p className='tituloPedidosReserva'>Pedidos de Reserva</p>
          {pedidosEmAnaliseDono.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>N° Pedido Reserva</th>
                  <th>Solicitante</th>
                  <th>Nome Recurso</th>
                  <th>Data Inicio</th>
                  <th>Data Fim</th>
                  <th>Aceitar Reserva</th>
                </tr>
              </thead>
              <tbody>
                {pedidosEmAnaliseDono.map((reservation) => (
                  <tr key={reservation.PedidoReservaID}>
                    <td>{reservation.PedidoReservaID}</td>
                    <td>{reservation.UtilizadorNome}</td>
                    <td>{reservation.RecursoNome}</td>
                    <td>{reservation.DataInicio}</td>
                    <td>{reservation.DataFim}</td>
                    <td>
                      <button className='btnSimPedidoReserva' onClick={() => handleReserve(reservation.PedidoReservaID)}>Sim</button>
                      <button className='btnNaoPedidoReserva' onClick={() => handleReject(reservation.PedidoReservaID)}>Não</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum pedido de reserva encontrado.</p>
          )}
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default ReservarRecurso;
