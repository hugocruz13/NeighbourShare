import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

const Manutencao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [mensagemErro, setMensagemErro] = useState(null);
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
        if (data && Array.isArray(data.pedidos)) {
          // Se 'pedidos' for um array, atualize o estado
          setPedidos(data.pedidos);
          setMensagemErro(null);  // Limpar qualquer mensagem de erro anterior
        } else if (data && data.detail) {
          // Caso a resposta seja um objeto com a chave 'detail', trate como erro
          setMensagemErro(data.detail);
          setPedidos([]);  // Não há pedidos, então esvazia o array
        } else {
          // Caso não se encaixe em nenhum dos cenários, definir como erro genérico
          setMensagemErro('Erro inesperado ao carregar os dados');
          setPedidos([]);
        }
      } catch (error) {
        console.error('Erro ao carregar os dados:', error);
        setMensagemErro('Falha ao carregar os dados');
        setPedidos([]);
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

  const handleStartEdit = (pedido) => {
    setEditDateId(pedido.ManutencaoID);
    setNewDate(pedido.DataManutencao || '');
  };

  const handleCancelEdit = () => {
    setEditDateId(null);
    setNewDate('');
  };

  const handleStatusChange = async (manutencao_id, novo_estado_id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/recursoscomuns/manutencao/update/${manutencao_id}/estado`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ novo_estado_id })
      });

      if (!res.ok) throw new Error();

      ToastManager.success('Estado do pedido atualizado com sucesso!');
      setPedidos((prev) =>
        prev.map((p) => p.ManutencaoID === manutencao_id ? { ...p, estado: novo_estado_id } : p)
      );
    } catch (error) {
      ToastManager.error('Erro ao atualizar estado do pedido.');
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

      ToastManager.success('Data de manutenção atualizada com sucesso!');
      setPedidos((prev) =>
        prev.map((p) =>
          p.ManutencaoID === pedido.ManutencaoID ? { ...p, DataManutencao: newDate } : p
        )
      );
      setEditDateId(null);
    } catch (error) {
      ToastManager.error('Erro ao atualizar a data.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
    
      <div className="home-container">
          <Tabela
            titulo="Manutenções"
            colunas = {[
              { accessorKey: 'NumManutencao', header: 'Nº Manutenção' },
              { accessorKey: 'Descricao', header: 'Descrição' },
              { 
                accessorKey: 'DataManutencao', 
                header: 'Data Manutenção',
        },
              { accessorKey: 'Estado', header: 'Estado' }
            ]}
            dados={pedidos}
          />
        </div>
        <Toaster />
      </div>
  );
};

export default Manutencao;
