import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";

const Orcamentos = () => {
  const [entities, setEntities] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNewResource] = useState({
      fornecedor_orcamento: '', 
      valor_orcamento: '', 
      descricao_orcamento: '',
      pdforcamento: null, 
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
      const res = await fetch('http://localhost:8000/api/orcamentos/inserir', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          fornecedor_orcamento: newResource.fornecedor_orcamento,
          valor_orcamento: parseInt(newResource.valor_orcamento),
          descricao_orcamento: newResource.descricao_orcamento,
          pdforcamento: newResource.pdforcamento,
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
        fornecedor_orcamento: '', 
        valor_orcamento: '', 
        descricao_orcamento: '', 
        pdforcamento: null,
      });
    } catch (error) {
      toast.error('Erro ao adicionar recurso: ' + error.message);
    }
  };
  

  const handleFileChange = (e) => {
    setNewResource({ ...newResource, pdforcamento: e.target.files[0] });
  };



  return (
    <div className="page-content">
      <div className="home-container">
        <div className='fundoMeusRecursos'>
          <button className="btn-registarRecurso" onClick={() => setShowModal(true)}>Inserir Orçamento</button>

          {showModal && (
          <>
          <div className="modal-backdrop" onClick={() => setShowModal(false)} />
          <div className="modal-content">
            <h2>Adicionar Orçamento</h2>
            <input type="text" placeholder="fornecedor" value={newResource.fornecedor_orcamento} onChange={(e) => setNewResource({ ...newResource, fornecedor_orcamento: e.target.value })}/>
            <input type="number" placeholder="valor" value={newResource.valor_orcamento} onChange={(e) => setNewResource({ ...newResource, valor_orcamento: e.target.value })}/>
            <input type="text" placeholder="descricao" value={newResource.descricao_orcamento} onChange={(e) => setNewResource({ ...newResource, descricao_orcamento: e.target.value })}/>
            <input type="file" onChange={handleFileChange} />
            <div>
              <button onClick={handleAddResource}>Adicionar</button>
              <button onClick={() => setShowModal(false)}>Cancelar</button>
            </div>
          </div>
          </>
          )}

          <p className='p-meusRecursos'>Orçamentos</p>
          <table>
            <thead>
              <tr>
                <th>Nº Entidade</th>
                <th>Nome da entidade</th>
                <th>Especialidade</th>
                <th>Contacto</th>
                <th>Nif</th>
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
              </tr>
              ))}
            </tbody>
          </table>

        </div>
      </div>


      


      
    </div>
  );
};

export default Orcamentos;
