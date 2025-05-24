import React, { useEffect, useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import Button from '../components/Button.jsx';
import ModalForm from '../components/ModalForm.jsx';
import Modal from '../components/ModalForm.jsx';

const MeusRecursos = () => {
  const [recurso, setUsers] = useState([]);
  const [erro, setErro] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNewResource] = useState({
    nome_recurso: '', 
    descricao_recurso: '', 
    imagem: null,
  });


  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns', {
          
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Erro ao buscar dados');
        const data = await res.json();
        console.log(data);
        setUsers(data);
      } catch (error) {
        setErro(error.message);
      }
    };

    fetchUsers();
  }, []);

  const handleAddResource = async () => {

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

      toast.success('Recurso adicionado com sucesso!');
      setShowModal(false);

      setNewResource({ 
        nome_recurso: '', 
        descricao_recurso: '', 
        imagem: null,
      }); // Limpar campos após envio
    } catch (error) {
      toast.error('Erro ao adicionar recurso: ' + error.message);
    }
  };

  const handleFileChange = (e) => {
    setNewResource({ ...newResource, imagem: e.target.files[0] });
  };


  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
          {/* Botão para abrir o modal de adicionar recurso */} 
          {/* Modal de Adicionar Recurso */}
          <ModalForm
            show={showModal}
            onClose={() => setShowModal(false)}
            onSubmit={handleAddResource}
            title="Adicionar Recurso Comum"
            fields={[
              { name: 'nome_recurso', label: 'Nome do Recurso', type: 'text', required: true },
              { name: 'descricao_recurso', label: 'Descrição', type: 'textarea', required: true },
              { name: 'imagem', label: 'Imagem', type: 'file', required: true },
            ]}
            formData={newResource}
            onChange={(e) => setNewResource({ ...newResource, [e.target.name]: e.target.value })}
            textBotao="Adicionar"
          />
          <Tabela
            titulo={"Recursos Comuns"}
            botoesOpcoes={[<Button variant='default' onClick={() => setShowModal(true)} text={"Adicionar Recurso Comum"}>Adicionar Recurso Comum</Button>]}
            colunas = {[
            {
              header: 'Imagem',
              accessorKey: 'Path',
              cell: info => (
                <img 
                src={info.getValue()} 
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
            { accessorKey: 'NumRecurso', header: 'Nº Recurso' },
            { accessorKey: 'NomeRecurso', header: 'Nome do Recurso' },
            { accessorKey: 'Descricao', header: 'Descrição' },
          ]} 
            dados={recurso.map((recurso) => ({
              'NumRecurso': recurso.RecComumID,
              'NomeRecurso': recurso.Nome,
              'Descricao': recurso.DescRecursoComum,
              'Path': recurso.Path,
            }))}
          />
      </div>
      <ToastContainer />
    </div>
  );
  
};

export default MeusRecursos;
