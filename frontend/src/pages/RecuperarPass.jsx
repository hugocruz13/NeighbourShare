import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import Input from '../components/Input.jsx';
import Button from '../components/Button.jsx';
import Navbar from "../components/Navbar.jsx";
import 'react-toastify/dist/ReactToastify.css';
import "../styles/RecuperarPass.css";

function RecuperarPass() {
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [error, setError] = useState("");
  const location = useLocation();
  const navigate = useNavigate(); 

  useEffect(() => {
    const search = location.search;
    if (search.startsWith('?')) {
      const tokenFromUrl = search.substring(1); // remove o '?'
      setToken(tokenFromUrl);
    }
  }, [location]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`http://localhost:8000/api/password/reset?token=${token}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        ToastManager.success('Senha alterada com sucesso!');
        setPassword("");

        // Aguarda 2 segundos para mostrar o toast e depois redireciona
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setError(data.detail);
        ToastManager.error('Erro ao alterar senha.');
      }
    } catch (error) {
      setError("Erro");
      ToastManager.error('Erro ao alterar senha.');
    }
  };

  return (
    <div>
      <Navbar />
    <div className="container-recuperar-pass">
      <h1>Recuperar Senha</h1>
      <form className="form-recuperar-pass" onSubmit={handleSubmit}>
        <div className="container-center">
          <Input className="inputNovaPass" name="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Nova Senha" type="password"/>

          <div className="container-btn">
            <Button className='btn' type="submit" text={"Alterar Senha"}>Alterar Senha</Button>
          </div>
          <p className="erro">{error && error}</p>
        </div>
      </form>
      <Toaster />
    </div>
    </div>

  );
}

export default RecuperarPass;