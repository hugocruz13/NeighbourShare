import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosNovosRecursos.css";
import Navbar2 from "../components/Navbar2.js";

const Votacoes = () => {
  const [votacoes, setVotacoes] = useState({
    lista_votacao_pedido_manutencao: [],
    lista_votacao_pedido_novo_recurso_binarias: [],
    lista_votacao_pedido_novo_recurso_multiplas: []
  });
  const [orcamentos, setOrcamentos] = useState([]);
  const [votacaoAtual, setVotacaoAtual] = useState(null);
  const [selectedOrcamento, setSelectedOrcamento] = useState('');
  const [votoBinario, setVotoBinario] = useState('');
  const [modalAberto, setModalAberto] = useState('');

  useEffect(() => {
    const fetchVotacoes = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/listar_votacaos', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
        setVotacoes(data);
      } catch (error) {
        console.error('Erro ao buscar votacoes:', error);
      }
    };
    fetchVotacoes();
  }, []);

  const abrirModal = async (votacao, tipo) => {
    setVotacaoAtual(votacao);
    setModalAberto(tipo);
    setSelectedOrcamento('');
    setVotoBinario('');

    if (tipo === 'manutencao') {
      try {
        const res = await fetch(`http://localhost:8000/api/votacao_orcamento_pm?id_v=${votacao.votacao_id}`, {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        setOrcamentos(data);
      } catch (error) {
        console.error('Erro ao buscar orçamentos:', error);
      }
    } else if (tipo === 'switch') {
      try {
        const res = await fetch(`http://localhost:8000/api/votacao_orcamento_pedido_novo_recurso?votacao_id=${votacao.votacao_id}`, {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        setOrcamentos(data);
      } catch (error) {
        console.error('Erro ao buscar orçamentos:', error);
      }
    }
  };

  const submeterVoto = async () => {
    try {
      const voto = modalAberto === 'binario' ? votoBinario : selectedOrcamento;

      const res = await fetch('http://localhost:8000/api/votar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          voto,
          id_votacao: votacaoAtual.votacao_id
        })
      });

      if (!res.ok) throw new Error('Erro ao registrar voto.');

      toast.success('Voto registrado com sucesso!');
      setModalAberto('');
    } catch (error) {
      console.error('Erro ao registrar voto:', error);
      toast.error('Erro ao registrar voto.');
    }
  };

  const renderTabela = (titulo, lista, tipo) => (
    <div className='fundoMeusRecursos'>
      <p className='p-NovosRecursos'>{titulo}</p>
      {Array.isArray(lista) && lista.length > 0 ? (
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
            {lista.map((v) => (
              <tr key={v.votacao_id || v.id}>
                <td>{v.votacao_id || v.id}</td>
                <td>{v.titulo}</td>
                <td>{v.descricao}</td>
                <td>{v.data_inicio}</td>
                <td>{v.data_fim}</td>
                <td>
                  <button onClick={() => abrirModal(v, tipo)}>Votar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Nenhuma votação encontrada.</p>
      )}
    </div>
  );

  const renderModal = () => {
    if (!votacaoAtual) return null;

    return (
      <>
        <div className="modal-backdrop" onClick={() => setModalAberto('')} />
        <div className="modal-content">
          <h3>Votação: {votacaoAtual.titulo}</h3>
          <p>{votacaoAtual.descricao}</p>

          {modalAberto === 'binario' ? (
            <>
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
                <button disabled={!votoBinario} onClick={submeterVoto}>Votar</button>
                <button onClick={() => setModalAberto('')}>Fechar</button>
              </div>
            </>
          ) : (
            <>
              <label htmlFor="orcamentos">Selecione um orçamento:</label>
              <select
                id="orcamentos"
                value={selectedOrcamento}
                onChange={(e) => setSelectedOrcamento(e.target.value)}
              >
                <option value="">-- Escolher --</option>
                {orcamentos.map((orcamento) => (
                  <option key={orcamento.OrcamentoID} value={orcamento.OrcamentoID}>
                    {orcamento.DescOrcamento}
                  </option>
                ))}
              </select>
              <div>
                <button disabled={!selectedOrcamento} onClick={submeterVoto}>Votar</button>
                <button onClick={() => setModalAberto('')}>Fechar</button>
              </div>
            </>
          )}
        </div>
      </>
    );
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        {renderTabela('Votações Pedidos Manutenção', votacoes.lista_votacao_pedido_manutencao, 'manutencao')}
        {renderTabela('Votações Novos Recursos (Sim/Não)', votacoes.lista_votacao_pedido_novo_recurso_binarias, 'binario')}
        {renderTabela('Votações Novos Recursos', votacoes.lista_votacao_pedido_novo_recurso_multiplas, 'switch')}
        {renderModal()}
      </div>
      <ToastContainer />
    </div>
  );
};

export default Votacoes;
