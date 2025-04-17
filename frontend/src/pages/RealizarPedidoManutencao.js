import React, { useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar2 from "../components/Navbar2.js";
const RealizarPedidoManutencao = () => {
  const [recurso_comum_id, setRecursoId] = useState('');
  const [desc_manutencao_recurso_comum, setDescricao] = useState('');

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
      <ToastContainer />
      <h1>Realizar Pedido de Manutenção</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Id:
            <input
              value={recurso_comum_id}
              onChange={(e) => setRecursoId(e.target.value)}
              required
            />
          </label>
        </div>

        <div>
          <label>
            Descrição:
            <textarea
              value={desc_manutencao_recurso_comum}
              onChange={(e) => setDescricao(e.target.value)}
              required
            />
          </label>
        </div>

        <button type="submit">Realizar pedido</button>
      </form>
      <p>
        Se achas que existe algum recurso avariado, como um elevador, porta ou entre outros,
        realiza aqui o teu pedido de manutenção.
      </p>
    </div>
  );
};

export default RealizarPedidoManutencao;
