import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const PedidosAquisicao = () => {
  const [pedidos, setPedidos] = useState([]);

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomum/pedidosnovos/pendentes');
        const data = await res.json();
        console.log(data)
        setPedidos(data);
      } catch (error) {
        console.error('Erro ao buscar pedidos de aquisição:', error);
      }
    };

    fetchPedidos();
  }, []);

  return (
    <div>
      <h1>Pedidos De Aquisição Pendentes</h1>
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
                <Link to={`/consultarPedidoAquisicao/${pedido.id}`}>Consultar</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PedidosAquisicao;