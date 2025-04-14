import React, { useState } from 'react';

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
      <div>
        <h1>Realizar Pedido de Novo Recurso</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              Descrição:
              <textarea value={descricao} onChange={(e) => setDescricao(e.target.value)} required/>
            </label>
          </div>
          <button type="submit">Realizar Pedido</button>
        </form>
      </div>
      <div>
        <img src="URL_DA_IMAGEM" alt="Imagem de um complexo de apartamentos moderno com piscina" style={{ width: '400px', height: 'auto' }} />
        <p>Se achas que é necessário novos recursos realiza o pedido aqui.</p>
      </div>
    </div>
  );
};

export default RealizarPedidoNovoRecurso;
