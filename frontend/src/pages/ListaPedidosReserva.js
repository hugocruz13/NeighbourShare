import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Tabela from '../components/Tabela.jsx';
import { IoMdCloseCircle } from "react-icons/io";
import { FaCheck } from 'react-icons/fa';
import Button from '../components/Button.jsx';
import ModalFrom from '../components/ModalForm.jsx';

const ReservarRecurso = ({ match }) => {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [idPedido, setIDPedido] = useState('');
  const [comoSolicitante, setComoSolicitante] = useState([]); // data[1]
  const [comoDono, setComoDono] = useState([]);               // data[0]
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [motivoRecusacao, setMotivoRecusacao] = useState('');
  const [pedidoReservaID, setPedidoReservaID] = useState(null);

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

  const handleReject = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/reserva/pedidosreserva/recusar?pedido_reserva_id=${pedidoReservaID}&motivo_recusacao=${motivoRecusacao}`, {
        method: 'POST',
        credentials: 'include', // Enviar cookies
      });
      console.log(res);

      if (res.ok) {
        alert('Pedido de reserva recusado com sucesso!');
        setShowRejectModal(false);
        setMotivoRecusacao('');
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
          <Tabela
            titulo={'Pedidos de Reserva - Solicitante'}
            colunas={[
              { id: 'PedidoReservaID',accessorKey: 'PedidoReservaID', header: 'ID' },
              { id: 'NomeUtilizador',accessorKey: 'NomeUtilizador', header: 'Nome Utilizador' },
              { id: 'NomeRecurso',accessorKey: 'NomeRecurso', header: 'Nome do Recurso' },
              { id: 'DataInicio',accessorKey: 'DataInicio', header: 'Data Início' },
              { id: 'DataFim',accessorKey: 'DataFim', header: 'Data Fim' },
              {
                  accessorKey: 'Estado do Pedido',
                  header: 'Estado',
                },
            ]}
            dados={pedidosEmAnaliseSolicitante}
          />

          <Tabela
           titulo={'Pedidos de Reserva - Dono'}
            colunas={[
              { id: 'PedidoReservaID',accessorKey: 'PedidoReservaID', header: 'ID' },
              { id: 'NomeUtilizador',accessorKey: 'NomeUtilizador', header: 'Nome Utilizador' },
              { id: 'NomeRecurso',accessorKey: 'NomeRecurso', header: 'Nome do Recurso' },
              { id: 'DataInicio',accessorKey: 'DataInicio', header: 'Data Início' },
              { id: 'DataFim',accessorKey: 'DataFim', header: 'Data Fim' },
              {
                  accessorKey: 'Acao',
                  header: 'Aceitar ?',
                  cell: ({ row }) => (
                    <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                      <Button
                        variant="editar"
                        onClick={() => {}}
                      >
                        <FaCheck  color="white" size={18} />
                      </Button>
                      <Button
                        variant="eliminar"
                        onClick={() => {}}
                      >
                        <IoMdCloseCircle  color="white" size={18} />
                      </Button>
                    </div>
                  ),
                },
            ]}
            dados={pedidosEmAnaliseDono.map(p => ({
              ...p
            }))}
          />
      </div>

      <ModalFrom
        show={showRejectModal}
        onclose={() => setShowRejectModal(false)}
        title="Recusar Pedido de Reserva"
        fields={[
          { name: 'motivoRecusacao', label: 'Motivo da Recusa', type: 'text', required: true }
        ]}
        formData={{ motivoRecusacao }}
        onChange={(e) => setMotivoRecusacao(e.target.value)}
        onSubmit={(e) => {
          e.preventDefault();
          handleReject();
        }}
        textBotao={'Recusar Pedido'}
      />
      <ToastContainer />
    </div>
  );
};

export default ReservarRecurso;

