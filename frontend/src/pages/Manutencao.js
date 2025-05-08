import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosManutencao.css";
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

const Manutencao = () => {
  const [manutencoes, setManutencoes] = useState([]);
  const [statusOptions, setStatusOptions] = useState([]);
  const [editDateId, setEditDateId] = useState(null);
  const [newDate, setNewDate] = useState('');

  useEffect(() => {
    const fetchManutencoes = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/manutencao/', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        if (Array.isArray(data)) {
          setManutencoes(data);
        } else if (data.detail === 'Nenhuma manutenção encontrada') {
          setManutencoes([]);
        } else {
          throw new Error("Resposta inesperada da API");
        }
      } catch (error) {
        console.error('Erro ao buscar manutenções:', error);
        toast.error('Erro ao buscar manutenções.');
      }
    };
    fetchManutencoes();
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

      toast.success('Estado da manutenção atualizado com sucesso!');
      setManutencoes((prev) =>
        prev.map((p) =>
          p.ManutencaoID === manutencao_id
            ? { ...p, EstadoManuID: parseInt(novo_estado_id) }
            : p
        )
      );
    } catch (error) {
      toast.error('Erro ao atualizar estado da manutenção.');
    }
  };

  const handleDateUpdate = async (manutencao) => {
    try {
      const res = await fetch('http://localhost:8000/api/recursoscomuns/manutencao/update/', {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ManutencaoID: manutencao.ManutencaoID,
          PMID: manutencao.PMID,
          DataManutencao: newDate,
          DescManutencao: manutencao.DescManutencao
        })
      });

      if (!res.ok) throw new Error();

      toast.success('Data de manutenção atualizada com sucesso!');
      setManutencoes((prev) =>
        prev.map((p) =>
          p.ManutencaoID === manutencao.ManutencaoID
            ? { ...p, DataManutencao: newDate }
            : p
        )
      );
      setEditDateId(null);
      setNewDate('');
    } catch (error) {
      toast.error('Erro ao atualizar a data.');
    }
  };

  // Helper para mostrar o nome do estado
  const getEstadoNome = (estadoId) => {
    const estado = statusOptions.find(opt => opt.EstadoManuID === estadoId);
    return estado ? estado.DescEstadoManutencao : estadoId;
  };

  return (
    <div className="page-content">
      <Navbar2 />

      <div className="home-container">
        <div className='fundoMeusRecursos'>
          <p className='p-meusRecursos'>Manutenções Registadas</p>
          <Tabela
            colunas={['Nº Manutenção', 'Descrição', 'Data Manutenção', 'Estado', 'Alterar Estado']}
            dados={manutencoes.map((manutencao) => ({
              'Nº Manutenção': manutencao.ManutencaoID,
              'Descrição': manutencao.DescManutencao,
              'Data Manutenção': manutencao.DataManutencao,
              'Estado': getEstadoNome(manutencao.EstadoManuID),
              'Alterar Estado': (
                <select
                  value={manutencao.EstadoManuID}
                  onChange={e => handleStatusChange(manutencao.ManutencaoID, e.target.value)}
                >
                  {statusOptions.map(option => (
                    <option key={option.EstadoManuID} value={option.EstadoManuID}>
                      {option.DescEstadoManutencao}
                    </option>
                  ))}
                </select>
              )
            }))}
            mensagemVazio="Nenhuma manutenção registada encontrada."
          />
        </div>

        <ToastContainer />
      </div>
    </div>
  );
};

export default Manutencao;
