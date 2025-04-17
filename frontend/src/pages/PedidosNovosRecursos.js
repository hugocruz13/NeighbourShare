import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosNovosRecursos.css";
import Navbar2 from "../components/Navbar2.js";

const PedidosAquisicao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosnovos/pendentes', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data)
        setPedidos(data);
      } catch (error) {
        console.error('Erro ao buscar pedidos de aquisição:', error);
      }
    };

    fetchPedidos();
  }, []);

  const handleConsultarClick = (pedido) => {
    setPedidoAtual(pedido);
    setShowModal(true);
  };

  const handleCriarVotacao = async () => {
    const hoje = new Date();
    const dataFim = new Date(hoje);
    dataFim.setDate(dataFim.getDate() + 3); // adiciona 3 dias
    const dataFimFormatada = dataFim.toISOString().split('T')[0];

    try {
      const response = await fetch('http://localhost:8000/api/criarvotacao_novo_recurso', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          titulo: "123",
          descricao: pedidoAtual.DescPedidoNovoRecurso,
          data_fim: dataFimFormatada, // Data de fim como a data atual
          id_pedido: pedidoAtual.PedidoNovoRecID
        }),
        credentials: 'include',
        
        
      });
      
      if (!response.ok) {
        throw new Error('Erro ao criar votação');
      }

      toast.success('Votação criada com sucesso!');
      setShowModal(false);
    } catch (error) {
      console.error('Erro:', error);
      toast.error('Não foi possível criar a votação.');
    }
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
                <div>
                  <p><strong>Nº do Pedido:</strong> {pedidoAtual.PedidoNovoRecID}</p>
                  <p><strong>Solicitante:</strong> {pedidoAtual.Utilizador_.NomeUtilizador}</p>
                  <p><strong>Data Do Pedido:</strong> {pedidoAtual.DataPedido}</p>
                  <p><strong>Descrição:</strong> {pedidoAtual.DescPedidoNovoRecurso}</p>
                </div>
                <div>
                  <button onClick={handleCriarVotacao}>Criar Votação</button>
                  <button onClick={() => setShowModal(false)}>Cancelar</button>
                </div>
              </div>
            </>
          )}

          <p className='p-NovosRecursos'>Pedidos De Aquisição Pendentes</p>
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
                    <Link className='linkStyle' onClick={() => handleConsultarClick(pedido)}>Consultar</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default PedidosAquisicao;
