import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Certifique-se de que o Link está importado
import { useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosManutencao.css";
import Navbar2 from "../components/Navbar2.js";

const PedidosManutencao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showJustificationModal, setShowJustificationModal] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);
  const [justificacao, setJustificacao] = useState('');

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosmanutencao/progresso', {
          method: 'GET',
          credentials: 'include' 
        });
        const data = await res.json();
        console.log(data);
        setPedidos(data);
      } catch (error) {
        console.error('Erro ao buscar pedidos de manutenção:', error);
      }
    };

    fetchPedidos();
  }, []);

  const handleConsultarClick = (pedido) => {
    setPedidoAtual(pedido);
    setShowModal(true);
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
                <textarea value={justificacao} onChange={(e) => setJustificacao(e.target.value)} required/>
              <div>
              <button onClick={handleJustificationSubmit}>Enviar</button>
              <button onClick={() => setShowJustificationModal(false)}>Cancelar</button>
            </div>
            </div>
          </>
          )}

          <p className='p-meusRecursos'>Pedidos de Manutenção</p>
          {pedidos.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Nº do Pedido</th>
                  <th>Solicitante</th>
                  <th>Data Do Pedido</th>
                  <th>Descrição</th>
                  <th>Recurso</th>
                  <th>Ação</th>
                </tr>
              </thead>
              <tbody>
                {pedidos.map((pedido) => (
                  <tr key={pedido.PMID}>
                    <td>{pedido.PMID}</td>
                    <td>{pedido.Utilizador_.NomeUtilizador}</td>
                    <td>{pedido.DataPedido}</td>
                    <td>{pedido.DescPedido}</td>
                    <td>{pedido.RecursoComun_.Nome}</td>
                    <td>
                      <Link className='linkStyle' onClick={() => handleConsultarClick(pedido)}>Consultar</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum pedido de manutenção encontrado.</p>
          )}
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default PedidosManutencao;
