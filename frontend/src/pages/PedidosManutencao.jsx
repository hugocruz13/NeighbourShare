import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import ModalForm from '../components/ModalForm.jsx';
import Modal from '../components/ModalForm.jsx';
import Select from '../components/Select.jsx';
import "../styles/PedidosManutencao.css";

const PedidosManutencao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [mensagemErro, setMensagemErro] = useState(null);
  const [statusOptions, setStatusOptions] = useState([]);
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showJustificationModal, setShowJustificationModal] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);
  const [justificacao, setJustificacao] = useState('');
  

  // Fetch pedidos
  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosmanutencao', {
          method: 'GET',
          credentials: 'include' 
        });
        const data = await res.json();
        if (data && Array.isArray(data)) {
          // Se for um array, atualiza os pedidos
          setPedidos(data);
          setMensagemErro(null);  // Limpar erro caso haja pedidos
        } else if (data && data.detail) {
          // Se a resposta contiver a chave 'detail', trata como erro
          setMensagemErro(data.detail);
          setPedidos([]);  // Limpa os pedidos
        } else {
          // Caso não seja nem um array nem um erro, define um erro genérico
          setMensagemErro('Erro inesperado ao carregar os dados');
          setPedidos([]);
        }

      } catch (error) {
        // Caso ocorra um erro durante a requisição
        console.error('Erro ao buscar pedidos de manutenção:', error);
        setMensagemErro('Falha ao carregar os dados');
        setPedidos([]);
      }
    };

    fetchPedidos();
  }, []);

  // Fetch status options
  useEffect(() => {
    const fetchStatusOptions = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosmanutencao/estados', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        setStatusOptions(data); // Assuming data is an array of status options
      } catch (error) {
        console.error('Erro ao buscar opções de estado:', error);
      }
    };

    fetchStatusOptions();
  }, []);

  const handleStatusChange = async (pedido_id, novo_estado_id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/recursoscomuns/pedidosmanutencao/${pedido_id}/estado`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ novo_estado_id: novo_estado_id }),
        
      });
      if (!res.ok) {
        throw new Error('Erro ao atualizar estado do pedido.');
      }

      ToastManager.success('Estado do pedido atualizado com sucesso!');
      
      // Update local state
      setPedidos((prevPedidos) =>
        prevPedidos.map((pedido) =>
          pedido.PMID === pedido_id ? { ...pedido, EstadoPedManuID: novo_estado_id } : pedido
        )
      );

    } catch (error) {
      console.error('Erro ao atualizar estado do pedido:', error);
      ToastManager.error('Erro ao atualizar estado do pedido.');
    }
  };

  const handleNaoClick = () => {
    setShowModal(false);
    setShowJustificationModal(true);
  };
    
  const handleJustificationSubmit = () => {
    // Aqui você pode adicionar a lógica para enviar a justificação ao servidor
    setShowJustificationModal(false);
    setJustificacao('');
  };

  const handleVotacaoExpirada = async (votacao_id)  => {
    try{
      const res = await fetch(`'http://localhost:8000/api/listar_votacaos'`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!res.ok) {
        throw new Error('Erro ao marcar votação como expirada.');
        }

        const data = await res.json();

        const naoExiste = !data.lista_votacao_pedido_manutencao.some(
          item => item.votacao_id === votacao_id
        );

        return naoExiste;

    }
    catch (error) {
      console.error('Erro ao verificar votação expirada:', error);
      ToastManager.error('Erro ao verificar votação expirada.');
    }
  }

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
  
          {/* Modal de Justificação */}
          <ModalForm
            show={showJustificationModal}
            onClose={() => setShowJustificationModal(false)}
            onSubmit={handleJustificationSubmit}
            title="Justificação"
            fields={[
              { name: 'justificacao', label: 'Justificação', type: 'textarea', required: true }
            ]}
            formData={{ justificacao }}
            onChange={(e) => setJustificacao(e.target.value)}
            textBotao="Enviar"
          />
          <Tabela
            titulo="Pedidos de Manutenção"
            colunas={[
              { accessorKey: 'PMID', header: 'Nº Pedido' },
              { accessorKey: 'Utilizador_.NomeUtilizador', header: 'Solicitante' },
              { accessorKey: 'DataPedido', header: 'Data do Pedido' },
              { accessorKey: 'DescPedido', header: 'Descrição' },
              { accessorKey: 'RecursoComun_.Nome', header: 'Recurso' },
              {
                accessorKey: 'Acao',
                header: 'Ação',
                cell: ({ row }) => {
                  const pedido = row.original;
                  return (
                    <Select 
                      value={statusOptions.find(opt => opt.EstadoPedManuID === pedido.EstadoPedManuID) && {
                        value: pedido.EstadoPedManuID,
                        label: statusOptions.find(opt => opt.EstadoPedManuID === pedido.EstadoPedManuID)?.DescEstadoPedidoManutencao
                      }}
                      onChange={(selectedOption) => handleStatusChange(pedido.PMID, selectedOption.target.value)}
                      options={statusOptions.map(opt => ({
                          value: opt.EstadoPedManuID,
                          label: opt.DescEstadoPedidoManutencao
                        }))
                      }
                      variant='geral'
                      menuPortalTarget={document.body}
                      styles={{
                        menuPortal: base => ({ ...base, zIndex: 9999 }),
                        menu: base => ({ ...base, zIndex: 9999 }),
                      }}
                      isDisabled={pedido.EstadoPedManuID === 5}
                    />
                  );
                }
              }
            ]}
            dados={pedidos.filter(
              pedido => pedido.EstadoPedManuID !== 2 && pedido.EstadoPedManuID !== 4
            )}
          />
      </div>
      <Toaster />
    </div>
  );
  
};

export default PedidosManutencao;
