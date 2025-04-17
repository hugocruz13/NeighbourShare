import React, { useState } from 'react';
import "../styles/RealizarPedidoNovoRecurso.css";
import Navbar2 from "../components/Navbar2.js";
const RealizarPedidoNovoRecurso = () => {
  const [descricao, setDescricao] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch(`http://localhost:8000/api/recursoscomuns/pedidosnovos/inserir?desc_pedido_novo_recurso=${descricao}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: "include",
        body: JSON.stringify({ descricao }),
      });
      alert('Pedido de novo recurso realizado com sucesso!');
      setDescricao('');
    } catch (error) {
      console.error('Erro ao realizar pedido de novo recurso:', error);
      alert('Erro ao realizar pedido de novo recurso.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="home-container">
        <div className='fundoNovosRecursos'>
        <div className='textoEsquerda'>
        <p className='p-NovosRecursos'>Realizar Pedido de Novo Recurso</p>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Descrição:</label><br></br>
            <textarea className='inputNovoRecurso' value={descricao} onChange={(e) => setDescricao(e.target.value)} required/>

          </div>
          <button className='btnNovoRecurso' type="submit">Realizar Pedido</button>
        </form>
      </div>

      <div className='imagemDireita'>
        <img className='imgNovosRecursos' src="./img/fundo2.png" alt="Imagem"/>
        <p>Se achas que é necessário novos recursos realiza o pedido aqui.</p>
      </div>
        </div>
      </div>

    </div>
  );
};

export default RealizarPedidoNovoRecurso;
