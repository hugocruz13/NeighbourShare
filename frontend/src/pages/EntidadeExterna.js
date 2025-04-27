import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";

const EntidadeExterna = () => {
  const [entities, setEntities] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNewResource] = useState({
      Especialidade: '', 
      Contacto: '', 
      Email: '',
      Nome: '', 
      Nif: '',
  });

  useEffect(() => {
      const fetchUsers = async () => {
        try {
          const res = await fetch('http://localhost:8000/api/entidades/ver', {
            method: 'GET',
            credentials: 'include' ,
          });
  
          if (!res.ok) throw new Error('Erro ao buscar dados');
          const data = await res.json();
          console.log(data);
          setEntities(data);
        } catch (error) {
          console.error('Erro ao buscar entidades:', error);
        }
      };
  
      fetchUsers();
  }, []);

  const handleAddResource = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/entidades/registar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          Especialidade: newResource.Especialidade,
          Contacto: parseInt(newResource.Contacto),
          Email: newResource.Email,
          Nome: newResource.Nome,
          Nif: parseInt(newResource.Nif),
        }),
      });
  
      if (!res.ok) {
        const errorData = await res.json();
        console.error(errorData);
        throw new Error(errorData.detail || 'Erro ao adicionar recurso');
      }
  
      toast.success('Recurso adicionado com sucesso!');
      setShowModal(false);
  
      setNewResource({ 
        Especialidade: '', 
        Contacto: '', 
        Email: '', 
        Nome: '',
        Nif: '', 
      });
    } catch (error) {
      toast.error('Erro ao adicionar recurso: ' + error.message);
    }
  };
  





  return (
    <div className="page-content">
      <div className="home-container">
        <div className='fundoMeusRecursos'>
        <button className="btn-registarRecurso" onClick={() => setShowModal(true)}>Registar Entidade</button>

        {showModal && (
        <>
        <div className="modal-backdrop" onClick={() => setShowModal(false)} />
          <div className="modal-content">
            <h2>Registar Entidade</h2>
            <input type="text" placeholder="especialidade" value={newResource.Especialidade} onChange={(e) => setNewResource({ ...newResource, Especialidade: e.target.value })}/>
            <input type="number" placeholder="contacto" value={newResource.Contacto} onChange={(e) => setNewResource({ ...newResource, Contacto: e.target.value })}/>
            <input type="text" placeholder="email" value={newResource.Email} onChange={(e) => setNewResource({ ...newResource, Email: e.target.value })}/>
            <input type="text" placeholder="nome" value={newResource.Nome} onChange={(e) => setNewResource({ ...newResource, Nome: e.target.value })}/>
            <input type="number" placeholder="nif" value={newResource.Nif} onChange={(e) => setNewResource({ ...newResource, Nif: e.target.value })}/>
            <div>
              <button onClick={handleAddResource}>Adicionar</button>
              <button onClick={() => setShowModal(false)}>Cancelar</button>
            </div>
          </div>
        </>
        )}

        <p className='p-meusRecursos'>Entidade Externa</p>
        <table>
          <thead>
            <tr>
              <th>Nº Entidade</th>
              <th>Nome da entidade</th>
              <th>Especialidade</th>
              <th>Contacto</th>
              <th>Nif</th>
              <th>Ação</th>
            </tr>
          </thead>
          <tbody>
            {entities.map((entity) => (
            <tr key={entity.EntidadeID}>
              <td>{entity.EntidadeID}</td>
              <td>{entity.Nome}</td>
              <td>{entity.Especialidade}</td>
              <td>{entity.Contacto}</td>
              <td>{entity.Nif}</td>
              <td>
                <button>Selecionar</button>
              </td>
            </tr>
            ))}
          </tbody>
        </table>

      </div>
    </div>


      


      
    </div>
  );
};

export default EntidadeExterna;
