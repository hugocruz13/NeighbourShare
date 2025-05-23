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
  const [newResource, setNewResource] = useState({
    id_entidade_externa: '',
    valor_orcamento: '',
    descricao_orcamento: '',
    pdforcamento: null,
    idprocesso: '',
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

  useEffect(() => {
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

    fetchOrcamentos();
    fetchFornecedores();
  }, []);

  const handleAddOrcamento = async () => {
    try {

      if (!newResource.id_entidade_externa || isNaN(parseInt(newResource.id_entidade_externa))) {
            ToastManager.error('ID da entidade externa deve ser um número válido');
            return;
          }
          
          if (!newResource.valor_orcamento || isNaN(parseFloat(newResource.valor_orcamento))) {
            ToastManager.error('Valor do orçamento deve ser um número válido');
            return;
          }
          
          if (!newResource.idprocesso || isNaN(parseInt(newResource.idprocesso))) {
            ToastManager.error('ID do processo deve ser um número válido');
            return;
          }
          
          if (!newResource.tipoorcamento) {
            ToastManager.error('Tipo de orçamento é obrigatório');
            return;
          }
          
          if (!newResource.pdforcamento) {
            ToastManager.error('Arquivo PDF é obrigatório');
            return;
          }

      const formData = new FormData();

      formData.append('id_entidade_externa', parseInt(newResource.id_entidade_externa).toString());
      formData.append('valor_orcamento', parseFloat(newResource.valor_orcamento).toString());
      formData.append('descricao_orcamento', newResource.descricao_orcamento);
      formData.append('pdforcamento', newResource.pdforcamento);
      formData.append('idprocesso', parseInt(newResource.idprocesso).toString());
      formData.append('tipoorcamento', newResource.tipoorcamento);

      const tipoMapping = {
        'Manutenção': 'MANUTENCAO',
        'Aquisição': 'AQUISICAO'
      };
      const tipoFinal = tipoMapping[newResource.tipoorcamento] || newResource.tipoorcamento;
      formData.append('tipoorcamento', tipoFinal);

      const res = await fetch('http://localhost:8000/api/orcamentos/inserir', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Erro ao adicionar recurso');
      }

      ToastManager.success('Recurso adicionado com sucesso!');
      setShowModal(false);
      setNewResource({
        id_entidade_externa: '',
        valor_orcamento: '',
        descricao_orcamento: '',
        pdforcamento: null,
        idprocesso: '',
        tipoorcamento: ''
      });
    } catch (error) {
      
      console.error('Erro ao adicionar recurso:', error);
      ToastManager.error('Erro ao adicionar recurso: ' + error.message);
    }
  };

  const handleCreateVotacao = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/criarvotacao', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(votacao),
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
        id_processo: 0,
        data_fim: '',
        tipo_votacao: '',
      });
    } catch (error) {
      ToastManager.error('Erro ao criar votação: ' + error.message);
    }
  };

  const handleChange = (e) => {
    const { name, value, files, type } = e.target;

    if (modalType === 'orcamento') {
      if (type === 'file') {
        const file = files?.[0];
        if (file) {
          setNewResource(prev => ({ ...prev, [name]: file }));
        }
      } else {
        setNewResource(prev => ({ ...prev, [name]: value }));
      }
    } else {
      setVotacao(prev => ({ ...prev, [name]: value }));
    }
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
              { name: 'idprocesso', label: 'ID Processo', type: 'text' },
              { name: 'tipoorcamento', label: 'Tipo Orçamento', type: 'select', options:[{value: 'Manutenção', label:'Manutenção'}, {value: 'Aquisição', label: 'Aquisição'}] },
              { name: 'pdforcamento', label: 'Arquivo', type: 'file' }
            ] : [
              { name: 'titulo', label: 'Título', type: 'text' },
              { name: 'descricao', label: 'Descrição', type: 'text' },
              { name: 'id_processo', label: 'ID do Processo', type: 'number' },
              { name: 'data_fim', label: 'Data de Fim', type: 'date' },
              { name: 'tipo_votacao', label: 'Tipo Votação', type: 'select', options:[{value: 'Manutenção', label:'Manutenção'}, {value: 'Aquisição', label: 'Aquisição'}] }
            ]}
            formData={modalType === 'orcamento' ? newResource : votacao}
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
              { accessorKey: 'PDF', header: 'PDF' }
            ]}
            dados={orcamentos.map((orcamento) => ({
              'Nº Orçamento': orcamento.OrcamentoID,
              'Fornecedor': orcamento.Entidade,
              'Valor': orcamento.Valor,
              'Descrição': orcamento.DescOrcamento,
              'PDF': <Button variant='defaultTabela' onClick={() => {}}text={"Download"}>Download</Button>
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