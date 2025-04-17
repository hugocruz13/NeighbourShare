import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Certifique-se de que o Link está importado
import { useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/PedidosManutencao.css";
import Navbar2 from "../components/Navbar2.js";

const Manutencao = () => {
  const [pedidos, setPedidos] = useState([]);
  const [selectedPedido, setSelectedPedido] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showJustificationModal, setShowJustificationModal] = useState(false);
  const [pedidoAtual, setPedidoAtual] = useState(null);

  useEffect(() => {
    const fetchPedidos = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursoscomuns/manutencao', {
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


  return (
    <div className="page-content">
<Navbar2 />

    <div className="home-container">
      <div className='fundoMeusRecursos'>

      <p className='p-meusRecursos'>Pedidos de Manutenção</p>
      <table>
        <thead>
          <tr>
            <th>Nº Manutenção</th>
            <th>Entidade</th>
            <th>Data Manutenção</th>
            <th>Descrição</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {pedidos.map((manutencao) => (
            <tr key={manutencao.ManutencaoID}>
              <td>{manutencao.ManutencaoID}</td>
              <td>{manutencao.EntidadeNome}</td>
              <td>{manutencao.DataManutencao}</td>
              <td>{manutencao.DescManutencao}</td>
              <td>{manutencao.Estado}</td>
            </tr>
          ))}
        </tbody>
      </table>


      </div>
      
    </div>
</div>
  );
};

export default Manutencao;
