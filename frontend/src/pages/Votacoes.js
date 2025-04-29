import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosNovosRecursos.css";
import Navbar2 from "../components/Navbar2.js";

const Votacoes = () => {
  const [pedidos, setPedidos] = useState([]);
  const [votacoes, setVotacoes] = useState({
    lista_votacao_pedido_manutencao: [],
    lista_votacao_pedido_novo_recurso_binarias: [],
    lista_votacao_pedido_novo_recurso_switchs: []
  });
  const [showModal, setShowModal] = useState(false);
  const [showModal2, setShowModal2] = useState(false);
  const [orcamentos, setOrcamentos] = useState([]);
  const [votacaoAtual, setVotacaoAtual] = useState(null);
  const [selectedOrcamento, setSelectedOrcamento] = useState('');

  const [showModalBinario, setShowModalBinario] = useState(false);  
  const [votoBinario, setVotoBinario] = useState('');


  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/listar_votacaos', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
        setPedidos(data);
        setVotacoes(data);
      } catch (error) {
        console.error('Erro ao buscar votacoes:', error);
      }
    };

    fetchPedidos();
  }, []);

  const handleVotarClick = async (votacao) => {
    setVotacaoAtual(votacao);
    setShowModal(true);

    try {
      const res = await fetch(`http://localhost:8000/api/votacao_orcamento_pm?id_v=${votacao.votacao_id}`, {
        method: 'GET',
        credentials: 'include'
      });
      const data = await res.json();
      console.log(data);
      setOrcamentos(data);
    } catch (error) {
      console.error('Erro ao buscar orçamentos:', error);
    }
  };


  const handleVotarBinarioClick = (votacao) => {
  setVotacaoAtual(votacao);
  setVotoBinario('');
  setShowModalBinario(true);
  };


  const handleVoteBinarioSubmit = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/votar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        voto: votoBinario,
        id_votacao: votacaoAtual.votacao_id
      })
    });

    if (!res.ok) throw new Error('Erro ao registrar voto.');

    const data = await res.json();
    console.log(data);
    toast.success('Voto registrado com sucesso!');
    setShowModalBinario(false);
  } catch (error) {
    console.error('Erro ao registrar voto:', error);
    toast.error('Erro ao registrar voto.');
  }
  };




  const handleVotar2Click = async (votacao) => {
    setVotacaoAtual(votacao);
    setShowModal2(true);

    try {
      const res = await fetch(`http://localhost:8000/api/votacao_orcamento_pedido_novo_recurso?votacao_id=${votacao.votacao_id}`, {
        method: 'GET',
        credentials: 'include'
      });
      const data = await res.json();
      console.log(data);
      setOrcamentos(data);
    } catch (error) {
      console.error('Erro ao buscar orçamentos:', error);
    }
  };

  const handleVoteSubmit = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/votar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          voto: selectedOrcamento,
          id_votacao: votacaoAtual.votacao_id
        })
      });
      if (!res.ok) {
        throw new Error('Erro ao registrar voto.');
      }
      const data = await res.json();
      console.log(data);
      toast.success('Voto registrado com sucesso!');
      setShowModal(false);
      setShowModal2(false);
    } catch (error) {
      console.error('Erro ao registrar voto:', error);
      toast.error('Erro ao registrar voto.');
    }
  };






  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        <div className='fundoMeusRecursos'>
          <p className='p-NovosRecursos'>Votações Pedidos Manutenção</p>
          {Array.isArray(votacoes.lista_votacao_pedido_manutencao) && votacoes.lista_votacao_pedido_manutencao.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Título</th>
                  <th>Descrição</th>
                  <th>Data de Início</th>
                  <th>Data de Fim</th>
                  <th>Ação</th>
                </tr>
              </thead>
              <tbody>
                {votacoes.lista_votacao_pedido_manutencao.map((votacao) => (
                  <tr key={votacao.votacao_id}>
                    <td>{votacao.votacao_id}</td>
                    <td>{votacao.titulo}</td>
                    <td>{votacao.descricao}</td>
                    <td>{votacao.data_inicio}</td>
                    <td>{votacao.data_fim}</td>
                    <td>
                      <button onClick={() => handleVotarClick(votacao)}>Votar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhuma votação de manutenção encontrada.</p>
          )}
        </div>

        <div className='fundoMeusRecursos'>
          <p className='p-NovosRecursos'>Votações Novos Recursos (Sim/Não)</p>
          {Array.isArray(votacoes.lista_votacao_pedido_novo_recurso_binarias) && votacoes.lista_votacao_pedido_novo_recurso_binarias.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Título</th>
                  <th>Descrição</th>
                  <th>Data de Início</th>
                  <th>Data de Fim</th>
                  <th>Ação</th>
                </tr>
              </thead>
              <tbody>
                {votacoes.lista_votacao_pedido_novo_recurso_binarias.map((votacao) => (
                  <tr key={votacao.votacao_id}>
                    <td>{votacao.votacao_id}</td>
                    <td>{votacao.titulo}</td>
                    <td>{votacao.descricao}</td>
                    <td>{votacao.data_inicio}</td>
                    <td>{votacao.data_fim}</td>
                    <td>
                      <button onClick={() => handleVotarBinarioClick(votacao)}>Votar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhuma votação de novo recurso (Sim/Não) encontrada.</p>
          )}
        </div>

        <div className='fundoMeusRecursos'>
          <p className='p-NovosRecursos'>Votações Novos Recursos</p>
          {Array.isArray(votacoes.lista_votacao_pedido_novo_recurso_switchs) && votacoes.lista_votacao_pedido_novo_recurso_switchs.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Título</th>
                  <th>Descrição</th>
                  <th>Data de Início</th>
                  <th>Data de Fim</th>
                  <th>Ação</th>
                </tr>
              </thead>
              <tbody>
                {votacoes.lista_votacao_pedido_novo_recurso_switchs.map((votacao) => (
                  <tr key={votacao.id}>
                    <td>{votacao.id}</td>
                    <td>{votacao.titulo}</td>
                    <td>{votacao.descricao}</td>
                    <td>{votacao.data_inicio}</td>
                    <td>{votacao.data_fim}</td>
                    <td>
                      <button onClick={() => handleVotar2Click(votacao)}>Votar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhuma votação de novo recurso encontrada.</p>
          )}
        </div>

        {/* Modal de Votação */}
        {showModal && votacaoAtual && (
          <>
            <div className="modal-backdrop" onClick={() => setShowModal(false)} />
            <div className="modal-content">
              <h3>Votação: {votacaoAtual.titulo}</h3>
              <p>{votacaoAtual.descricao}</p>
              <label htmlFor="orcamentos">Selecione um orçamento:</label>
              <select
                id="orcamentos"
                value={selectedOrcamento}
                onChange={(e) => setSelectedOrcamento(e.target.value)}
              >
                {orcamentos.map((orcamento) => (
                  <option key={orcamento.OrcamentoID} value={orcamento.OrcamentoID}>
                    {orcamento.DescOrcamento}
                  </option>
                ))}
              </select>
              <div>
                <button onClick={handleVoteSubmit}>Votar</button>
                <button onClick={() => setShowModal(false)}>Fechar</button>
              </div>
            </div>
          </>
        )}

          {/* Modal de Votação Aquisição*/}
          {showModal2 && votacaoAtual && (
          <>
            <div className="modal-backdrop" onClick={() => setShowModal2(false)} />
            <div className="modal-content">
              <h3>Votação: {votacaoAtual.titulo}</h3>
              <p>{votacaoAtual.descricao}</p>
              <label htmlFor="orcamentos">Selecione um orçamento:</label>
              <select
                id="orcamentos"
                value={selectedOrcamento}
                onChange={(e) => setSelectedOrcamento(e.target.value)}
              >
                {orcamentos.map((orcamento) => (
                  <option key={orcamento.OrcamentoID} value={orcamento.OrcamentoID}>
                    {orcamento.DescOrcamento}
                  </option>
                ))}
              </select>
              <div>
                <button onClick={handleVoteSubmit}>Votar</button>
                <button onClick={() => setShowModal2(false)}>Fechar</button>
              </div>
            </div>
          </>
        )}


{showModalBinario && votacaoAtual && (
  <>
    <div className="modal-backdrop" onClick={() => setShowModalBinario(false)} />
    <div className="modal-content">
      <h3>Votação: {votacaoAtual.titulo}</h3>
      <p>{votacaoAtual.descricao}</p>
      <label htmlFor="votoBinario">Selecione o seu voto:</label>
      <select
        id="votoBinario"
        value={votoBinario}
        onChange={(e) => setVotoBinario(e.target.value)}
      >
        <option value="">-- Escolher --</option>
        <option value="sim">Sim</option>
        <option value="nao">Não</option>
      </select>
      <div>
        <button disabled={!votoBinario} onClick={handleVoteBinarioSubmit}>Votar</button>
        <button onClick={() => setShowModalBinario(false)}>Fechar</button>
      </div>
    </div>
  </>
)}



      </div>
      <ToastContainer />
    </div>
  );
};

export default Votacoes;
