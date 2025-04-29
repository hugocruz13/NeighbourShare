import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.js";

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

  useEffect(() => {
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

    fetchEntidades();
  }, []);

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
      if (!res.ok) {
        throw new Error('Erro ao registrar entidade.');
      }
      const data = await res.json();
      console.log(data);
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
        <div className='fundoEntidadesExternas'>
          <p className='p-entidadesExternas'>Entidades Externas</p>
          <button onClick={() => setShowModal(true)}>Adicionar Entidade</button>
          {entidades.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nome</th>
                  <th>Nif</th>
                  <th>Contacto</th>
                  <th>Email</th>
                  <th>Especialidade</th>
                </tr>
              </thead>
              <tbody>
                {entidades.map((entidade) => (
                  <tr key={entidade.EntidadeID}>
                    <td>{entidade.EntidadeID}</td>
                    <td>{entidade.Nome}</td>
                    <td>{entidade.Nif}</td>
                    <td>{entidade.Contacto}</td>
                    <td>{entidade.Email}</td>
                    <td>{entidade.Especialidade}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhuma entidade externa encontrada.</p>
          )}
        </div>

        {showModal && (
          <>
            <div className="modal-backdrop" onClick={() => setShowModal(false)} />
            <div className="modal-content">
              <h3>Adicionar Nova Entidade</h3>
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
                  <button type="button" onClick={() => setShowModal(false)}>Fechar</button>
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
