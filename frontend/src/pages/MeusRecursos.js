import React, { useEffect, useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";
import Navbar2 from "../components/Navbar2.jsx";
import Button from '../components/Button.jsx';
import Tabela from '../components/Tabela.jsx'; // importando tabela
import { FaTrash, FaPen, FaCheck, FaTimes } from 'react-icons/fa';

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

  const handleAddResource = async () => {
    const formData = new FormData();
    formData.append('nome_recurso', newResource.nome_recurso);
    formData.append('descricao_recurso', newResource.descricao_recurso);
    formData.append('caucao_recurso', newResource.caucao_recurso);
    formData.append('recurso_disponivel', newResource.recurso_disponivel);
    formData.append('categoria_recurso', newResource.categoria_recurso);  
    formData.append('fotos_recurso', newResource.fotos_recurso);

    try {
      const res = await fetch('http://localhost:8000/api/recursos/inserir', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      if (!res.ok) throw new Error('Erro ao adicionar recurso');

      toast.success('Recurso adicionado com sucesso!');
      setShowModal(false);

      setNewResource({ 
        nome_recurso: '', 
        descricao_recurso: '', 
        caucao_recurso: '', 
        recurso_disponivel: '',
        categoria_recurso: '', 
        fotos_recurso: null,
      });
    } catch (error) {
      toast.error('Erro ao adicionar recurso: ' + error.message);
    }
  };

  const handleFileChange = (e) => {
    setNewResource({ ...newResource, fotos_recurso: e.target.files[0] });
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

          {showModal && (
            <>
              <div className="modal-backdrop" onClick={() => setShowModal(false)} />
              <div className="modal-content">
                <h2>Adicionar Recurso</h2>
                <input type="text" placeholder="Nome do Recurso" value={newResource.nome_recurso} onChange={(e) => setNewResource({ ...newResource, nome_recurso: e.target.value })}/>
                <textarea placeholder="Descrição" value={newResource.descricao_recurso} onChange={(e) => setNewResource({ ...newResource, descricao_recurso: e.target.value })}/>
                <input type="text" placeholder="Caução" value={newResource.caucao_recurso} onChange={(e) => setNewResource({ ...newResource, caucao_recurso: e.target.value })}/>
                <select className='input-style' value={newResource.recurso_disponivel} onChange={(e) => setNewResource({ ...newResource, recurso_disponivel: e.target.value })}>
                  <option value="">Disponível?</option>
                  <option value="Disponível">Disponível</option>
                  <option value="Indisponível">Indisponível</option>
                </select>
                <select className='input-style' value={newResource.categoria_recurso} onChange={(e) => setNewResource({ ...newResource, categoria_recurso: e.target.value })}>
                  <option value="">Selecione a Categoria</option>
                  <option value="Lazer">Lazer</option>
                  <option value="Tecnologia">Tecnologia</option>
                  <option value="Ferramentas">Ferramentas</option>
                  <option value="Cozinha">Cozinha</option>
                  <option value="Outros">Outros</option>
                </select>
                <input type="file" onChange={handleFileChange} />
                <div>
                  <button onClick={handleAddResource}>Adicionar</button>
                  <button onClick={() => setShowModal(false)}>Cancelar</button>
                </div>
              </div>
            </>
          )}
          <Tabela
            titulo="Meus Recursos"
            colunas={colunas}
            dados={recursos}
            botoesOpcoes={[<Button className='btn-registarRecurso' onClick={() => setShowModal(true)} text={"Adicionar Recurso"}>Adicionar Recurso</Button>]}
          />

      </div>
      <ToastContainer />
    </div>
  );
};

export default MeusRecursos;
