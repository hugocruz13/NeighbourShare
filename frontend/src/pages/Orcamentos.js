import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
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
        console.log(data);
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

  const handleAddResource = async () => {
    try {
      const formData = new FormData();
      formData.append('id_entidade_externa', newResource.id_entidade_externa);
      formData.append('valor_orcamento', parseInt(newResource.valor_orcamento));
      formData.append('descricao_orcamento', newResource.descricao_orcamento);
      formData.append('pdforcamento', newResource.pdforcamento);
      formData.append('idprocesso', newResource.idprocesso);
      formData.append('tipoorcamento', newResource.tipoorcamento);

      const res = await fetch('http://localhost:8000/api/orcamentos/inserir', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Erro ao adicionar recurso');
      }

      toast.success('Recurso adicionado com sucesso!');
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
      toast.error('Erro ao adicionar recurso: ' + error.message);
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

      toast.success('Votação criada com sucesso!');
      setShowModal(false);
      setVotacao({
        titulo: '',
        descricao: '',
        id_processo: 0,
        data_fim: '',
        tipo_votacao: '',
      });
    } catch (error) {
      toast.error('Erro ao criar votação: ' + error.message);
    }
  };

  const handleFileChange = (e) => {
    setNewResource({ ...newResource, pdforcamento: e.target.files[0] });
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
              { name: 'tipoorcamento', label: 'Tipo Orçamento', type: 'text' },
              { name: 'pdforcamento', label: 'Arquivo', type: 'file' }
            ] : [
              { name: 'titulo', label: 'Título', type: 'text' },
              { name: 'descricao', label: 'Descrição', type: 'text' },
              { name: 'id_processo', label: 'ID do Processo', type: 'number' },
              { name: 'data_fim', label: 'Data de Fim', type: 'date' },
              { name: 'tipo_votacao', label: 'Tipo Votação', type: 'text' }
            ]}
            formData={modalType === 'orcamento' ? newResource : votacao}
            onChange={(e) => {
              const { name, value } = e.target;
              if (modalType === 'orcamento') {
                setNewResource({ ...newResource, [name]: value });
              } else {
                setVotacao({ ...votacao, [name]: value });
              }
            }}
            onSubmit={(e) => {
              e.preventDefault();
              if (modalType === 'orcamento') {
                handleAddResource();
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
              { accessorKey: 'Descricao', header: 'Descrição' }
            ]}
            dados={orcamentos.map((orcamento) => ({
              'Nº Orçamento': orcamento.OrcamentoID,
              'Fornecedor': orcamento.Entidade,
              'Valor': orcamento.Valor,
              'Descrição': orcamento.DescOrcamento,
            }))}
            botoesOpcoes={[<Button className={styles.btnregistarRecurso} onClick={() => { setShowModal(true); setModalType('orcamento'); }} text={"Inserir Orçamento"}>Inserir Orçamento</Button>, 
            <Button className={styles.btnregistarRecurso} onClick={() => { setShowModal(true); setModalType('votacao'); }} text={"Criar Votação"}>Criar Votação</Button>]}
          />
      </div>

      <ToastContainer />
    </div>
  );
};

export default Orcamentos;