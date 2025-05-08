import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Tabela from '../components/Tabela';

const ConsultarVotacao = () => {
  const { id } = useParams();
  const [orcamentos, setOrcamentos] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showModal2, setShowModal2] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);
  const [newResource, setNewResource] = useState({ nome_recurso: '' });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrcamentos = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/votacoes/${id}/orcamentos`);
        const data = await res.json();
        setOrcamentos(data);
      } catch (error) {
        console.error('Erro ao buscar orçamentos:', error);
      }
    };

    fetchOrcamentos();
  }, [id]);

  const handleConsultarClick = (pedido) => {
    setPedidoAtual(pedido);
    setShowModal2(true);
  };

  const colunas = [
    'Opção',
    'Entidade',
    'Recurso',
    'Descrição',
    'Data',
    'Valor',
    'Ação'
  ]

  return (
    <div>
      <h1>Orçamentos a Avaliar</h1>

      {/* Botão para abrir o modal de votar */}
      <button className="btn-registarRecurso" onClick={() => setShowModal(true)}>Votar</button>

      {showModal && (
        <>
          <div className="modal-backdrop" onClick={() => setShowModal(false)} />
          <div className="modal-content">
            <h2>Votar</h2>
            <input type="text" placeholder="Selecionar Opção " value={newResource.nome_recurso} onChange={(e) => setNewResource({ ...newResource, nome_recurso: e.target.value })}/>
            <div>
              <button>Votar</button>
              <button onClick={() => setShowModal(false)}>Cancelar</button>
            </div>
          </div>
        </>
      )}

      {showModal2 && (
        <>
          <div className="modal-backdrop" onClick={() => setShowModal2(false)} />
          <div className="modal-content">
            <h2>Detalhes do Orçamento</h2>
            <input type="text" placeholder="Selecionar Opção " value={newResource.nome_recurso} onChange={(e) => setNewResource({ ...newResource, nome_recurso: e.target.value })}/>
            <button onClick={() => setShowModal2(false)}>Fechar</button>
          </div>
        </>
      )}

      <Tabela
        colunas={colunas}
        dados={orcamentos}
        aoClicarAcao={handleConsultarClick}
        tipoAcao="link"
        mensagemVazio="Sem orçamentos disponíveis"
      />
    </div>
  );
};

export default ConsultarVotacao;
