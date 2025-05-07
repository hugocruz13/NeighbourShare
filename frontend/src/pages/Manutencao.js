import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosManutencao.css";
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

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
          <Tabela
            colunas={['Nº Manutenção', 'Descrição', 'Data Manutenção', 'Estado']}
            dados={pedidos}
            aoClicarAcao={(pedido) => handleDateUpdate(pedido)}
            tipoAcao="link"
            mensagemVazio="Nenhum pedido de manutenção encontrado."
          />
        </div>
  
        <ToastContainer />
      </div>
    </div>
  );
};

export default Manutencao;
