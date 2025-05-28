import { useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { FaTrash, FaPen, FaCheck, FaTimes } from 'react-icons/fa';
import ToastManager from '../components/ToastManager.jsx';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import Button from '../components/Button.jsx';
import ModalForm from '../components/ModalForm.jsx';
import Input from '../components/Input.jsx';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";

const MeusRecursos = () => {
  const [recurso, setRecursos] = useState([]);
  const [erro, setErro] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNovoRecurso] = useState({
    nome_recurso: '', 
    descricao_recurso: '', 
    imagem: null,
  });

  const [editData, setEditData] = useState({});
  const [editId, setEditId] = useState(null);


  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns', {
          
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Erro ao buscar dados');
        const data = await res.json();
        setRecursos(data);
      } catch (error) {
        setErro(error.message);
      }
    };

    fetchUsers();
  }, []);

  const handleAddResource = async (e) => {
    e.preventDefault(); // Prevenir o comportamento padrão do formulário

    const formData = new FormData();
    formData.append('nome_recurso', newResource.nome_recurso);
    formData.append('descricao_recurso', newResource.descricao_recurso);
    formData.append('imagem', newResource.imagem);
    

    // Enviar os dados para a API
    try {
      const res = await fetch('http://localhost:8000/api/recursoscomuns/inserir', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      if (!res.ok) throw new Error('Erro ao adicionar recurso');

      ToastManager.success('Recurso adicionado com sucesso!');
      setShowModal(false);

      // Limpar campos após envio
      setNovoRecurso({ 
        nome_recurso: '', 
        descricao_recurso: '', 
        imagem: null,
      });

      // Recarregar a lista de recursos
      const refreshRes = await fetch('http://localhost:8000/api/recursoscomuns', {
        credentials: 'include',
      });
      if (refreshRes.ok) {
        const refreshData = await refreshRes.json();
        setRecursos(refreshData);
      }
    } catch (error) {
      ToastManager.error('Erro ao adicionar recurso: ' + error.message);
    }
  };

  const handleFileChange = (e) => {
    setNovoRecurso({ ...newResource, imagem: e.target.files[0] });
  };

  const handleInputChange = (e) => {
    if (e.target.type === 'file') {
      handleFileChange(e);
    } else {
      setNovoRecurso({ ...newResource, [e.target.name]: e.target.value });
    }
  };

  const handleEditClick = (recurso) => {
    setEditId(recurso.NumRecurso);
    setEditData({ ...recurso });
  };

  const handleCancelEdit = () => {
    setEditId(null);
    setEditData({});
  };

  const handleEditChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === 'file') {
      setEditData(prev => ({ ...prev, imagem: files[0] }));
    } else {
      setEditData(prev => ({ ...prev, [name]: value }));
      // Coloca o foco no campo editado após renderização
      setTimeout(() => {
        const input = document.querySelector(`input[name="${name}"]`);
        if (input) input.focus();
      }, 0);
    }
  };

  const handleSaveEdit = async (recurso_comum_id) => {
    if (
      !editData.NomeRecurso?.trim() || 
      !editData.Descricao?.trim()
    ) {
      ToastManager.error('Todos os campos são obrigatórios!');
      return;
    }
      const formData = new FormData();
      formData.append('nome_recurso', editData.NomeRecurso);
      formData.append('descricao_recurso', editData.Descricao);
      if (editData.imagem)
      {
        formData.append('imagem', editData.imagem);
      }
    try {
      const res = await fetch(`http://localhost:8000/api/recursoscomuns/update/${recurso_comum_id}`, {
        method: 'PUT',
        credentials: 'include',
        body: formData,
      });

      if (!res.ok) throw new Error('Erro ao atualizar recurso comum.');

      const refreshRes = await fetch('http://localhost:8000/api/recursoscomuns', {
        credentials: 'include',
      });
      if (refreshRes.ok) {
        const updatedRecursos = await refreshRes.json();
        setRecursos(updatedRecursos);
      }

      ToastManager.success('Recurso comum atualizado com sucesso!');
      setEditId(null);
      setEditData({});
    } catch (error) {
      console.error('Erro ao atualizar recurso:', error);
      ToastManager.error('Erro ao atualizar recurso.');
    }
  };

  const handleDelete = async (recurso_comum_id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/recursoscomuns/delete/${recurso_comum_id}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      const text = await res.text();
      const data = JSON.parse(text);
      if (!res.ok) throw new Error('Erro ao remover a recurso.');
      if (data.includes("Recurso comum numa pedido de manutenção ativo")) { ToastManager.error("Recurso comum num pedido de manutenção ativo"); return; }
      const refreshRes = await fetch('http://localhost:8000/api/recursoscomuns', {
        credentials: 'include',
      });
      if (refreshRes.ok) {
        const updatedRecursos = await refreshRes.json();
        setRecursos(updatedRecursos);
      }

      ToastManager.success('Recurso Comum removido com sucesso!');
    } catch (error) {
      console.error('Erro ao remover o recurso:', error);
      ToastManager.error('Erro ao remover o recurso.');
    }
  };


  return (
    <>
      <Navbar2 />
      <div className="home-container">
          {/* Botão para abrir o modal de adicionar recurso */} 
          {/* Modal de Adicionar Recurso */}          
          <ModalForm
            show={showModal}
            onclose={() => setShowModal(false)}
            onSubmit={handleAddResource}
            title="Adicionar Recurso Comum"
            fields={[
              { name: 'nome_recurso', label: 'Nome do Recurso', type: 'text', required: true },
              { name: 'descricao_recurso', label: 'Descrição', type: 'textarea', required: true },
              { name: 'imagem', label: 'Imagem', type: 'image', required: true },
            ]}
            formData={newResource}
            onChange={handleInputChange}
            textBotao="Adicionar"
          />
          <Tabela
            titulo={"Recursos Comuns"}
            botoesOpcoes={[
              <Button 
                key="add" 
                variant='default' 
                onClick={() => setShowModal(true)} 
                text={"Adicionar Recurso Comum"}
              >
                Adicionar Recurso Comum
              </Button>
            ]}
            colunas={[
              {
                header: 'Imagem',
                accessorKey: 'Path',
                cell: ({ row }) => {
                  const recurso = row.original;
                  return editId === recurso.NumRecurso ? (
                    <>
                      <Input
                        type="file"
                        name="imagem"
                        onChange={handleEditChange}
                        variant="default"
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
                      src={recurso.Path}
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
              { accessorKey: 'NumRecurso', header: 'Nº Recurso' },
              { 
                accessorKey: 'NomeRecurso', 
                header: 'Nome do Recurso',
                cell: ({ row }) => {
                    const recurso = row.original;
                    return editId === recurso.NumRecurso ? (
                      <Input
                        type="text"
                        name="NomeRecurso"
                        value={editData.NomeRecurso}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : recurso.NomeRecurso;
                  } },
              { accessorKey: 'Descricao', 
                header: 'Descrição',
                cell: ({ row }) => {
                    const recurso = row.original;
                    return editId === recurso.NumRecurso ? (
                      <Input
                        type="text"
                        name="Descricao"
                        value={editData.Descricao}
                        onChange={handleEditChange}
                        variant="default"
                      />
                    ) : recurso.Descricao;
                  },
              },
              {
                accessorKey: 'Acao',
                header: 'Ações',
                cell: ({ row }) => {
                  const recurso = row.original;
                  if (editId === recurso.NumRecurso) {
                    // Botões confirmar e cancelar na edição
                    return (
                      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                        <Button variant="green" onClick={() => handleSaveEdit(recurso.NumRecurso)}>
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
                      <Button variant="editar" onClick={() => handleEditClick(recurso)}>
                        <FaPen color="white" size={18} />
                      </Button>
                      <Button variant="eliminar" onClick={() => handleDelete(recurso.NumRecurso)}>
                        <FaTrash color="white" size={18} />
                      </Button>
                    </div>
                  );
                }
              }
            ]}
            dados={recurso.map((recurso) => ({
              NumRecurso: recurso.RecComumID,
              NomeRecurso: recurso.Nome,
              Descricao: recurso.DescRecursoComum,
              Path: recurso.Path,
            }))}
          />

      </div>
      <Toaster />
    </>
  );
  
};

export default MeusRecursos;
