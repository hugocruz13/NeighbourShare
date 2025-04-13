import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import "../styles/RecursosDisponiveis.css";
import Navbar2 from "../components/Navbar2.js";

const RecursosDisponiveis = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/recursos/disponiveis', {
          method: 'GET',
          credentials: 'include' 
        });
        const data = await res.json();
        console.log(data)
        setProducts(data);
      } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className='home-container'>
      <Navbar2 />

      <div className='fundoRecursos'>
      <p className='p-Recursos'>Recursos Disponíveis ({products.length})</p>
      <div className="grid-recursos">
        {products.map((product) => (
          <div key={product.RecursoID}>
            <Link to={`/pedidosReserva/${product.RecursoID}`}>
              <img src={product.Image} alt={product.name} style={{ width: '100%' }} />
            </Link>
            <h2>{product.Nome}</h2>
            <h2>{product.DescRecurso}</h2>
          </div>
        ))}
      </div>
      </div>
    </div>
  );
};

export default RecursosDisponiveis;