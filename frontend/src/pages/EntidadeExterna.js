import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from '../components/Tabela.jsx';
import ModalForm from '../components/ModalForm.jsx'; 
import { motion } from 'framer-motion';
import Input from '../components/Input.jsx';

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
        <div className={styles.fundo}>
          <p className={styles.titulo}>Entidades Externas</p>
            <button
              onClick={() => setShowModal(true)}
              className={styles.btnRegistar}
            >
              Adicionar Entidade
            </button>
          <Tabela
              colunas={[
                { accessorKey: 'EntidadeID', header: 'ID' },
                { accessorKey: 'Nome', header: 'Nome' },
                { accessorKey: 'Nif', header: 'NIF' },
                { accessorKey: 'Contacto', header: 'Contacto' },
                { accessorKey: 'Email', header: 'Email' },
                { accessorKey: 'Especialidade', header: 'Especialidade' },
                {accessorKey: 'Acao',header: 'Ações'},/*, cell: ({ row }) => (
                  <button
                    onClick={() => {
                      const id = row.original.EntidadeID;
                      // Implementar a lógica para editar ou excluir a entidade
                      console.log(`Editar ou excluir entidade com ID: ${id}`);
                    }}
                  >
                    Editar/Excluir
                  </button>
                )}*/
              ]}
            dados={entidades}
            destaqueId={ultimaEntidadeId}
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
          />       
        <ToastContainer />
      </div>
    </div>
  );
};

export default EntidadesExternas;
