import React, { useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";
import Navbar2 from "../components/Navbar2.jsx";
import Button from '../components/Button.jsx';
import Tabela from '../components/Tabela.jsx'; // importando tabela
import { FaTrash, FaPen, FaCheck, FaTimes } from 'react-icons/fa';
import ModalForm from '../components/ModalForm.jsx';
import Input from '../components/Input.jsx';
import Select from '../components/Select.jsx';

const MeusRecursos = () => {
  const [recursos, setRecursos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [disponibilidades, setDisponibilidades] = useState([]);
  const [erro, setErro] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNewResource] = useState({
    nome_recurso: '', 
    descricao_recurso: '', 
    caucao_recurso: '',
    recurso_disponivel: '', 
    categoria_recurso: '', 
    foto_recurso: null,
  });
  const [editData, setEditData] = useState({});
  const [editId, setEditId] = useState(null);

  useEffect(() => {
    const fetchRecursosPessoais = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/pessoais', {
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Erro ao buscar dados');
        const data = await res.json();
        console.log(data);
        setRecursos(data);
      } catch (error) {
        setErro(error.message);
      }
    };
    const fetchCategorias = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/categorias', {
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Erro ao buscar categorias');
        const categorias = await res.json();
        setCategorias(categorias);
        console.log(categorias);
      } catch (error) {
        setErro(error.message);
      }
    };
    const fetchDisponibilidade = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/disponibilidades', {
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Erro ao buscar disponibilidades');
        const disponibilidades = await res.json();
        setDisponibilidades(disponibilidades);
        console.log(disponibilidades);
      } catch (error) {
        setErro(error.message);
      }
    };
    fetchDisponibilidade();
    fetchCategorias();
    fetchRecursosPessoais();
  }, [], [], []);

   const handleAddResource = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('nome_recurso', newResource.nome_recurso);
    formData.append('descricao_recurso', newResource.descricao_recurso);
    formData.append('caucao_recurso', newResource.caucao_recurso);
    formData.append('recurso_disponivel', newResource.recurso_disponivel);
    formData.append('categoria_recurso', newResource.categoria_recurso);  
    formData.append('fotos_recurso', newResource.imagem);
    try {
      const res = await fetch('http://localhost:8000/api/recursos/inserir', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      console.log(res.text());
      if (!res.ok) throw new Error('Erro ao adicionar recurso');

      ToastManager.success('Recurso adicionado com sucesso!');
      setShowModal(false);

      setNewResource({ 
        nome_recurso: '', 
        descricao_recurso: '', 
        caucao_recurso: '', 
        recurso_disponivel: '',
        categoria_recurso: '', 
        fotos_recurso: null,
      });

      const refreshRes = await fetch('http://localhost:8000/api/recursos/pessoais', {
        credentials: 'include',
      });
      if (refreshRes.ok) {
        const updatedRecursos = await refreshRes.json();
        setRecursos(updatedRecursos);
      }
    } catch (error) {
      ToastManager.error('Erro ao adicionar recurso: ' + error.message);
    }
  };

  const handleFileChange = (e) => {
    setNewResource({ ...newResource, imagem: e.target.files[0] });
  };

  const handleInputChange = (e) => {
    if (e.target.type === 'file') {
      handleFileChange(e);
    } else {
      setNewResource({ ...newResource, [e.target.name]: e.target.value });
    }
  };

