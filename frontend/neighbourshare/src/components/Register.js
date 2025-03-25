import { useState } from "react";

import "./Register.css";

export default function Register() {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    contacto: "",
    password: "",
    confirmarPassword: "",
    dataNascimento: "",
    permissoes: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Verifica se as passwords são iguais
    if (formData.password !== formData.confirmarPassword)
    {
      alert("As passwords não coincidem!");
      return;
    }


    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log("Successo:", data);
    } catch (error) {
      console.error("Erro:", error);
    }
  };

  return (
    <div class="pagina">
      <div class="esquerda">
        <img class="imagem" src="/images/fundo.png" alt="Imagem" />
      </div>

      <div class="direita">
        <h1>Bem-Vindo</h1>

        <div class="formulario">
          <h2>Registar Conta</h2>

          <form class="formulario" onSubmit={handleSubmit}>

            <div class="inputs">
              <label>Nome Completo</label><br></br>
              <input class="caixaNome" type="text" name="nome" value={formData.nome} onChange={handleChange} required/>
            </div>

          <div class="conjuntoInput">
            <div>
              <div class="inputs">
                <label>Email</label><br></br>
                <input type="email" name="email" value={formData.email} onChange={handleChange} required/>
              </div>

              <div class="inputs">
                <label>Password</label><br></br>
                <input type="password" name="password" value={formData.password} onChange={handleChange} required/>
              </div>

              <div class="inputs">
                <label>Data de Nascimento</label><br></br>
                <input type="date" name="dataNascimento" value={formData.dataNascimento} onChange={handleChange} required/>
              </div>
            </div>
            
            <div>
              <div class="inputs">
                <label>Contacto</label><br></br>
                <input type="tel" name="contacto" value={formData.contacto} onChange={handleChange} required/>
              </div>

              <div class="inputs">
                <label>Confirmar Password</label><br></br>
                <input type="password" name="confirmarPassword" value={formData.confirmarPassword} onChange={handleChange} required/>
              </div>

              <div class="inputs">
                <label>Permissões</label><br></br>
                <select name="permissoes" value={formData.permissoes} onChange={handleChange} required>
                  <option value="">Selecione...</option>
                  <option value="gestor">Gestor</option>
                  <option value="vizinho">Vizinho</option>
                </select>
              </div>
            </div>
          </div>

          <div class="botao">
            <button class="btn" type="submit">Criar Conta</button>
          </div>
          </form>
        </div>
      </div>
    </div>
  );
}
