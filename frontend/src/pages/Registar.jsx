import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import ToastManager from '../components/ToastManager.jsx';
import Input from '../components/Input.jsx';
import Select from '../components/Select.jsx';
import Navbar2 from "../components/Navbar2.jsx";
import Button from '../components/Button.jsx';
import 'react-toastify/dist/ReactToastify.css';
import "../styles/Registar.css";

const Registar = () => {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('');

  const roleOptions = [
    { value: "residente", label: "Residente" },
    { value: "gestor", label: "Gestor" },
    { value: "admin", label: "Admin" }
  ];

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

      ToastManager.success('Utilizador registrado com sucesso!');
      setEmail('');
      setRole('');
    } catch (error) {
      ToastManager.error('Erro ao registrar utilizador: ' + error.message);
    }
  };  return (
    <div className="registar-container">
      <Navbar2 />
      <div className="registar-content">
        <div className="registar-container-esquerda">
          <div className="registar-container-formulario">
            <h1 className="registar-titulo">Registar Utilizador</h1>
            <h2 className="registar-subtitulo">Junte-se à nossa vizinhança!</h2>
            <div className="registar-container-form">
              <Input 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="Email" 
                type="email" 
                variant="geral"
              />              <Select 
                value={roleOptions.find(option => option.value === role) || null} 
                onChange={(e) => setRole(e.target.value)} 
                placeholder="Escolha a função"
                options={roleOptions}
                variant="geral"
              />
              <div className="registar-container-btn">
                <Button className='registar-btn' onClick={handleRegister} text={"Registrar"}>
                  Registrar
                </Button>
              </div>
            </div>
          </div>
        </div>
        <div className="registar-container-direita">
          <img className="registar-imagem" src="img/new.jpg" alt="Imagem" />
        </div>
      </div>
      <Toaster />
    </div>

        
  );
};

export default Registar;