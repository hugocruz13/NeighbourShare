import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela";
import ModalForm from "../components/ModalForm.jsx";

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
        setVotacoes(data);
      } catch (error) {
        console.error('Erro ao buscar votações:', error);
      }
    };
    fetchVotacoes();
  }, []);

  const abrirModal = async (votacao, tipo) => {
    setVotacaoAtual(votacao);
    setModalAberto(tipo);
    setSelectedOrcamento('');
    setVotoBinario('');

    const endpoint = tipo === 'manutencao'
      ? `http://localhost:8000/api/votacao_orcamento_pm?id_v=${votacao.votacao_id}`
      : tipo === 'switch'
      ? `http://localhost:8000/api/votacao_orcamento_pedido_novo_recurso?votacao_id=${votacao.votacao_id}`
      : null;

    if (endpoint) {
      try {
        const res = await fetch(endpoint, {
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

  const renderTabela = (titulo, lista, tipo) => {
    const colunas = [
      { accessorKey: 'ID', header: 'ID' },
      { accessorKey: 'Titulo', header: 'Título' },
      { accessorKey: 'Descricao', header: 'Descrição' },
      { accessorKey: 'DataInicio', header: 'Data de Início' },
      { accessorKey: 'DataFim', header: 'Data de Fim' },
      { accessorKey: 'Acao', header: 'Ação' }
    ];

    const dados = lista.map((v) => ({
      ID: v.votacao_id || v.id,
      Título: v.titulo,
      Descrição: v.descricao,
      'Data de Início': v.data_inicio,
      'Data de Fim': v.data_fim,
      Ação: {
        acaoTexto: 'Votar',
        tipo: 'botao',
        disabled: false,
        linhaOriginal: v
      }
    }));

    return (
        <Tabela
          titulo={titulo}
          colunas={colunas}
          dados={dados}
          tipoAcao="botao"
          aoClicarAcao={(linha) => abrirModal(linha.linhaOriginal, tipo)}
          mensagemVazio="Nenhuma votação encontrada."
        />
    );
  };

  const renderModal = () => {
    if (!votacaoAtual) return null;

    return (
      <>
        <ModalForm
          show={modalAberto !== ''}
          onclose={() => {
            setModalAberto('');
            setVotacaoAtual(null);
          }}
          title={`Votação: ${votacaoAtual.titulo}`}
          fields={[
            {
              name: 'voto',
              label: modalAberto === 'binario' ? 'Selecione o seu voto:' : 'Selecione um orçamento:',
              type: modalAberto === 'binario' ? 'select' : 'select',
              options: modalAberto === 'binario'
                ? [
                    { value: '', label: '-- Escolher --' },
                    { value: 'sim', label: 'Sim' },
                    { value: 'nao', label: 'Não' }
                  ]
                : orcamentos.map((orc) => ({
                    value: orc.OrcamentoID,
                    label: orc.DescOrcamento
                  }))
            }
          ]}
          formData={{ voto: modalAberto === 'binario' ? votoBinario : selectedOrcamento }}
          onChange={(e) => {
            if (modalAberto === 'binario') {
              setVotoBinario(e.target.value);
            } else {
              setSelectedOrcamento(e.target.value);
            }
          }}
          onSubmit={(e) => {
            e.preventDefault();
            submeterVoto();
          }}
          textBotao="Votar"
        />
      </>
    );
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        {renderTabela('Votações Pedidos Manutenção', votacoes.lista_votacao_pedido_manutencao, 'manutencao')}
        {renderTabela('Votações Novos Recursos (Sim/Não)', votacoes.lista_votacao_pedido_novo_recurso_binarias, 'binario')}
        {renderTabela('Votações Novos Recursos (Múltipla Escolha)', votacoes.lista_votacao_pedido_novo_recurso_multiplas, 'switch')}
        {renderModal()}
      </div>
      <ToastContainer />
    </div>
  );
};

export default Votacoes;
