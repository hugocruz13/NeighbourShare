import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from '../components/Tabela.jsx';
import styles from '../components/Tabela.module.css';
import ModalForm from '../components/ModalForm.jsx'; 
import { motion } from 'framer-motion';
import Input from '../components/Input.jsx';
import Button from '../components/Button.jsx';
import { FaTrash, FaPen } from 'react-icons/fa';

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
    console.log('Submitting form with data:', novaEntidade);
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

      console.log('Entidade registrada com sucesso:', data);

      setEntidades((prevEntidades) => [...prevEntidades, data]);
      setUltimaEntidadeId(data.EntidadeID);

      toast.success('Entidade registrada com sucesso!', {
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
      toast.error('Erro ao registrar entidade.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
          <Tabela
              titulo={'Entidades Externas'}
              colunas={[
                { accessorKey: 'EntidadeID', header: 'ID' },
                { accessorKey: 'Nome', header: 'Nome' },
                { accessorKey: 'Nif', header: 'NIF' },
                { accessorKey: 'Contacto', header: 'Contacto' },
                { accessorKey: 'Email', header: 'Email' },
                { accessorKey: 'Especialidade', header: 'Especialidade' },
                {
                  accessorKey: 'Acao',
                  header: 'Ações',
                  cell: ({ row }) => (
                    <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                      <Button
                        variant="editar"
                        onClick={() => {}}
                      >
                        <FaPen color="white" size={18} />
                      </Button>
                      <Button
                        variant="eliminar"
                        onClick={() => {}}
                      >
                        <FaTrash color="white" size={18} />
                      </Button>
                    </div>
                  ),
                },
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
        <ToastContainer />
      </div>
  );
};

export default EntidadesExternas;
