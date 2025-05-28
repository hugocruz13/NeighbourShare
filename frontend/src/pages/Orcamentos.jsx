import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import Button from '../components/Button.jsx';
import ModalForm from '../components/ModalForm.jsx';

const Orcamentos = () => {
  const [orcamentos, setOrcamentos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [newOrcamento, setNewOrcamento] = useState({
    id_entidade_externa: '',
    valor_orcamento: '',
    descricao_orcamento: '',
    pdforcamento: null,
    id_processo: '',
    tipoorcamento: ''
  });
  const [votacao, setVotacao] = useState({
    titulo: '',
    descricao: '',
    id_processo: 0,
    data_fim: '',
    tipo_votacao: 'Aquisição',
  });
  const [fornecedores, setFornecedores] = useState([]);
  const [pedidosAquisicao, setPedidosAquisicao] = useState([]);
  const [pedidosManutencao, setPedidosManutencao] = useState([]);

  const fetchOrcamentos = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/orcamentos/listar', {
        method: 'GET',
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Erro ao buscar dados');
      const data = await res.json();
      setOrcamentos(data);
    } catch (error) {
      console.error('Erro ao buscar orcamentos:', error);
    }
  };

  const fetchFornecedores = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/entidades/ver', {
          method: 'GET',
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Erro ao buscar fornecedores');
        const data = await res.json();
        setFornecedores(data);
      } catch (error) {
        console.error('Erro ao buscar fornecedores:', error);
      }
  };

  const fetchPedidosAquisicao = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosnovos', {
        method: 'GET',
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Erro ao buscar pedidos de aquisição');
      const data = await res.json();
      setPedidosAquisicao(data);
    } catch (error) {
      console.error('Erro ao buscar pedidos de aquisição:', error);
    }
  }

  const fecthPedidosManutencao = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosmanutencao', {
        method: 'GET',
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Erro ao buscar pedidos de manutenção');
      const data = await res.json();
      setPedidosManutencao(data);
    } catch (error) {
      console.error('Erro ao buscar pedidos de manutenção:', error);
    }
  }

  useEffect(() => {
    fetchOrcamentos();
    fetchFornecedores();
    fetchPedidosAquisicao();
    fecthPedidosManutencao();
  }, []);

  const handleAddOrcamento = async () => {
    try {

      if (!newOrcamento.id_entidade_externa || isNaN(parseInt(newOrcamento.id_entidade_externa))) {
            ToastManager.error('ID da entidade externa deve ser um número válido');
            return;
          }
          
          if (!newOrcamento.valor_orcamento || isNaN(parseFloat(newOrcamento.valor_orcamento))) {
            ToastManager.error('Valor do orçamento deve ser um número válido');
            return;
          }
          
          if (!newOrcamento.id_processo || isNaN(parseInt(newOrcamento.id_processo))) {
            ToastManager.error('ID do processo deve ser um número válido');
            return;
          }
          
          if (!newOrcamento.tipoorcamento) {
            ToastManager.error('Tipo de orçamento é obrigatório');
            return;
          }
          
          if (!newOrcamento.pdforcamento) {
            ToastManager.error('Arquivo PDF é obrigatório');
            return;
          }

      const formData = new FormData();

      formData.append('id_entidade_externa', newOrcamento.id_entidade_externa);
      formData.append('valor_orcamento', Number(newOrcamento.valor_orcamento).toFixed(2));
      formData.append('descricao_orcamento', newOrcamento.descricao_orcamento);
      formData.append('pdforcamento', newOrcamento.pdforcamento);
      formData.append('idprocesso', newOrcamento.id_processo);
      formData.append('tipoorcamento', newOrcamento.tipoorcamento);

      const res = await fetch('http://localhost:8000/api/orcamentos/inserir', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Erro ao adicionar recurso');
      }

      ToastManager.success('Orçamento adicionado com sucesso!');
      await fetchOrcamentos(); // <== aqui
      setShowModal(false);
      setNewOrcamento({
        id_entidade_externa: '',
        valor_orcamento: '',
        descricao_orcamento: '',
        pdforcamento: null,
        id_processo: '',
        tipoorcamento: ''
      });
      
    } catch (error) {
      
      console.error('Erro ao adicionar recurso:', error);
      ToastManager.error('Erro ao adicionar recurso: ' + error.message);
    }
  };

  const handleCreateVotacao = async () => {
    try {
      const votacaoCorrigida = {
        ...votacao,
        id_processo: parseInt(votacao.id_processo),
      };
  
      if (!votacaoCorrigida.id_processo || isNaN(votacaoCorrigida.id_processo)) {
        ToastManager.error('ID do processo deve ser um número válido');
        return;
      }
  
      const res = await fetch('http://localhost:8000/api/criarvotacao', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(votacaoCorrigida),
      });
    
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Erro ao criar votação');
      }
  
      ToastManager.success('Votação criada com sucesso!');
      setShowModal(false);
      setVotacao({
        titulo: '',
        descricao: '',
        id_processo: '',
        data_fim: '',
        tipo_votacao: '',
      });
    } catch (error) {
      ToastManager.error('Erro ao criar votação: ' + error.message);
    }
  };
  

  const handleChange = (e, actionMeta) => {
    if (e && e.target) {
      const { name, value, files, type } = e.target;

      if (modalType === 'orcamento') {
        if (type === 'file') {
          const file = files?.[0];
          if (file) {
            setNewOrcamento(prev => ({ ...prev, [name]: file }));
          }
        } else {
          setNewOrcamento(prev => ({ ...prev, [name]: value }));
        }
      } else {
        setVotacao(prev => ({ ...prev, [name]: value }));
      }
    } else if (e && actionMeta && actionMeta.action === 'select-option') {
      // Caso do react-select, que passa o objeto selecionado (e) e meta (actionMeta)
      const name = actionMeta.name;
      if (modalType === 'orcamento') {
        setNewOrcamento(prev => ({ ...prev, [name]: e.value }));
      } else {
        setVotacao(prev => ({ ...prev, [name]: e.value }));
      }
    } else if (e && e.name && e.value) {
      // Caso de um objeto simples com name e value (pode ser redundante, mas seguro)
      if (modalType === 'orcamento') {
        setNewOrcamento(prev => ({ ...prev, [e.name]: e.value }));
      } else {
        setVotacao(prev => ({ ...prev, [e.name]: e.value }));
      }
    }
  };

  const handleDownloadPDF = (caminho) => {
    const url = `http://localhost:8000/${caminho.replace(/\\/g, '/')}`;
    window.open(url, '_blank');
  };
  

  return (
    <div className="page-container">
      <Navbar2 />
      <div className="home-container">
          <ModalForm
            show={showModal}
            onclose={() => setShowModal(false)}
            title={modalType === 'orcamento' ? 'Adicionar Orçamento' : 'Criar Votação'}
            fields={modalType === 'orcamento' ? [
              { name: 'id_entidade_externa', label: 'Fornecedor', type: 'select', options: fornecedores.map(f => ({ value: f.EntidadeID, label: f.Nome })) },
              { name: 'valor_orcamento', label: 'Valor', type: 'number', required: true },
              { name: 'descricao_orcamento', label: 'Descrição', type: 'text' },
              { name: 'tipoorcamento', label: 'Tipo', type: 'select', options:[{value: 'Manutenção', label:'Manutenção'}, {value: 'Aquisição', label: 'Aquisição'}] },
              { name: 'id_processo', label: 'Processo', type: 'select',
                options:
                  newOrcamento.tipoorcamento === 'Aquisição'
                    ? pedidosAquisicao.map(p => ({ value: p.PedidoNovoRecID, label: p.PedidoNovoRecID + ' - ' + p.DescPedidoNovoRecurso }))
                    : newOrcamento.tipoorcamento === 'Manutenção'
                      ? pedidosManutencao.map(p => ({ value: p.PMID, label: p.PMID + ' - ' + p.DescPedido }))
                      : [] },
              { name: 'pdforcamento', label: 'Arquivo', type: 'file' }
            ] : [
              { name: 'titulo', label: 'Título', type: 'text' },
              { name: 'descricao', label: 'Descrição', type: 'text' },
              { name: 'tipo_votacao', label: 'Tipo Votação', type: 'select', options:[{value: 'Manutenção', label:'Manutenção'}, {value: 'Aquisição', label: 'Aquisição'}] },
              { 
                name: 'id_processo', 
                label: 'Processo', 
                type: 'select',
                options: [
                  { value: '', label: votacao.tipo_votacao ? `Selecione o processo de ${votacao.tipo_votacao.toLowerCase()}` : 'Selecione o processo' },
                  ...(votacao.tipo_votacao === 'Aquisição'
                    ? pedidosAquisicao.map(p => ({ value: p.PedidoNovoRecID, label: p.PedidoNovoRecID + ' - ' + p.DescPedidoNovoRecurso }))
                    : votacao.tipo_votacao === 'Manutenção'
                      ? pedidosManutencao.map(p => ({ value: p.PMID, label: p.PMID + ' - ' + p.DescPedido }))
                      : []
                  )
                ] 
              },
              { name: 'data_fim', label: 'Data de Fim', type: 'date' }
              
              
            ]}
            formData={modalType === 'orcamento' ? newOrcamento : votacao}
            onChange={handleChange}
            onSubmit={(e) => {
              e.preventDefault();
              if (modalType === 'orcamento') {
                handleAddOrcamento();
              } else {
                handleCreateVotacao();
              }
            }}
            textBotao={modalType === 'orcamento' ? 'Adicionar' : 'Criar'}
          />
          <Tabela
            titulo={"Orçamentos"}
            const colunas = {[
              { accessorKey: 'NumOrcamento', header: 'Nº Orçamento' },
              { accessorKey: 'Fornecedor', header: 'Fornecedor' },
              { accessorKey: 'Valor', header: 'Valor' },
              { accessorKey: 'Descricao', header: 'Descrição' },
              { accessorKey: 'PDF', 
                header: 'PDF',
              cell: ({ row }) => (
                  <Button variant='default' onClick={() => handleDownloadPDF(row.original.CaminhoPDF)}text={"Download"}>Abrir</Button>
              )
              }
            ]}
            dados={orcamentos.map((orcamento) => ({
              'NumOrcamento': orcamento.OrcamentoID,
              'Fornecedor': orcamento.Entidade,
              'Valor': orcamento.Valor,
              'Descricao': orcamento.DescOrcamento,
              'CaminhoPDF': orcamento.CaminhoPDF
            }))}
            botoesOpcoes={[<Button  onClick={() => { setShowModal(true); setModalType('orcamento'); }} text={"Inserir Orçamento"}>Inserir Orçamento</Button>, 
            <Button onClick={() => { setShowModal(true); setModalType('votacao'); }} text={"Criar Votação"}>Criar Votação</Button>]}
          />
      </div>

      <Toaster />
    </div>
  );
};

export default Orcamentos;