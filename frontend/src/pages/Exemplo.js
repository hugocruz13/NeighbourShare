import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import "../styles/RecursosDisponiveis.css";
import Navbar2 from "../components/Navbar2.js";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Exemplo = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    

    const fetchProducts = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await res.json();
        console.log(data);
        setProducts(data);
        setLoading(false);
      } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);


  return (
    <div className="page-content">
      <Navbar2 />
      <div className='home-container'>
        <div className='fundoRecursos'>
          <p className='p-Recursos'>Recursos Disponíveis</p>
          <div className="grid-recursos">
            {products.map((product) => (
              <div key={product.RecursoID}>
                <Link to={`/pedidosReserva/${product.RecursoID}`}>
                  <img src="http://127.0.0.1:8000/api/imagens/recursos/1/Circulo_amarelo.png" alt={product.Nome} style={{ width: '100%' }} />
                </Link>
                <h2>{product.Nome}</h2>
                <h2>{product.DescRecurso}</h2>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Exemplo;
