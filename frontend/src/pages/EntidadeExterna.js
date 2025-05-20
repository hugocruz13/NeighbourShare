import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from '../components/Tabela.jsx';


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
      toast.success('Entidade registrada com sucesso!');
      setShowModal(false);
      setNovaEntidade({
        Especialidade: '',
        Contacto: '',
        Email: '',
        Nome: '',
        Nif: ''
      });
      setEntidades([...entidades, data]);
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
          />
        </div>

        {showModal && (
          <>
            <div
              className={styles.modalbackdrop}
              onClick={() => setShowModal(false)}
            />
            <div className={styles.modalcontent}>
              <h3 className={styles.titulo}>Adicionar Nova Entidade</h3>
              <form onSubmit={handleSubmit}>
                <label>
                  Nome:
                  <input
                    type="text"
                    name="Nome"
                    value={novaEntidade.Nome}
                    onChange={handleInputChange}
                    required
                  />
                </label>
                <label>
                  Especialidade:
                  <input
                    type="text"
                    name="Especialidade"
                    value={novaEntidade.Especialidade}
                    onChange={handleInputChange}
                    required
                  />
                </label>
                <label>
                  Contato:
                  <input
                    type="text"
                    name="Contacto"
                    value={novaEntidade.Contacto}
                    onChange={handleInputChange}
                    required
                  />
                </label>
                <label>
                  Email:
                  <input
                    type="email"
                    name="Email"
                    value={novaEntidade.Email}
                    onChange={handleInputChange}
                    required
                  />
                </label>
                <label>
                  NIF:
                  <input
                    type="text"
                    name="Nif"
                    value={novaEntidade.Nif}
                    onChange={handleInputChange}
                    required
                  />
                </label>
                <div>
                  <button type="submit">Registrar</button>
                  <button type="button" onClick={() => setShowModal(false)}>
                    Fechar
                  </button>
                </div>
              </form>
            </div>
          </>
        )}
        <ToastContainer />
      </div>
    </div>
  );
};

export default EntidadesExternas;
