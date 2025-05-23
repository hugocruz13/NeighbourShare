import React, { useState, useEffect } from 'react';
import Navbar2 from "../components/Navbar2.js";
import 'react-toastify/dist/ReactToastify.css';
import Tabela from '../components/Tabela.jsx';
import { IoMdCloseCircle } from "react-icons/io";
import { FaCheck } from 'react-icons/fa';
import Button from '../components/Button.jsx';
import ModalForm from '../components/ModalForm.jsx';
import ToastManager from '../components/ToastManager';
import { Toaster } from 'react-hot-toast';

const ReservarRecurso = ({ match }) => {
  const [comoSolicitante, setComoSolicitante] = useState([]); // data[1]
  const [comoDono, setComoDono] = useState([]);               // data[0]
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [motivoRecusacao, setMotivoRecusacao] = useState('');
  const [pedidoParaRecusar, setPedidoParaRecusar] = useState(null);

  /*Obtenção dos dados dos pedidos de reserva, quer como dono quer como vizinho*/
  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/reserva/pedidosreserva/lista', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        setComoDono(data[0]);         // Dono → pedidos recebidos
        setComoSolicitante(data[1]);  // Solicitante → pedidos que fez
      } catch (error) {
        console.error('Erro ao buscar pedidos de reserva:', error);
      }
    };
    fetchReservations();
  }, []);

  /*Função para abrir o modal de recusa de pedido*/
  const abrirModalRecusa = (PedidoReservaID) => {
    setPedidoParaRecusar(PedidoReservaID);
    setShowRejectModal(true);
  };

  /*Função para confirmar a recusa de um pedido de reserva*/
  const confirmarRecusa = () => {
    ToastManager.customConfirm(
      'Tem a certeza que deseja recusar este pedido de reserva?',
      () => handleRejeitaPedidoReserva(pedidoParaRecusar, motivoRecusacao), // Sim
      () => {} // Não
    );
  };

  /*Função para aceitar um pedido de reserva*/
  const handleAceitarPedidoReserva = async (PedidoReservaID) => {
    ToastManager.customConfirmAsync(
  'Tem a certeza que deseja aceitar este pedido de reserva?',
  async () => {
        try {
          const res = await fetch(`http://localhost:8000/api/reserva/criar?pedido_reserva_id=${PedidoReservaID}`, {
            method: 'POST',
            credentials: 'include',
          });

          if (res.ok) {
            ToastManager.success('Reserva realizada com sucesso!');

            // Atualiza a lista de pedidos de reserva
            setComoDono(prev =>
            prev.filter(pedido => pedido.PedidoReservaID !== PedidoReservaID)
          );

          } else {
            ToastManager.error('Erro ao realizar reserva.');
          }
        } catch (error) {
          console.error('Erro ao enviar reserva:', error);
          ToastManager.error('Erro ao enviar reserva.');
        }
      }
    );
  };

  /*Função para recusar um pedido de reserva*/
  const handleRejeitaPedidoReserva = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/reserva/pedidosreserva/recusar?pedido_reserva_id=${pedidoParaRecusar}&motivo_recusacao=${encodeURIComponent(motivoRecusacao)}`, {
        method: 'POST',
        credentials: 'include',
      });
      if (res.ok) {
        ToastManager.success('Pedido de reserva recusado com sucesso!');
        setComoDono(prev => prev.filter(p => p.PedidoReservaID !== pedidoParaRecusar));
        setShowRejectModal(false);
        setMotivoRecusacao('');
        setPedidoParaRecusar(null);
      } else {
        ToastManager.error('Erro ao recusar pedido de reserva.');
        setShowRejectModal(false);
      }
    } catch (error) {
      ToastManager.error('Erro ao recusar pedido de reserva.');
      console.error('Erro ao recusar pedido de reserva:', error);
      setShowRejectModal(false);
    }
  };

  /*Filtragem dos pedidos de reserva em análise*/
  const pedidosEmAnaliseSolicitante = Array.isArray(comoSolicitante) ? comoSolicitante.filter(reservation => reservation.EstadoPedidoReserva === "Em análise") : [];
  const pedidosEmAnaliseDono = Array.isArray(comoDono) ? comoDono.filter(reservation => reservation.EstadoPedidoReserva === "Em análise" ) : [];

  return (
    <>
    <Toaster position="top-center" />
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
          <Tabela
            titulo={'Pedidos de Reserva - Solicitante'}
            colunas={[
              { id: 'PedidoReservaID',accessorKey: 'PedidoReservaID', header: 'ID' },
              { id: 'UtilizadorNome',accessorKey: 'UtilizadorNome', header: 'Nome Utilizador' },
              { id: 'RecursoNome',accessorKey: 'RecursoNome', header: 'Nome do Recurso' },
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
              { id: 'UtilizadorNome',accessorKey: 'UtilizadorNome', header: 'Nome Utilizador' },
              { id: 'RecursoNome',accessorKey: 'RecursoNome', header: 'Nome do Recurso' },
              { id: 'DataInicio',accessorKey: 'DataInicio', header: 'Data Início' },
              { id: 'DataFim',accessorKey: 'DataFim', header: 'Data Fim' },
              {
                  accessorKey: 'Acao',
                  header: 'Aceitar ?',
                  cell: ({ row }) => (
                    <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                      <Button
                        variant="green"
                        onClick={() => handleAceitarPedidoReserva(row.original.PedidoReservaID)}
                      >
                        <FaCheck  color="white" size={18} />
                      </Button>
                      <Button
                        variant="red"
                        onClick={() => abrirModalRecusa(row.original.PedidoReservaID)}
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

      <ModalForm
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
          confirmarRecusa();
        }}
        textBotao={'Recusar Pedido'}
      />  
    </div>
    </>
  );
};

export default ReservarRecurso;

