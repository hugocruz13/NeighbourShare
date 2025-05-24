import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import "../styles/RecursosDisponiveis.css";
import Navbar2 from "../components/Navbar2.jsx";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const RecursosDisponiveis = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const fetchUserId = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/me', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await res.json();

        setUserId(data.id); // Supondo que o ID do utilizador está na propriedade 'id'
      } catch (error) {
        console.error('Erro ao buscar ID do utilizador:', error);
      }
    };

    const fetchProducts = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await res.json();
        console.log(data);
        if (Array.isArray(data)) {
          setProducts(data);
        } else if (data.detail === 'Nenhum recurso encontrado') {
          setProducts([]);
        } else {
          throw new Error("Resposta inesperada da API");
        }

        setLoading(false);
      } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        setLoading(false);
      }
    };

    fetchUserId();
    fetchProducts();
  }, []);

  const filteredProducts = products.filter(product => product.Utilizador_.UtilizadorID !== userId && product.Disponibilidade_.DispID === 1);

  return (
    <div className="page-content">
      <Navbar2 />
      <div className='home-container'>
        <div className='fundoRecursos'>
          <p className='p-Recursos'>Recursos Disponíveis ({filteredProducts.length})</p>
          <div className="grid-recursos">
            {filteredProducts.map((product) => (
              <div key={product.RecursoID}>
                <Link to={`/pedidosReserva/${product.RecursoID}`}>
                  <img src={product.Image} alt={product.name} style={{ width: '100%' }} />
                </Link>
                <h2>Nome: {product.Nome}</h2>
                <h2>Desc: {product.DescRecurso}</h2>
                <h2>Dono: {product.Utilizador_.NomeUtilizador}</h2>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecursosDisponiveis;
