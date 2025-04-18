import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.js";
import { InputLogin, InputPassword } from "../components/Inputs.js";
import "../styles/Login.css";

function Registar() {
  const [formData, setFormData] = useState({ email: "", role: "" });
  const [error, setError] = useState("");
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/api/registar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
        credentials: "include",
      });

      const data = await response.json();

      if (!response.ok) {
              throw new Error(data.detail || 'Erro ao registar.');
      }
      toast.success('Utilizador Registado com sucesso!');
    } catch (error) {
      setError("Erro");
    }
  };
  return (
    <div className="container-login">
      <div className="container-esquerda">
        <div className="container-formulario">
          <form className="formulario" onSubmit={handleSubmit}>
            <h2>Registar Utilizador</h2>
            <div className="container-center">
              <InputLogin
                name={"email"}
                value={formData.email}
                onChange={handleChange}
              />
              <InputPassword
                name={"password"}
                value={formData.password}
                onChange={handleChange}
              />
              <div className="container-btn">
                <button className="btn" type="submit">
                  Registar
                </button>
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

export default Registar;