const handleEditClick = (recurso) => {
  setEditId(recurso.RecursoID);
  setEditData({
    ...recurso
  });
};

  const handleCancelEdit = () => {
    setEditId(null);
    setEditData({});
  };

  const handleEditChange = (e) => {
    if (e && e.target) {
      console.log('handleEditChange:', e.target);
      const { name, value, type, files } = e.target;

      if (type === 'file') {
        setEditData(prev => ({ ...prev, imagem: files[0] }));
      } else {

        setEditData(prev => ({ ...prev, [name]: value }));

        //Para atribuir o valor correto ao campo de categoria e disponibilidade
        if (name === 'DescCategoria') {
          setEditData(prev => ({ ...prev, Categoria_: { label: value, value: value } }));
        } else if (name === 'DescDisponibilidade') {
          setEditData(prev => ({ ...prev, Disponibilidade_: { label: value, value: value }}));
        }
        
        setTimeout(() => {
          const input = document.querySelector(`input[name="${name}"]`);
          if (input) input.focus();
        }, 0);
      }
    } else {
      console.warn('Formato inesperado em handleEditChange:', e);
    }
  };




  const handleSaveEdit = async (recurso_comum_id) => {
    console.log('handleSaveEdit:', editData);
    if (
      !editData.Nome ||
      !editData.Descricao ||
      !editData.Caucao ||
      !editData.DescCategoria ||
      !editData.DescDisponibilidade ||
      !editData.imagem
    ) {
      ToastManager.error('Todos os campos são obrigatórios!');
      return;
    }
      const formData = new FormData();
      formData.append('id', recurso_comum_id);
      formData.append('nome', editData.Nome);
      formData.append('descricao', editData.Descricao);
      formData.append('caucao', editData.Caucao);
      formData.append('categoria', editData.DescCategoria || '');
      formData.append('disponivel', editData.DescDisponibilidade || '');
      formData.append('foto', editData.imagem);
    try {
      const res = await fetch(`http://localhost:8000/api/recursos/update/`, {
        method: 'PUT',
        credentials: 'include',
        body: formData,
      });
      if (!res.ok) throw new Error('Erro ao atualizar recurso.');

      const refreshRes = await fetch('http://localhost:8000/api/recursos/pessoais', {
        credentials: 'include',
      });
      if (refreshRes.ok) {
        const updatedRecursos = await refreshRes.json();
        setRecursos(updatedRecursos);
      }

      ToastManager.success('Recurso atualizado com sucesso!');
      setEditId(null);
      setEditData({});
    } catch (error) {
      console.error('Erro ao atualizar recurso:', error);
      ToastManager.error('Erro ao atualizar recurso.');
    }
  };

  const handleDelete = async (recurso_id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/recursos/${recurso_id}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      
      if (!res.ok) throw new Error('Erro ao remover a recurso.');
      
      const refreshRes = await fetch('http://localhost:8000/api/recursos/pessoais', {
        credentials: 'include',
      });
      if (refreshRes.ok) {
        const updatedRecursos = await refreshRes.json();
        setRecursos(updatedRecursos);
      }

      ToastManager.success('Recurso removido com sucesso!');
    } catch (error) {
      console.error('Erro ao remover o recurso:', error);
      ToastManager.error('Erro ao remover o recurso.');
    }
  };

  // Definindo colunas para o componente Tabela
  const colunas = [
      {
        header: 'Imagem',
        accessorKey: 'Image',
        cell: ({ row }) => {
          const recurso = row.original;
          return editId === recurso.RecursoID ? (
            <>
              <Input
                type="file"
                name="imagem"
                onChange={handleEditChange}
                variant="default"
                accept="image/*"
              />
              {editData.imagem && (
                <img
                  src={URL.createObjectURL(editData.imagem)}
                  alt="Preview"
                  style={{ width: 90, height: 90, borderRadius: '50%', objectFit: 'cover', marginTop: '8px' }}
                />
              )}
            </>
          ) : (
            <img
              src={recurso.Image}
              alt="Recurso"
              style={{
                width: 90,
                height: 90,
                borderRadius: '50%',
                objectFit: 'cover',
              }}
            />
          );
        }
      },
      {
        header: 'Nome do Recurso',
        accessorKey: 'Nome',
        cell: ({ row }) => {
          const recurso = row.original;
          return editId === recurso.RecursoID ? (
            <Input
              type="text"
              name="Nome"
              value={editData.Nome}
              onChange={handleEditChange}
              variant="default"
            />
          ) : recurso.Nome;
        }
      },
      {
        header: 'Descrição',
        accessorKey: 'Descricao',
        cell: ({ row }) => {
          const recurso = row.original;
          return editId === recurso.RecursoID ? (
            <Input
              type="text"
              name="Descricao"
              value={editData.Descricao}
              onChange={handleEditChange}
              variant="default"
            />
          ) : recurso.Descricao;
        }
      },
      {
        header: 'Caução',
        accessorKey: 'Caucao',
        cell: ({ row }) => {
          const recurso = row.original;
          return editId === recurso.RecursoID ? (
            <Input
              type="number"
              name="Caucao"
              value={editData.Caucao}
              onChange={handleEditChange}
              variant="default"
            />
          ) : new Intl.NumberFormat('pt-PT', { style: 'currency', currency: 'EUR' }).format(recurso.Caucao);
        }
      },
      {
        header: 'Categoria',
        accessorKey: 'Categoria_.DescCategoria',
        cell: ({ row }) => {
          const recurso = row.original;
          return editId === recurso.RecursoID ? (
            <Select
              name="DescCategoria"
              onChange={handleEditChange}
              options={categorias.map(cat => ({ label: cat.DescCategoria, value: cat.DescCategoria}))}
              variant="default"
              value={editData.Categoria_ || null}
            />
          ) : recurso.Categoria_?.DescCategoria;
        }
      },
      {
        header: 'Disponibilidade',
        accessorKey: 'Disponibilidade_.DescDisponibilidade',
        cell: ({ row }) => {
          const recurso = row.original;
          return editId === recurso.RecursoID ? (
            <Select
              name="DescDisponibilidade"
              onChange={handleEditChange}
              options={disponibilidades.map(disp => ({ label: disp.DescDisponibilidade, value: disp.DescDisponibilidade }))}
              variant="default"
              value={editData.Disponibilidade_ || null}
            />
          ) : recurso.Disponibilidade_?.DescDisponibilidade;
        }
      },
      {
        header: 'Ações',
        accessorKey: 'Acoes',
        cell: ({ row }) => {
          const recurso = row.original;
          if (editId === recurso.RecursoID) {
            return (
              <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                <Button variant="green" onClick={() => handleSaveEdit(recurso.RecursoID)}>
                  <FaCheck color="white" size={18} />
                </Button>
                <Button variant="red" onClick={handleCancelEdit}>
                  <FaTimes color="white" size={18} />
                </Button>
              </div>
            );
          }
          return (
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
              <Button variant="editar" onClick={() => handleEditClick(recurso)}>
                <FaPen color="white" size={18} />
              </Button>
              <Button variant="eliminar" onClick={() => handleDelete(recurso.RecursoID)}>
                <FaTrash color="white" size={18} />
              </Button>
            </div>
          );
        }
      }
    ];

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">

          <ModalForm
            show={showModal}
            onclose={() => setShowModal(false)}
            onSubmit={handleAddResource}
            title="Adicionar Recurso Pessoal"
            fields={[
              { name: 'nome_recurso', label: 'Nome do Recurso', type: 'text', required: true },
              { name: 'descricao_recurso', label: 'Descrição', type: 'textarea', required: true },
              { name: 'caucao_recurso', label: 'Caução', type: 'number', required: true },
              {
                name: 'recurso_disponivel',
                label: 'Disponível?',
                type: 'select',
                required: true,
                options: disponibilidades.map(disp => ({ label: disp.DescDisponibilidade, value: disp.DescDisponibilidade })),
              },
              {
                name: 'categoria_recurso',
                label: 'Categoria',
                type: 'select',
                required: true,
                options: categorias.map(cat => ({ label: cat.DescCategoria, value: cat.DescCategoria })),
              },
              { name: 'imagem', label: 'Imagem', type: 'image', required: true },
            ]}
            formData={newResource}
            onChange={handleInputChange}
            textBotao="Adicionar"
          />

          <Tabela
            titulo="Meus Recursos"
            colunas={colunas}
            dados={recursos}
            botoesOpcoes={[<Button className='btn-registarRecurso' onClick={() => setShowModal(true)} text={"Adicionar Recurso"}>Adicionar Recurso</Button>]}
          />

      </div>
      <Toaster />
    </div>
  );
};

export default MeusRecursos;
