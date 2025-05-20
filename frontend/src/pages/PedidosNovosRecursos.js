import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

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

  const handleCriarVotacao = async () => {
    const hoje = new Date();
    const dataFim = new Date(hoje);
    dataFim.setDate(dataFim.getDate() + 3);
    const dataFimFormatada = dataFim.toISOString().split('T')[0];

    try {
      const response = await fetch('http://localhost:8000/api/criarvotacao', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          titulo: "Votação para novo recurso",
          descricao: pedidoAtual.DescPedidoNovoRecurso,
          id_processo: pedidoAtual.PedidoNovoRecID,
          data_fim: dataFimFormatada,
          tipo_votacao: "Aquisição"
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
        <div className={styles.fundo}>
          {showModal && pedidoAtual && (
            <>
              <div className={styles.modalbackdrop} onClick={() => setShowModal(false)} />
              <div className={styles.modalcontent}>
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

          <p className={styles.titulo}>Pedidos De Aquisição Pendentes</p>

          <Tabela
            colunas = {[
              { accessorKey: 'NumPedido', header: 'Nº do Pedido' },
              { accessorKey: 'Solicitante', header: 'Solicitante' },
              { accessorKey: 'DataPedido', header: 'Data Do Pedido' },
              { accessorKey: 'Descricao', header: 'Descrição' },
              { accessorKey: 'Acao', header: 'Ação' }
            ]}

            dados={pedidos.map((pedido) => ({
              'NumPedido': pedido.PedidoNovoRecID,
              'Solicitante': pedido.Utilizador_.NomeUtilizador,
              'DataPedido': pedido.DataPedido,
              'Descricao': pedido.DescPedidoNovoRecurso,
              'Acao': (
                <Link className={styles.btn_registarRecurso} onClick={() => handleConsultarClick(pedido)}>
                  Consultar
                </Link>
              )
            }))}
            mensagemVazio="Nenhum pedido de novo recurso encontrado."
          />
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default PedidosAquisicao;
