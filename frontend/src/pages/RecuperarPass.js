import React, { useState } from "react";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


function RecuperarPass() {
  const [formData, setFormData] = useState({ token: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`http://localhost:8000/api/password/reset?token=${formData.token}`, { // token na URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: formData.password }),
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Senha alterada com sucesso!');
      } else {
        setError(data.detail);
        toast.error('Erro ao alterar senha.');
      }
    } catch (error) {
      setError("Erro");
      toast.error('Erro ao alterar senha.');
    }
  };

  return (
    <div className="container-recuperar-pass">
      <h1>Recuperar Senha</h1>
      <form className="form-recuperar-pass" onSubmit={handleSubmit}>
        <div className="container-center">
          <input
            type="text"
            name="token"
            value={formData.token}
            onChange={handleChange}
            placeholder="Token"
          />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Nova Senha"
          />
          <div className="container-btn">
            <button className="btn" type="submit">
              Alterar Senha
            </button>
          </div>
          <p className="erro">{error && error}</p>
        </div>
      </form>
      <ToastContainer />
    </div>
  );
}

export default RecuperarPass;
