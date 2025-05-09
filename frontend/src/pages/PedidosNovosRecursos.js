import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosNovosRecursos.css";
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

const PedidosAquisicao = () => {
  const [pedidos, setPedidos] = useState([]);
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
        if (Array.isArray(data)) {
          setPedidos(data);
        } else if (data.detail === 'Nenhum recurso encontrado') {
          setPedidos([]);
        } else {
          throw new Error("Resposta inesperada da API");
        }       
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
  
          <Tabela
            colunas={['Nº do Pedido', 'Solicitante', 'Data Do Pedido', 'Descrição', 'Ação']}
            dados={pedidos.map((pedido) => ({
              'Nº do Pedido': pedido.PedidoNovoRecID,
              'Solicitante': pedido.Utilizador_.NomeUtilizador,
              'Data Do Pedido': pedido.DataPedido,
              'Descrição': pedido.DescPedidoNovoRecurso,
              'Ação': (
                <Link className='linkStyle' onClick={() => handleConsultarClick(pedido)}>
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
