import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

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
        <div className={styles.fundo}>
  
          {/* Modal de Adicionar Recurso */}
          {showModal && pedidoAtual && (
            <>
              <div className={styles.modalbackdrop} onClick={() => setShowModal(false)} />
              <div className={styles.modalcontent}>
                <div className={styles.detalhesManutencao}>
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
              <div className={styles.modalbackdrop} onClick={() => setShowJustificationModal(false)} />
              <div className={styles.modalcontent}>
                <h2>Justificação</h2>
                <textarea value={justificacao} onChange={(e) => setJustificacao(e.target.value)} required />
                <div>
                  <button onClick={handleJustificationSubmit}>Enviar</button>
                  <button onClick={() => setShowJustificationModal(false)}>Cancelar</button>
                </div>
              </div>
            </>
          )}
  
          <p className={styles.pmeusRecursos}>Pedidos de Manutenção</p>
          <Tabela
            colunas={['Nº do Pedido', 'Solicitante', 'Data Do Pedido', 'Descrição', 'Recurso', 'Ação']}
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
