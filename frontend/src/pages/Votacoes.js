import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosNovosRecursos.css";
import Navbar2 from "../components/Navbar2.js";

const Votacoes = () => {
  const [pedidos, setPedidos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);
  const [votacoes, setVotacoes] = useState([]);

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/votacoes/listar', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
        setPedidos(data);
      } catch (error) {
        console.error('Erro ao buscar pedidos de aquisição:', error);
      }
    };

    fetchPedidos();
  }, []);

  const handleConsultarClick = async (pedido) => {
    setPedidoAtual(pedido);
    setShowModal(true);

    try {
      const res = await fetch(`http://localhost:8000/api/votacao_orcamento_pm?id=${pedido.PedidoNovoRecID}`, {
        method: 'GET',
        credentials: 'include'
      });
      const data = await res.json();
      console.log(data);
      setVotacoes(data);
    } catch (error) {
      console.error('Erro ao buscar votações:', error);
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        <div className='fundoMeusRecursos'>
          {/* Modal de Ver Votações */}
          {showModal && pedidoAtual && (
            <>
              <div className="modal-backdrop" onClick={() => setShowModal(false)} />
              <div className="modal-content">
                <div>
                  <p><strong>Nº do Pedido:</strong> {pedidoAtual.PedidoNovoRecID}</p>
                  <p><strong>Solicitante:</strong> {pedidoAtual.Utilizador_.NomeUtilizador}</p>
                  <p><strong>Data Do Pedido:</strong> {pedidoAtual.DataPedido}</p>
                  <p><strong>Descrição:</strong> {pedidoAtual.DescPedidoNovoRecurso}</p>
                </div>
                <div>
                  <h3>Lista de Votações</h3>
                  {Array.isArray(votacoes) && votacoes.length > 0 ? (
                    <ul>
                      {votacoes.map((votacao) => (
                        <li key={votacao.id}>
                          <p><strong>Título:</strong> {votacao.titulo}</p>
                          <p><strong>Descrição:</strong> {votacao.descricao}</p>
                          <p><strong>Data de Fim:</strong> {votacao.data_fim}</p>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>Nenhuma votação encontrada.</p>
                  )}
                </div>
                <div>
                  <button onClick={() => setShowModal(false)}>Fechar</button>
                </div>
              </div>
            </>
          )}

          <p className='p-NovosRecursos'>Pedidos De Aquisição Pendentes</p>
          {Array.isArray(pedidos) && pedidos.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Nº do Pedido</th>
                  <th>Solicitante</th>
                  <th>Data Do Pedido</th>
                  <th>Descrição</th>
                  <th>Ação</th>
                </tr>
              </thead>
              <tbody>
                {pedidos.map((pedido) => (
                  <tr key={pedido.PedidoNovoRecID}>
                    <td>{pedido.PedidoNovoRecID}</td>
                    <td>{pedido.Utilizador_.NomeUtilizador}</td>
                    <td>{pedido.DataPedido}</td>
                    <td>{pedido.DescPedidoNovoRecurso}</td>
                    <td>
                      <Link className='linkStyle' onClick={() => handleConsultarClick(pedido)}>Votar</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum pedido de novo recurso encontrado.</p>
          )}
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default Votacoes;
