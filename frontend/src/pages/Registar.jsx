import React, { useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/Registar.css";
import Input from '../components/Input.jsx';
import Select from '../components/Select.jsx';
import Navbar2 from "../components/Navbar2.js";
import Button from '../components/Button.jsx';

const Registar = () => {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('');

  const handleRegister = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/registar', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, role }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error(errorData);
        throw new Error(errorData.detail || 'Erro ao registrar utilizador');
      }

      toast.success('Utilizador registrado com sucesso!');
      setEmail('');
      setRole('');
    } catch (error) {
      toast.error('Erro ao registrar utilizador: ' + error.message);
    }
  };

  return (
    <div className="container-registar">
      <Navbar2 />
      <div className="container-esquerda">
        <br></br>
        <h1>Registar Utilizador</h1>
        <div className="container-formulario">
            <h2>Registar Novo Utilizador</h2><br></br>
            <div className="container-form">
              <Input  className="inputRegisto" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" type="email" variant="default"/>
              <Select className="inputRegisto" value={role} onChange={(e) => setRole(e.target.value)} placeholder="Escolha a função"
                options={[
                { value: "residente", label: "Residente" },
                { value: "gestor", label: "Gestor" },
                { value: "admin", label: "Admin" }
                ]}
                variant="default"/>             
              <div className="container-btn">
                <Button className='btn' onClick={handleRegister} text={"Registrar"}>Registrar</Button>
              </div>
            </div>
        </div>
      </div>
      <div className="container-direita">
        <img className="imagem" src="img/new.jpg" alt="Imagem" />
      </div>
      <ToastContainer />
    </div>

        
  );
};

export default Registar;