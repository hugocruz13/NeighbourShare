import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";
import { InputLogin, InputPassword } from "../components/Inputs.js";

function Login() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
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
        navigate("/menu");
      } else {
        setError(data.detail);
      }
    } catch (error) {
      setError("Erro");
    }
  };
  return (
    <div className="container-login">
      <div className="container-esquerda">
        <h1>Bem-vindo de volta!</h1>
        <div className="container-formulario">
          <form className="formulario" onSubmit={handleSubmit}>
            <h2>Acesse a sua conta!</h2>
            <div className="container-center">
              <InputLogin name={"email"} value={formData.email} onChange={handleChange} />
              <InputPassword name={"password"} value={formData.password} onChange={handleChange} /> 
              <div className="container-btn">
                <button className="btn" type="submit">Login</button>
              </div>
              <p className="erro">{error && error}</p>
            </div>
          </form>
        </div>
      </div>
      <div className="container-direita">
        <img className="imagem" src="img/fundo.jpg" alt="Imagem" />
      </div>
    </div>
  );
}

export default Login;
