import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/ListaReservas.css";
import Navbar2 from "../components/Navbar2.js";

const MeusPedidosReserva = () => {
  const [disabledButtons, setDisabledButtons] = useState(new Set());
  const [comoSolicitante, setComoSolicitante] = useState([]); // data[1]
  const [comoDono, setComoDono] = useState([]);               // data[0]
  const [showModal, setShowModal] = useState(false);
  const [newResource, setNewResource] = useState({
      justification: '', 
  });
 const [selectedReservaID, setSelectedReservaID] = useState(null);


  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/reserva/lista', {
          method: 'GET',
          credentials: 'include' 
        });
        const data = await res.json();
        console.log(data);
        setComoDono(data[0]);         // Dono → Segunda tabela
        setComoSolicitante(data[1]);  // Solicitante → Primeira tabela
      } catch (error) {
        console.error('Erro ao buscar pedidos de reserva:', error);
      }
    };

    fetchReservations();
  }, []);


  const handleUpdate = async (id, field, value, origem) => {
    const fieldMap = {
      recursoEntregue: 'RecursoEntregueSolicitante',
      caucaoEntregue: 'ConfirmarCaucaoSolicitante',
      recursoEntregue2: 'RecursoEntregueDono',
      caucaoEntregue2: 'ConfirmarCaucaoDono',
      bomEstado: 'bomEstado'
    };
    const fieldName = fieldMap[field];
  
    // Mostrar confirmação se for uma ação irreversível
    if (['recursoEntregue', 'caucaoEntregue', 'recursoEntregue2', 'caucaoEntregue2'].includes(field)) {
      const confirmar = window.confirm("Esta operação é irreversível. Tens a certeza que queres continuar?");
      if (!confirmar) return;
    }
  
    let apiEndpoint = '';
  
    switch (field) {
      case 'recursoEntregue':
        apiEndpoint = `http://localhost:8000/api/reserva/confirma/rececao/recurso?reserva_id=${id}`;
        break;
      case 'caucaoEntregue':
        apiEndpoint = `http://localhost:8000/api/reserva/confirma/entrega/caucao?reserva_id=${id}`;
        break;
      case 'recursoEntregue2':
        apiEndpoint = `http://localhost:8000/api/reserva/confirma/entrega/recurso?reserva_id=${id}`;
        break;
      case 'caucaoEntregue2':
        apiEndpoint = `http://localhost:8000/api/reserva/confirma/rececao/caucao?reserva_id=${id}`;
        break;
      case 'bomEstado':
        apiEndpoint = `http://localhost:8000/api/reserva/confirma/bomestado?reserva_id=${id}`;
        break;
      default:
        console.error('Campo desconhecido:', field);
        return;
    }
  
    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reserva_id: id, value }),
      });
  
      const result = await response.json();
      console.log('API response:', result);
  
      if (response.ok) {
        const updateState = (prev) =>
          prev.map((reservation) =>
            reservation.ReservaID === id
              ? { ...reservation, [fieldName]: value }
              : reservation
          );
  
        if (origem === 'solicitante') {
          setComoSolicitante(updateState);
        } else if (origem === 'dono') {
          setComoDono(updateState);
        }
  
        // Adiciona o botão desativado
        setDisabledButtons(prev => new Set(prev).add(`${field}-${id}`));
      } else {
        console.error('Erro na resposta da API:', result);
      }
    } catch (error) {
      console.error('Erro ao atualizar pedido de reserva:', error);
    }
  };
  
      
   
