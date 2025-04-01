import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
        credentials: "include",  // Envia cookies com a requisição
      });

      const data = await response.json();

      if (response.ok) {
        navigate("/menu");  // Após o login com sucesso, redireciona para o menu
      } else {
        setError(data.detail || "Erro ao fazer login");
      }
    } catch (error) {
      setError("Erro");
    }
  };

  return (
    <div className="paginaLogin">

      <div class="esquerdaLogin">
        <h1 class="h1Login">Login</h1>

        <div class="formularioLogin">

          <form class="formulario" onSubmit={handleSubmit}>

            <h2>Login</h2>

            <div class="inputsLogin">
              <label>Email</label><br></br>
              <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>

            <div class="inputsLogin">
              <label>Password</label><br></br>
              <input type="password" name="password" value={formData.password} onChange={handleChange} required />
            </div>

            <div>
              <button class="btn" type="submit">Login</button>
            </div>
          </form>

        </div>
        
      </div>

      <div class="direitaLogin">
        <img class="imagem" src="/images/fundo.png" alt="Imagem" />
      </div>

      
    </div>
  );
}
