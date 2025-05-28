import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from '../components/Tabela.jsx';
import ModalForm from '../components/ModalForm.jsx'; 
import Input from '../components/Input.jsx';
import Button from '../components/Button.jsx';
import { FaTrash, FaPen, FaCheck, FaTimes } from 'react-icons/fa';

const EntidadesExternas = () => {
  const [entidades, setEntidades] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [novaEntidade, setNovaEntidade] = useState({
    Especialidade: '',
    Contacto: '',
    Email: '',
    Nome: '',
    Nif: ''
  });
  const [ultimaEntidadeId, setUltimaEntidadeId] = useState(null);
    
  const [editId, setEditId] = useState(null);
  const [editData, setEditData] = useState({});
  
  const fetchEntidades = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/entidades/ver', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
        setEntidades(data);
      } catch (error) {
        console.error('Erro ao buscar entidades externas:', error);
      }
    };
  
  useEffect(() => {
    fetchEntidades();
  },[]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNovaEntidade({ ...novaEntidade, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/entidades/registar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(novaEntidade)
      });
      if (!res.ok) throw new Error('Erro ao registrar entidade.');
      
      const data = await res.json();

      setEntidades((prevEntidades) => [...prevEntidades, data]);
      setUltimaEntidadeId(data.EntidadeID);

      ToastManager.success('Entidade registrada com sucesso!', {
        autoClose: 2500
      });
      setShowModal(false);
      setNovaEntidade({
        Especialidade: '',
        Contacto: '',
        Email: '',
        Nome: '',
        Nif: ''
      });
      
    } catch (error) {
      console.error('Erro ao registrar entidade:', error);
      ToastManager.error('Erro ao registrar entidade.');
    }
  };

  const handleEditClick = (entidade) => {
    setEditId(entidade.EntidadeID);
    setEditData({ ...entidade });
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditData(prev => ({ ...prev, [name]: value }));
    // Coloca o foco no campo editado após renderização
    setTimeout(() => {
      const input = document.querySelector(`input[name="${name}"]`);
      if (input) input.focus();
    }, 0);
  };

  const handleCancelEdit = () => {
    setEditId(null);
    setEditData({});
  };

  const handleSaveEdit = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/entidades/update/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(editData)
      });
      if (!res.ok) throw new Error('Erro ao atualizar entidade.');
      
      // Atualiza o estado local com os dados editados
      setEntidades(prev => prev.map(ent =>
        ent.EntidadeID === editId ? editData : ent
      ));

      ToastManager.success('Entidade atualizada com sucesso!');
      setEditId(null);
      setEditData({});
    } catch (error) {
      console.error('Erro ao atualizar entidade:', error);
      ToastManager.error('Erro ao atualizar entidade.');
    }
  };

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/entidades/eliminar/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Erro ao remover a entidade.');
      setEntidades(prev => prev.filter(ent => ent.EntidadeID !== id));
      ToastManager.success('Entidade removida com sucesso!');
    } catch (error) {
      console.error('Erro ao remover a entidade:', error);
      ToastManager.error('Erro ao remover a entidade.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
          <Tabela
              titulo={'Entidades Externas'}
              colunas={[
                { 
                  accessorKey: 'Nome', 
                  header: 'Nome',
                  cell: ({ row }) => {
                    const entidade = row.original;
                    return editId === entidade.EntidadeID ? (
                      <Input
                        type="text"
                        name="Nome"
                        value={editData.Nome}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : entidade.Nome;
                  }
                },
                { 
                  accessorKey: 'Nif', 
                  header: 'NIF',
                  cell: ({ row }) => {
                    const entidade = row.original;
                    return editId === entidade.EntidadeID ? (
                      <Input
                        type="text"
                        name="Nif"
                        value={editData.Nif}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : entidade.Nif;
                  }
                },
                { 
                  accessorKey: 'Contacto', 
                  header: 'Contacto',
                  cell: ({ row }) => {
                    const entidade = row.original;
                    return editId === entidade.EntidadeID ? (
                      <Input
                        type="text"
                        name="Contacto"
                        value={editData.Contacto}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : entidade.Contacto;
                  }
                },
                { 
                  accessorKey: 'Email', 
                  header: 'Email',
                  cell: ({ row }) => {
                    const entidade = row.original;
                    return editId === entidade.EntidadeID ? (
                      <Input
                        type="email"
                        name="Email"
                        value={editData.Email}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : entidade.Email;
                  }
                },
                { 
                  accessorKey: 'Especialidade', 
                  header: 'Especialidade',
                  cell: ({ row }) => {
                    const entidade = row.original;
                    return editId === entidade.EntidadeID ? (
                      <Input
                        type="text"
                        name="Especialidade"
                        value={editData.Especialidade}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : entidade.Especialidade;
                  }
                },
                {
                  accessorKey: 'Acao',
                  header: 'Ações',
                  cell: ({ row }) => {
                    const entidade = row.original;
                    if (editId === entidade.EntidadeID) {
                      // Botões confirmar e cancelar na edição
                      return (
                        <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                          <Button variant="green" onClick={handleSaveEdit}>
                            <FaCheck color="white" size={18} />
                          </Button>
                          <Button variant="red" onClick={handleCancelEdit}>
                            <FaTimes color="white" size={18} />
                          </Button>
                        </div>
                      );
                    }
                    // Botões padrão (editar e excluir)
                    return (
                      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                        <Button variant="editar" onClick={() => handleEditClick(entidade)}>
                          <FaPen color="white" size={18} />
                        </Button>
                        <Button variant="eliminar" onClick={() => handleDelete(entidade.EntidadeID)}>
                          <FaTrash color="white" size={18} />
                        </Button>
                      </div>
                    );
                  }
                }
              ]}
            dados={entidades}
            destaqueId={ultimaEntidadeId}
            botoesOpcoes={[<Button key="1" onClick={setShowModal}>Adicionar Entidade Externa</Button>]}
          />
        </div>
        
        <ModalForm
            show={showModal}
            onclose={() => setShowModal(false)}
            title="Nova Entidade Externa"
            fields={[
              { label: 'Nome', name: 'Nome', type: 'text', required: true },
              { label: 'Especialidade', name: 'Especialidade', type: 'text', required: true },
              { label: 'Contacto', name: 'Contacto', type: 'text', required: true },
              { label: 'Email', name: 'Email', type: 'email', required: true },
              { label: 'NIF', name: 'Nif', type: 'text', required: true },
            ]}
            formData={novaEntidade}
            onChange={handleInputChange}
            onSubmit={handleSubmit}
            textBotao={'Adicionar Entidade Externa'}
          />       
        <Toaster />
      </div>
  );
};

export default EntidadesExternas;
