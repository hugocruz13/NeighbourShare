import React, { useState, useEffect } from 'react';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from '../components/Tabela.jsx';
import Button from '../components/Button.jsx';
import ModalForm from '../components/ModalForm.jsx';
import ToastManager from '../components/ToastManager';
import { Toaster } from 'react-hot-toast';


const FIELD_MAP = {
  recursoEntregue: 'RecursoEntregueSolicitante',
  caucaoEntregue: 'ConfirmarCaucaoSolicitante',
  recursoEntregue2: 'RecursoEntregueDono',
  caucaoEntregue2: 'ConfirmarCaucaoDono',
  bomEstado: 'bomEstado'
};

const API_ENDPOINTS = {
  recursoEntregue: (id) => `/api/reserva/confirma/rececao/recurso?reserva_id=${id}`,
  caucaoEntregue: (id) => `/api/reserva/confirma/entrega/caucao?reserva_id=${id}`,
  recursoEntregue2: (id) => `/api/reserva/confirma/entrega/recurso?reserva_id=${id}`,
  caucaoEntregue2: (id) => `/api/reserva/confirma/rececao/caucao?reserva_id=${id}`,
  bomEstado: (id) => `/api/reserva/confirma/bomestado?reserva_id=${id}`,
};

const atualizaTabelaReservas = (reservations, id, fieldName, value) =>
  reservations.map((r) =>
    r.ReservaID === id ? { ...r, [fieldName]: value } : r
);
const isReservaPendente = (res) =>
  !res.DevolucaoCaucao && !res.EstadoRecurso && res.JustificacaoEstadoProduto === null;

const SimNaoBotao = ({ id, field, value, origem, handleClick }) => (
  <Button
    variant={value ? "green" : "red"}
    onClick={() => handleClick(id, field, !value, origem)}
    disabled={value}
  >
    {value ? 'Sim' : 'Não'}
  </Button>
);


