import React, { useState } from 'react';
import "../styles/RealizarPedidoNovoRecurso.css";
import Navbar2 from "../components/Navbar2.js";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Textarea from '../components/Textarea.jsx';
import Button from '../components/Button.jsx';

const RealizarPedidoNovoRecurso = () => {
  const [desc_pedido_novo_recurso, setDescricao] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch(`http://localhost:8000/api/recursoscomuns/pedidosnovos/inserir?desc_pedido_novo_recurso=${desc_pedido_novo_recurso}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // importante se usares cookies httpOnly
        body: JSON.stringify({ desc_pedido_novo_recurso }),
      });
      toast.success('Pedido de novo recurso realizado com sucesso!');
      setDescricao('');
    } catch (error) {
      console.error('Erro ao realizar pedido de novo recurso:', error);
      toast.error('Erro ao realizar pedido de novo recurso.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <br></br>
      <br></br>
      <div className="home-container">
        <div className='fundoNovosRecursos'>
          <div className='textoEsquerda'>
            <p className='p-NovosRecursos'>Realizar Pedido de Novo Recurso</p>
            <form onSubmit={handleSubmit}>
              <div>
                <label>Descrição:</label><br></br>
                <Textarea value={desc_pedido_novo_recurso} onChange={(e) => setDescricao(e.target.value)} placeholder="Escreve aqui..." rows={6} variant="desc" required/>
              </div>
              <Button className='btnNovoRecurso' type="submit" text={"Realizar Pedido"}>Realizar Pedido</Button>
            </form>
          </div>

          <div className='imagemDireitaManu'>
            <img className='imgNovosRecursosManu' src="./img/fundo2.png" alt="Imagem"/>
          </div>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default RealizarPedidoNovoRecurso;
