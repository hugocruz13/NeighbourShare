import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import ModalForm from '../components/ModalForm.jsx';
import Modal from '../components/ModalForm.jsx';

const PedidosAquisicao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [mensagemErro, setMensagemErro] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosnovos', {
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
        console.error('Erro ao buscar pedidos de aquisição:', error);
        setPedidos([]);
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
      <Navbar2 />
      <div className="home-container">
          <Tabela
            titulo="Pedidos de Aquisição"
            colunas = {[
              { accessorKey: 'NumPedido', header: 'Nº do Pedido' },
              { accessorKey: 'Solicitante', header: 'Solicitante' },
              { accessorKey: 'DataPedido', header: 'Data Do Pedido' },
              { accessorKey: 'Descricao', header: 'Descrição' },
            ]}

            dados={pedidos.map((pedido) => ({
              'NumPedido': pedido.PedidoNovoRecID,
              'Solicitante': pedido.Utilizador_.NomeUtilizador,
              'DataPedido': pedido.DataPedido,
              'Descricao': pedido.DescPedidoNovoRecurso,
            }))}
          />
      </div>
      <ToastContainer />
    </div>
  );
};

export default PedidosAquisicao;
