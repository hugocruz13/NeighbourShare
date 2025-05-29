import { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import Navbar2 from "../components/Navbar2.jsx";
import Tabela from "../components/Tabela.jsx";
import ModalForm from '../components/ModalForm.jsx';
import Button from '../components/Button.jsx';
import 'react-toastify/dist/ReactToastify.css';

const PedidosAquisicao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [showModal, setShowModal] = useState(false);
    const [votacao, setVotacao] = useState({
      titulo: '',
      descricao: '',
      id_processo: 0,
      data_fim: '',
      tipo_votacao: 'Aquisição',
    });

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/pedidosnovos', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        if (data && Array.isArray(data)) {
          // Se for um array, atualiza os pedidos
          setPedidos(data);
        } else if (data && data.detail) {
          // Se a resposta contiver a chave 'detail', trata como erro
          setPedidos([]);  // Limpa os pedidos
        } else {
          // Caso não seja nem um array nem um erro, define um erro genérico
          setPedidos([]);
        }
      } catch (error) {
        console.error('Erro ao buscar pedidos de aquisição:', error);
        setPedidos([]);
      }
    };

    fetchPedidos();
  }, []);

  const handleCreateVotacao = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/criarvotacao', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(votacao),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Erro ao criar votação');
      }

      ToastManager.success('Votação criada com sucesso!');
      setShowModal(false);
      setVotacao({
        titulo: '',
        descricao: '',
        id_processo: 0,
        data_fim: '',
        tipo_votacao: '',
      });
    } catch (error) {
      ToastManager.error('Erro ao criar votação: ' + error.message);
    }
  };

  const handleChange = (e, actionMeta) => {
    if (e && e.target) {
      const { name, value } = e.target;
      setVotacao(prev => ({ ...prev, [name]: value }));
    } else if (e && actionMeta && actionMeta.action === 'select-option') {
      setVotacao(prev => ({ ...prev, [actionMeta.name]: e.value }));
    } else if (e && e.name && e.value) {
      setVotacao(prev => ({ ...prev, [e.name]: e.value }));
    }
  };


  return (
    <>
      <Navbar2 />
      <div className="home-container">
          <Tabela
            titulo="Pedidos de Aquisição"
            colunas = {[
              { accessorKey: 'NumPedido', header: 'Nº do Pedido' },
              { accessorKey: 'Solicitante', header: 'Solicitante' },
              { accessorKey: 'DataPedido', header: 'Data Do Pedido' },
              { accessorKey: 'Descricao', header: 'Descrição' },
            ]}

            dados={pedidos.map((pedido) => ({
              'NumPedido': pedido.PedidoNovoRecID,
              'Solicitante': pedido.Utilizador_.NomeUtilizador,
              'DataPedido': pedido.DataPedido,
              'Descricao': pedido.DescPedidoNovoRecurso,
            }))}
            botoesOpcoes={[<Button onClick={() => {setShowModal(true)}} text={"Criar Votação"}>Criar Votação</Button>]}
          />
      </div>
      <ModalForm
            show={showModal}
            onclose={() => setShowModal(false)}
            title={'Criar Votação'}
            fields={[
              { name: 'titulo', label: 'Título', type: 'text' },
              { name: 'descricao', label: 'Descrição', type: 'text' },
              { name: 'id_processo', label: 'Processo', type: 'select',
                options: pedidos.map(p => ({ value: p.PedidoNovoRecID, label: p.PedidoNovoRecID + ' - ' + p.DescPedidoNovoRecurso }))},
              { name: 'data_inicio', label: 'Data de Início', type: 'date' },
              { name: 'data_fim', label: 'Data de Fim', type: 'date' }
            ]}
              
            formData={votacao}
            onChange={handleChange}
            onSubmit={(e) => {
              e.preventDefault();
              handleCreateVotacao();
            }}
            textBotao={'Criar Votação'}
          />
      <Toaster />
    </>
  );
};

export default PedidosAquisicao;
