import React, { useEffect, useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/LayoutPaginasTabelas.module.css';
import Navbar2 from "../components/Navbar2.js";
import Tabela from "../components/Tabela.jsx";

const PedidosNovosRecursosPendentesVoto = () => {
  const [recurso, setUsers] = useState([]);
  const [erro, setErro] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/pessoais', {
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Erro ao buscar dados');
        const data = await res.json();
        setUsers(data);
      } catch (error) {
        setErro(error.message);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        <div className={styles.fundo}>
          <p className={styles.pmeusRecursos}>Detalhes Pedido</p>

          <Tabela
            colunas={['Nº Pedido', 'Descrição', 'Concorda com a Aquisição?']}
            dados={recurso.map((recurso) => ({
              'Nº Pedido': recurso.RecursoID,
              'Descrição': recurso.Desc,
              'Concorda com a Aquisição?': (
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button className={styles.btnSimPedidoReserva}>Sim</button>
                  <button className={styles.btnNaoPedidoReserva}>Não</button>
                </div>
              )
            }))}
            mensagemVazio="Nenhum recurso encontrado."
          />
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default PedidosNovosRecursosPendentesVoto;
