import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosManutencao.css";
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

const PedidosManutencao = () => {
  const [pedidos, setPedidos] = useState([]);
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
        if (Array.isArray(data)) {
          setPedidos(data);
        } else if (data.detail === 'Nenhum recurso encontrado') {
          setPedidos([]);
        } else {
          throw new Error("Resposta inesperada da API");
        }
      } catch (error) {
        console.error('Erro ao buscar pedidos de manutenção:', error);
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

  const handleAprovarInterna = async (pedido) => {
    if (pedido.EstadoPedManuID !== 1) {
      toast.error('Só pode aprovar pedidos que estão "Em análise".');
      return;
    }
    try {
      const res = await fetch(`http://localhost:8000/api/recursoscomuns/pedidosmanutencao/${pedido.PMID}/estado`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ novo_estado_id: 2 }), // 2 = Aprovado para manutenção interna
      });
      if (!res.ok) throw new Error('Erro ao aprovar para manutenção interna.');
      toast.success('Pedido aprovado para manutenção interna!');
      setPedidos((prev) =>
        prev.map((p) =>
          p.PMID === pedido.PMID ? { ...p, EstadoPedManuID: 2 } : p
        )
      );
    } catch (error) {
      toast.error(error.message || 'Erro ao aprovar pedido.');
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
        <div className='fundoMeusRecursos'>
  
          {/* Modal de Adicionar Recurso */}
          {showModal && pedidoAtual && (
            <>
              <div className="modal-backdrop" onClick={() => setShowModal(false)} />
              <div className="modal-content">
                <div className='detalhesManutencao'>
                  <p><strong>Nº do Pedido:</strong> {pedidoAtual.PMID}</p>
                  <p><strong>Solicitante:</strong> {pedidoAtual.Utilizador_.NomeUtilizador}</p>
                  <p><strong>Data Do Pedido:</strong> {pedidoAtual.DataPedido}</p>
                  <p><strong>Descrição:</strong> {pedidoAtual.DescPedido}</p>
                  <p><strong>Recurso:</strong> {pedidoAtual.RecursoComun_.Nome}</p>
                </div>
                <div>
                  <p>Pedido necessita de entidade externa</p>
                  <button>Sim</button>
                  <button onClick={handleNaoClick}>Não</button>
                </div>
              </div>
            </>
          )}
  
          {/* Modal de Justificação */}
          {showJustificationModal && (
            <>
              <div className="modal-backdrop" onClick={() => setShowJustificationModal(false)} />
              <div className="modal-content">
                <h2>Justificação</h2>
                <textarea value={justificacao} onChange={(e) => setJustificacao(e.target.value)} required />
                <div>
                  <button onClick={handleJustificationSubmit}>Enviar</button>
                  <button onClick={() => setShowJustificationModal(false)}>Cancelar</button>
                </div>
              </div>
            </>
          )}
  
          <p className='p-meusRecursos'>Pedidos de Manutenção</p>
          <Tabela
            colunas={['Nº do Pedido', 'Solicitante', 'Data Do Pedido', 'Descrição', 'Recurso', 'Ação', 'Execução Interna']}
            dados={pedidos.map((pedido) => ({
              'Nº do Pedido': pedido.PMID,
              'Solicitante': pedido.Utilizador_.NomeUtilizador,
              'Data Do Pedido': pedido.DataPedido,
              'Descrição': pedido.DescPedido,
              'Recurso': pedido.RecursoComun_.Nome,
              'Ação': (
                <select
                  value={pedido.estado}
                  onChange={(e) => handleStatusChange(pedido.PMID, e.target.value)}
                >
                  {statusOptions.map((option) => (
                    <option key={option.EstadoPedManuID} value={option.EstadoPedManuID}>
                      {option.DescEstadoPedidoManutencao}
                    </option>
                  ))}
                </select>
              ),
              'Execução Interna': (
                <button
                  className="btnAprovarInterna"
                  onClick={() => handleAprovarInterna(pedido)}
                  disabled={pedido.EstadoPedManuID !== 1}
                >
                  Aprovar Execução Interna
                </button>
              )
            }))}
            mensagemVazio="Nenhum pedido de manutenção encontrado."
          />
        </div>
      </div>
      <ToastContainer />
    </div>
  );
  
};

export default PedidosManutencao;
