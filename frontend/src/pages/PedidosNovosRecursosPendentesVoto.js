import React, { useEffect, useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/MeusRecursos.css";
import Navbar2 from "../components/Navbar2.js";

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
        console.log(data);
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
        <div className='fundoMeusRecursos'>
          <p className='p-meusRecursos'>Detalhes Pedido</p>
          <table >
            <thead>
              <tr>
                <th>Nº Pedido</th>
                <th>Descrição</th>
                <th>Concorda com a Aquisição?</th>
              </tr>
            </thead>
            <tbody>
              {recurso.map((recurso) => (
              <tr key={recurso.RecursoID}>
                <td>{recurso.RecursoID}</td>
                <td>{recurso.Desc}</td>
                <td>
                  <button className='btnSimReserva' >Sim</button>
                  <button className='btnNaoReserva' >Não</button>
                </td>
              </tr>
              ))}
            </tbody>
          </table>

      </div>
    </div>
    <ToastContainer />
</div>
  );
};

export default PedidosNovosRecursosPendentesVoto;
