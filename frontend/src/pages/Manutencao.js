import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosManutencao.css";
import Navbar2 from "../components/Navbar2.js";

const Manutencao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [statusOptions, setStatusOptions] = useState([]);
  const [editDateId, setEditDateId] = useState(null);
  const [newDate, setNewDate] = useState('');

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/manutencao/', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
        setPedidos(data);
      } catch (error) {
        console.error('Erro ao buscar pedidos de manutenção:', error);
      }
    };

    fetchPedidos();
  }, []);

  useEffect(() => {
    const fetchStatusOptions = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/manutencao/estados', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        setStatusOptions(data);
      } catch (error) {
        console.error('Erro ao buscar opções de estado:', error);
      }
    };

    fetchStatusOptions();
  }, []);

  const handleStatusChange = async (manutencao_id, novo_estado_id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/recursoscomuns/manutencao/update/${manutencao_id}/estado`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ novo_estado_id })
      });

      if (!res.ok) throw new Error();

      toast.success('Estado do pedido atualizado com sucesso!');
      setPedidos((prev) =>
        prev.map((p) => p.ManutencaoID === manutencao_id ? { ...p, estado: novo_estado_id } : p)
      );
    } catch (error) {
      toast.error('Erro ao atualizar estado do pedido.');
    }
  };

  const handleDateUpdate = async (pedido) => {
    try {
      const res = await fetch('http://localhost:8000/api/recursoscomuns/manutencao/update/', {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ManutencaoID: pedido.ManutencaoID,
          PMID: pedido.PMID,
          DataManutencao: newDate,
          DescManutencao: pedido.DescManutencao
        })
      });

      if (!res.ok) throw new Error();

      toast.success('Data de manutenção atualizada com sucesso!');
      setPedidos((prev) =>
        prev.map((p) =>
          p.ManutencaoID === pedido.ManutencaoID ? { ...p, DataManutencao: newDate } : p
        )
      );
      setEditDateId(null);
    } catch (error) {
      toast.error('Erro ao atualizar a data.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />

      <div className="home-container">
        <div className='fundoMeusRecursos'>
          <p className='p-meusRecursos'>Pedidos de Manutenção</p>
          {pedidos.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Nº Manutenção</th>
                  <th>Descrição</th>
                  <th>Data Manutenção</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {pedidos.filter(manutencao => manutencao.EstadoManuID !== 2).map((manutencao) => (
                  <tr key={manutencao.ManutencaoID}>
                    <td>{manutencao.ManutencaoID}</td>
                    <td>{manutencao.DescManutencao}</td>
                    <td>
                      {editDateId === manutencao.ManutencaoID ? (
                        <>
                          <input
                            type="date"
                            value={newDate}
                            onChange={(e) => setNewDate(e.target.value)}
                          />
                          <button onClick={() => handleDateUpdate(manutencao)}>💾</button>
                          <button onClick={() => setEditDateId(null)}>❌</button>
                        </>
                      ) : (
                        <>
                          {manutencao.DataManutencao}
                          <button onClick={() => {
                            setEditDateId(manutencao.ManutencaoID);
                            setNewDate(manutencao.DataManutencao);
                          }}>✏️</button>
                        </>
                      )}
                    </td>
                    <td>
                      <select
                        value={manutencao.estado}
                        onChange={(e) => handleStatusChange(manutencao.ManutencaoID, e.target.value)}
                      >
                        {statusOptions.map((option) => (
                          <option key={option.EstadoManuID} value={option.EstadoManuID}>
                            {option.DescEstadoManutencao}
                          </option>
                        ))}
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum pedido de manutenção encontrado.</p>
          )}
        </div>
        <ToastContainer />
      </div>
    </div>
  );
};

export default Manutencao;
