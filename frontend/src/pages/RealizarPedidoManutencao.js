import React, { useState, useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.jsx";
import "../styles/RealizarPedidoManutencao.css";
import Select from '../components/Select.jsx';
import Textarea from '../components/Textarea.jsx';
import Button from '../components/Button.jsx';

const RealizarPedidoManutencao = () => {
  const [recurso_comum_id, setRecursoId] = useState('');
  const [desc_manutencao_recurso_comum, setDescricao] = useState('');
  const [recursos, setRecursos] = useState([]);

  useEffect(() => {
    const fetchRecursos = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/recursoscomuns/', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await response.json();
        console.log(data);
        setRecursos(data);
      } catch (error) {
        console.error('Erro ao buscar recursos comuns:', error);
        toast.error('Erro ao buscar recursos comuns.');
      }
    };

    fetchRecursos();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/api/recursoscomuns/pedidosmanutencao/inserir?recurso_comum_id=${recurso_comum_id}&desc_manutencao_recurso_comum=${desc_manutencao_recurso_comum}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // importante se usares cookies httpOnly
        body: JSON.stringify({ recurso_comum_id, desc_manutencao_recurso_comum }),
      });

      const data = await response.json();
      console.log(data);
      console.log(response);

      if (!response.ok) {
        throw new Error(data.detail || 'Erro ao realizar pedido.');
      }

      toast.success('Pedido de manutenção realizado com sucesso!');
      setRecursoId('');
      setDescricao('');
    } catch (error) {
      console.error('Erro ao realizar pedido de manutenção:', error);
      toast.error(error.message || 'Erro inesperado.');
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <br></br>
      <br></br>
      <ToastContainer />
      <div className="home-container">
        <div className='fundoNovosRecursos'>
          <div className='textoEsquerda'>
            <h1>Realizar Pedido de Manutenção</h1>
            <br></br>
            <form onSubmit={handleSubmit}>
              <div>
                <label>Id:</label><br></br>

                <Select value={recurso_comum_id} onChange={(e) => setRecursoId(e.target.value)} placeholder="Escolha um recurso"
                options={recursos.map(recurso => ({
                  value: recurso.RecComumID,
                  label: recurso.Nome
                }))}
                required variant='geral'/>



                
              </div>

              <div>
                <label>Descrição:</label><br></br>

                <Textarea value={desc_manutencao_recurso_comum} onChange={(e) => setDescricao(e.target.value)} placeholder="Escreve aqui..." rows={6} variant="desc" required/>



              </div>
              <Button className='btnNovoRecurso' type="submit" text={"Realizar pedido"}>Realizar pedido</Button>
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

export default RealizarPedidoManutencao;