const MeusPedidosReserva = () => {
  const [disabledButtons, setDisabledButtons] = useState(new Set());
  const [comoSolicitante, setComoSolicitante] = useState([]); // data[1]
  const [comoDono, setComoDono] = useState([]);               // data[0]
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNewResource] = useState({ justification: ''});
  const [selectedReservaID, setSelectedReservaID] = useState(null);

  /*Obtenção dos dados dos pedidos de reserva, quer como dono quer como vizinho*/
  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/reserva/lista', {
          method: 'GET',
          credentials: 'include' 
        });
        const data = await res.json();
        setComoDono(data[0] || []);         // Dono → Segunda tabela
        setComoSolicitante(data[1] || []);  // Solicitante → Primeira tabela
      } catch (error) {
        console.error('Erro ao buscar pedidos de reserva:', error);
      }
    };
    fetchReservations();
  }, []);

 /*Função para atualizar o estado da entrega/receção do recurso/caução*/
  const handleUpdate = async (id, field, value, origem) => {
    const fieldName = FIELD_MAP[field];
    const irreversiveFields = ['recursoEntregue', 'caucaoEntregue', 'recursoEntregue2', 'caucaoEntregue2', 'bomEstado'];
    
    const removeReservaDaTabela = (prev) => prev.filter(res => res.ReservaID !== id);

    const doUpdate = async () => {
      const endpoint = `http://localhost:8000${API_ENDPOINTS[field](id)}`;
      try{
        const response = await fetch(endpoint, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ reserva_id: id }),
        });
        const result = await response.json();
        if (response.ok){
          ToastManager.success('Atualização realizada com sucesso!');
          const updater = origem === 'solicitante' ? setComoSolicitante : setComoDono;

          if (field === 'bomEstado') {
          updater(prev => removeReservaDaTabela(prev));
          } else {
            updater(prev => atualizaTabelaReservas(prev, id, fieldName, value));
          }
          setDisabledButtons(prev => new Set(prev).add(`${field}-${id}`));

        }
        else {
          ToastManager.error('Erro ao atualizar reserva.');
          console.error('Erro ao atualizar reserva:', result);
        }
      }
      catch (error) {
        console.error('Erro ao atualizar reserva:', error);
        ToastManager.error('Erro ao atualizar reserva.');
      }
  };

  if(irreversiveFields.includes(field)) {
    ToastManager.customConfirm(
      "Esta ação é irreversível. Tem a certeza que deseja continuar?",
      doUpdate,
      () => {}
    );
  } else {
    doUpdate();
  };
  };

  const handleJustification = (id) => {
   const justification = newResource.justification.trim();

   if (!justification) {
      ToastManager.error('A justificação não pode estar vazia.');
      return;
    }

   fetch(`http://localhost:8000/api/reserva/submissao/justificacao?reserva_id=${id}&justificacao=${justification}`, {
      method: 'POST',
      credentials: 'include',
      headers: {
      'Content-Type': 'application/json',
      },
      body: JSON.stringify({ reserva_id: id, justification }),
   })
   .then(response => response.json())
   .then(() => {
      ToastManager.success('Justificação enviada com sucesso!');
      setShowModal(false);
      setNewResource({ justification: '' }); // limpar campo
      setComoDono(prev => prev.filter(res => res.ReservaID === id ? false : true));
      })
   .catch(error => {
      console.error('Erro ao enviar justificação:', error);
      ToastManager.error('Erro ao enviar justificação.');
      });
 
   };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
          <Tabela
            titulo="Reservas como Solicitante"
            colunas={[
              { accessorKey: 'Dono', header: 'Dono' },
              { accessorKey: 'DataInicio', header: 'Data Início' },
              { accessorKey: 'DataFim', header: 'Data Fim' },
              { accessorKey: 'NomeRecurso', header: 'Recurso' },
              {
                accessorKey: 'RecursoRecebido',
                header: 'Recurso Recebido ?',
                cell: ({ row }) => {
                  const res = row.original;
                  return (
                  <SimNaoBotao
                    id={res.ReservaID}
                    field="recursoEntregue"
                    value={res.RecursoEntregueSolicitante}
                    origem="solicitante"
                    disabled={disabledButtons.has(`recursoEntregue-${res.ReservaID}`)}
                    handleClick={handleUpdate}
                  />
                );
                }
              },
              {
                accessorKey: 'CaucaoEntregue',
                header: 'Caução Entregue ?',
                cell: ({ row }) => {
                  const res = row.original;
                  return (
                  <SimNaoBotao
                    id={res.ReservaID}
                    field="caucaoEntregue"
                    value={res.ConfirmarCaucaoSolicitante}
                    origem="solicitante"
                    disabled={disabledButtons.has(`caucaoEntregue-${res.ReservaID}`)}
                    handleClick={handleUpdate}
                  />
                  );
                }
              },
            ]}
            dados={comoSolicitante.filter(isReservaPendente)}
          />
          <Tabela
            titulo="Reservas como Dono"
            colunas={[
              { accessorKey: 'Solicitante', header: 'Solicitante' },
              { accessorKey: 'DataInicio', header: 'Data Início' },
              { accessorKey: 'DataFim', header: 'Data Fim' },
              { accessorKey: 'NomeRecurso', header: 'Recurso' },
              {
                accessorKey: 'RecursoEntregue',
                header: 'Recurso Entregue ?',
                cell: ({ row }) => {
                  const res = row.original;
                  return (
                  <SimNaoBotao
                    id={res.ReservaID}
                    field="recursoEntregue2"
                    value={res.RecursoEntregueDono}
                    origem="dono"
                    disabled={disabledButtons.has(`recursoEntregue2-${res.ReservaID}`)}
                    handleClick={handleUpdate}
                  />
                  );
                }
              },
              {
                accessorKey: 'CaucaoRecebida',
                header: 'Caução Recebida ?',
                cell: ({ row }) => {
                  const res = row.original;
                  return (
                  <SimNaoBotao
                    id={res.ReservaID}
                    field="caucaoEntregue2"
                    value={res.ConfirmarCaucaoDono}
                    origem="dono"
                    disabled={disabledButtons.has(`caucaoEntregue2-${res.ReservaID}`)}
                    handleClick={handleUpdate}
                  />
                  );
                }
              },
              {
                accessorKey: 'ConfirmarEstadoRecurso',
                header: 'Confirmar Estado Recurso',
                cell: ({ row }) => {
                  const res = row.original;
                  const podeConfirmarEstado = res.RecursoEntregueDono === true && res.ConfirmarCaucaoDono === true;
                  return (
                    <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                      <Button variant="green" onClick={() => handleUpdate(res.ReservaID, 'bomEstado', true, 'dono')} disabled={!podeConfirmarEstado}>Sim</Button>
                      <Button variant="red" onClick={() => { setSelectedReservaID(res.ReservaID); setShowModal(true)}} disabled={!podeConfirmarEstado}>Não</Button>
                    </div>
                  );
                }
              },
            ]}
            dados={comoDono.filter(isReservaPendente)}
        />
        <ModalForm
          show={showModal}
          onclose={() => setShowModal(false)}
          title="Justificação"
          fields={[
            { label: 'Justificação', name: 'justification', type: 'text', required: true },
          ]}
          formData={newResource}
          onChange={(e) => setNewResource({ ...newResource, [e.target.name]: e.target.value })}
          onSubmit={(e) => {
            e.preventDefault();
            handleJustification(selectedReservaID);
          }}
          textBotao="Enviar Justificação"
        />
      </div>
      <Toaster position="top-center" />
    </div>
  );
};


export default MeusPedidosReserva;