const handleJustification = (id) => {
   const justification = newResource.justification;

   if (justification.trim() === '') {
    toast.error('A justificação não pode estar vazia.');
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
   .then(data => {
   console.log('Justificação enviada:', data);
   toast.success('Justificação enviada com sucesso!');
   setShowModal(false);
   setNewResource({ justification: '' }); // limpar campo
   })
   .catch(error => {
   console.error('Erro ao enviar justificação:', error);
   toast.error('Erro ao enviar justificação.');
   });
 
   };
   
   
  const filteredComoDono = (comoDono || []).filter(reservation => 
   !reservation.DevolucaoCaucao === true && !reservation.EstadoRecurso === true && reservation.JustificacaoEstadoProduto === null
  );

  const filteredComoSolicitante = (comoSolicitante || []).filter(reservation =>
    !reservation.DevolucaoCaucao === true && !reservation.EstadoRecurso === true && reservation.JustificacaoEstadoProduto === null
  );
  

  return (
    <div className="page-content">
      <Navbar2 />
    <div className="home-container">
      <div className='fundoListaReserva'>
        <p className='tituloReserva'>Os Meus Pedidos de Reserva de Recursos</p>
        {Array.isArray(filteredComoSolicitante) && filteredComoSolicitante.length > 0 ? (
        <table>
        <thead>
          <tr>
            <th>N° da Reserva</th>
            <th>Dono do recurso</th>
            <th>Data Início</th>
            <th>Data Fim</th>
            <th>Recurso</th>
            <th>Recurso Recebido</th>
            <th>Caução Entregue</th>
          </tr>
        </thead>
        <tbody>
          {comoSolicitante.map((reservation) => (
            <tr key={reservation.ReservaID}>
              <td>{reservation.ReservaID}</td>
              <td>{reservation.Dono}</td>
              <td>{reservation.DataInicio}</td>
              <td>{reservation.DataFim}</td>
              <td>{reservation.NomeRecurso}</td>
              <td>
              <button className='btnConfirmacoes' onClick={() => handleUpdate(reservation.ReservaID, 'recursoEntregue', !reservation.RecursoEntregueSolicitante, 'solicitante')}
                disabled={disabledButtons.has(`recursoEntregue-${reservation.ReservaID}`)}
                >
                {reservation.RecursoEntregueSolicitante ? 'Sim' : 'Não'}
              </button>
              </td>
              <td>
              <button
                className='btnConfirmacoes'
                onClick={() => handleUpdate(reservation.ReservaID, 'caucaoEntregue', !reservation.ConfirmarCaucaoSolicitante, 'solicitante')}
                disabled={disabledButtons.has(`caucaoEntregue-${reservation.ReservaID}`)}
                >
                {reservation.ConfirmarCaucaoSolicitante ? 'Sim' : 'Não'}
              </button>
              </td>
            </tr>
          ) ) }
        </tbody>
      </table>
) : (
   <p>Nenhum pedido de reserva encontrado.</p>
 )}

      </div>

      <div className='fundoListaReserva'>
        <p className='tituloReserva'>Reservas</p>

        {Array.isArray(filteredComoDono) && filteredComoDono.length > 0 ? (
        <table>
        <thead>
          <tr>
            <th>N° da Reserva</th>
            <th>Solicitante</th>
            <th>Data Início</th>
            <th>Data Fim</th>
            <th>Recurso</th>
            <th>Recurso Entregue</th>
            <th>Caucao Recebida</th>
            <th>Confirmar Estado Recurso</th>
          </tr>
        </thead>
        <tbody>
          {comoDono.map((reservation) => (
            <tr key={reservation.ReservaID}>
              <td>{reservation.ReservaID}</td>
              <td>{reservation.Solicitante}</td>
              <td>{reservation.DataInicio}</td>
              <td>{reservation.DataFim}</td>
              <td>{reservation.NomeRecurso}</td>
              <td>
              <button
              className='btnConfirmacoes'
              onClick={() => handleUpdate(reservation.ReservaID, 'recursoEntregue2', !reservation.RecursoEntregueDono, 'dono')}
              disabled={disabledButtons.has(`recursoEntregue2-${reservation.ReservaID}`)}
              >
              {reservation.RecursoEntregueDono ? 'Sim' : 'Não'}
              </button>
              </td>
              <td>
              <button
              className='btnConfirmacoes'
              onClick={() => handleUpdate(reservation.ReservaID, 'caucaoEntregue2', !reservation.ConfirmarCaucaoDono, 'dono')}
              disabled={disabledButtons.has(`caucaoEntregue2-${reservation.ReservaID}`)}
              >
              {reservation.ConfirmarCaucaoDono ? 'Sim' : 'Não'}
              </button>
              </td>
              <td>
                 <button className='btnSimReserva' onClick={() => handleUpdate(reservation.ReservaID, 'bomEstado', true, 'dono')}>Sim</button>

                  <button className='btnNaoReserva' onClick={() => {setSelectedReservaID(reservation.ReservaID); setShowModal(true);}}>Não</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
) : (
 <p>Nenhuma reserva encontrada.</p>
 )}

      </div>

         
      {showModal && (

      <>
        <div className="modal-backdrop" onClick={() => setShowModal(false)} />
          <div className="modal-content">
            <h2>Enviar Justificação</h2>
            <textarea placeholder="Descrição" value={newResource.justification} onChange={(e) => setNewResource({ ...newResource, justification: e.target.value })}/>
            <div>
              <button onClick={() => handleJustification(selectedReservaID)}>Enviar</button>
              <button onClick={() => setShowModal(false)}>Cancelar</button>
            </div>
          </div>
      </>
      )}


    </div>
    <ToastContainer />
    </div>

    
  );
};

export default MeusPedidosReserva;
