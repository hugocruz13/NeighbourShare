import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Votacoes = () => {
  const [votacoes, setVotacoes] = useState([]);

  useEffect(() => {
    const fetchVotacoes = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/votacoes');
        const data = await res.json();
        setVotacoes(data);
      } catch (error) {
        console.error('Erro ao buscar votações:', error);
      }
    };

    fetchVotacoes();
  }, []);

  return (
    <div> 
      <h1>Votações</h1>
      <table>
        <thead>
          <tr>
            <th>Nº Votação</th>
            <th>Recurso</th>
            <th>Fim da votação</th>
            <th>Descrição</th>
            <th>Aceite</th>
            <th>Ação</th>
          </tr>
        </thead>
        <tbody>
          {votacoes.map((votacao) => (
            <tr key={votacao.id}>
              <td>{votacao.id}</td>
              <td>{votacao.recurso}</td>
              <td>{votacao.fimVotacao}</td>
              <td>{votacao.descricao}</td>
              <td>{votacao.aceite}</td>
              <td>
                <Link to={`/consultarVotacao/${votacao.id}`}>Consultar</Link>
              </td> 
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Votacoes;
 