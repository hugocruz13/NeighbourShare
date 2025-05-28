import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.js";
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import "../styles/Login.css";
import Button from "../components/Button.jsx";
import Input from '../components/Input.jsx';

function Login() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [emailRecuperacao, setEmailRecuperacao] = useState("");
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        const res = await fetch("http://localhost:8000/api/me", {
          credentials: "include",
        });
        const userData = await res.json();
        setUser(userData);

        if (userData.role === "admin") {
          navigate("/menu");
        } else if (userData.role === "residente" || userData.role === "gestor") {
          navigate("/menu");
        } else {
          navigate("/login");
        }
      } else {
        ToastManager.error("Email ou password inválidos.");
      }
    } catch (error) {
      ToastManager.error("Erro ao fazer login.");
    }
  };

  const handleRecuperacaoSenha = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/password/forgot", { // endpoint para recuperação de senha
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: emailRecuperacao }),
        credentials: "include",
      });

      if (response.ok) {
        ToastManager.success('Email de recuperação enviado com sucesso!');
        setShowModal(false);
      } else {
        ToastManager.error('Erro ao enviar email de recuperação.');
      }
    } catch (error) {
      ToastManager.error('Erro ao enviar email de recuperação.');
    }
  };

  return (
    <div className="container-login">
      <div className="container-esquerda">
        <div className="container-formulario">
          <h1>Bem-vindo de volta!</h1>
          <form className="formulario" onSubmit={handleSubmit}>
            <h2 className="subtitle">Acesse a sua conta!</h2>
            <div className="container-center">
              <Input className="input" name="email" value={formData.email} onChange={handleChange} placeholder="Email" type="email" variant="geral"/>
              <Input name="password" value={formData.password} onChange={handleChange} placeholder="Password" type="password" variant="geral"></Input>
              <div className="container-button">
                <Button className="btn-login" variant= "login"  type="submit" text={"Entrar"}>Entrar</Button>
              </div>
              <p className="erro">{error && error}</p>
              <p className="link-recuperacao" onClick={() => setShowModal(true)}>Esqueceu a senha?</p>
            </div>
          </form>
        </div>
      </div>
      <div className="container-direita">
        <img className="imagem" src="img/fundo.jpg" alt="Imagem" />
      </div>
      {showModal && (
        <>
          <div className="modal-backdrop" onClick={() => setShowModal(false)} />
          <div className="modal-content">
            <h3>Recuperação de Senha</h3>
            <p>Digite seu email para receber instruções de recuperação de senha.</p>
            <Input name="emailRecuperacao" value={emailRecuperacao} onChange={(e) => setEmailRecuperacao(e.target.value)} placeholder="email" type="email" variant="modal"/>
            <button onClick={handleRecuperacaoSenha}>Enviar</button>
            <button onClick={() => setShowModal(false)}>Cancelar</button>
          </div>
        </>
      )}
      <Toaster />
    </div>
  );
}

export default Login;
