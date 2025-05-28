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

const MeusRecursos = () => {
  const [recursos, setRecursos] = useState([]);
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

    fetchRecursosPessoais();
  }, []);

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

  // Definindo colunas para o componente Tabela
  const colunas = [
    {
      header: 'Imagem',
      accessorKey: 'Image', // Ajuste conforme seu dado
      cell: info => (
        <img 
        src={info.getValue()} // Ajuste conforme seu dado
          alt="Recurso"
          style={{
            width: 90,
            height: 90,
            borderRadius: '50%',
            objectFit: 'cover',
          }}
        />
      )
    },
    {
      header: 'Nome do Recurso',
      accessorKey: 'Nome'
    },
    {
      header: 'Caução',
      accessorKey: 'Caucao'
    },
    {
      header: 'Categoria',
      accessorKey: 'Categoria_.DescCategoria'
    },
    {
      header: 'Disponibilidade',
      accessorKey: 'Disponibilidade_.DescDisponibilidade'
    },
    {
      header: 'Ações',
      accessorKey: 'Acoes',
      cell: ({ row }) => (
        <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
          <Button variant="editar" onClick={() => {}}>
            <FaPen color="white" size={18} />
          </Button>
          <Button variant="eliminar" onClick={() => {}}>
            <FaTrash color="white" size={18} />
          </Button>
        </div>
      )
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
                options: [
                  { label: 'Disponível', value: 'Disponível' },
                  { label: 'Indisponível', value: 'Indisponível' },
                ],
              },
              {
                name: 'categoria_recurso',
                label: 'Categoria',
                type: 'select',
                required: true,
                options: [
                  { label: 'Lazer', value: 'Lazer' },
                  { label: 'Tecnologia', value: 'Tecnologia' },
                  { label: 'Ferramentas', value: 'Ferramentas' },
                  { label: 'Cozinha', value: 'Cozinha' },
                  { label: 'Outros', value: 'Outros' },
                ],
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
