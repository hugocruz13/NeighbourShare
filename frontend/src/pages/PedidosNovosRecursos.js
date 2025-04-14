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
    


  return (
    <div className="page-content">


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
              <button>Adicionar</button>
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
    </div>
  );
};

export default PedidosAquisicao;