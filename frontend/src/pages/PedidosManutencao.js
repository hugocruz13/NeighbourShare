import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";
import ModalForm from '../components/ModalForm.jsx';
import Modal from '../components/ModalForm.jsx';
import Select from '../components/Select.jsx';

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
        console.log(data);
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
        console.log(data);
        setStatusOptions(data); // Assuming data is an array of status options
        console.log("Resposta dos status:", data);
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

      toast.success('Estado do pedido atualizado com sucesso!');
      
      // Update local state
      setPedidos((prevPedidos) =>
        prevPedidos.map((pedido) =>
          pedido.PMID === pedido_id ? { ...pedido, estado: novo_estado_id } : pedido
        )
      );
    } catch (error) {
      console.error('Erro ao atualizar estado do pedido:', error);
      toast.error('Erro ao atualizar estado do pedido.');
    }
  };

  const handleNaoClick = () => {
    setShowModal(false);
    setShowJustificationModal(true);
  };
    
  const handleJustificationSubmit = () => {
    // Aqui você pode adicionar a lógica para enviar a justificação ao servidor
    console.log('Justificação:', justificacao);
    setShowJustificationModal(false);
    setJustificacao('');
  };

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
                      options={statusOptions.map((option) => ({
                        value: option.EstadoPedManuID,
                        label: option.DescEstadoPedidoManutencao
                      }))}
                      value={pedido.EstadoPedManuID}
                      onChange={(selectedOption) => handleStatusChange(pedido.PMID, selectedOption.value)}
                      onClick={() => {
                        setSelectedPedido(pedido.PMID);
                        setShowModal(true);
                      }}
                    variant='geral'/>
                  );
                }
              }
            ]}
            dados={pedidos}
          />
      </div>
      <ToastContainer />
    </div>
  );
  
};

export default PedidosManutencao;
