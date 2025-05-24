import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import Select from '../components/Select.jsx';

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
      console.log("Dados recebidos:", data);

      if (Array.isArray(data)) {
        setPedidos(data);
        setMensagemErro(null);
      } else if (data && data.detail) {
        setMensagemErro(data.detail);
        setPedidos([]);
      } else {
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
            titulo={"Manutenções"}
            colunas = {[
              { accessorKey: 'ManutencaoID', header: 'Nº Manutenção' },
              { accessorKey: 'DescManutencao', header: 'Descrição' },
              { accessorKey: 'DataManutencao', header: 'Data Manutenção'},
              { accessorKey: 'EstadoManuID', 
                header: 'Estado',
                cell: ({ row }) => {
                  const pedido = row.original
                  return (
                    <Select
                      value={
                        statusOptions.find(opt =>opt.EstadoManuID === pedido.EstadoManuID) && {
                          value: pedido.EstadoManuID,
                          label: statusOptions.find(opt => opt.EstadoManuID === pedido.EstadoManuID)?.DescEstadoManutencao
                        }
                      }
                      onChange={(selectedOption) =>
                        handleStatusChange(pedido.ManutencaoID, selectedOption.target.value)
                      }
                      options={statusOptions.map(opt => ({
                        value: opt.EstadoManuID,
                        label: opt.DescEstadoManutencao
                      }))}
                      isDisabled={pedido.EstadoManuID === 2}
                      menuPortalTarget={document.body}
                      styles={{
                        menuPortal: base => ({ ...base, zIndex: 9999}),
                        menu: base => ({ ...base, zIndex: 9999}),
                      }}
                    />
                  );
                } }
            ]}
            dados={pedidos}
            
          />




        </div>
        <Toaster />
      </div>
  );
};

export default Manutencao;
