import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../styles/AtualizarDados.css'; // importa o CSS personalizado
import Input from '../components/Input.jsx';
import Button from '../components/Button.jsx';
import Navbar from "../components/Navbar.jsx";

const AtualizarDados = () => {
  const [data_nascimento, setDataNascimento] = useState('');
  const [nome, setNome] = useState('');
  const [contacto, setContacto] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [foto, setFoto] = useState(null);

  const location = useLocation();
  const navigate = useNavigate(); 

  useEffect(() => {
    const search = location.search;
    if (search.startsWith('?')) {
      const tokenFromUrl = search.substring(1);
      setToken(tokenFromUrl);
    }
  }, [location]);

  const handleUpdate = async () => {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d])([^\s]){8,}$/;

    if (!passwordRegex.test(password)) {
      toast.error('Password inválida. Deve ter pelo menos 8 caracteres, incluindo uma maiúscula, uma minúscula, um número e um carácter especial.');
      return;
    }

    const formData = new FormData();
    formData.append('data_nascimento', data_nascimento);
    formData.append('nome', nome);
    formData.append('contacto', contacto);
    formData.append('password', password);
    formData.append('token', token);
    if (foto) formData.append('foto', foto);

    try {
      const res = await fetch('http://localhost:8000/api/registar/atualizar_dados', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Erro ao atualizar dados');
      }

      toast.success('Dados atualizados com sucesso!');
      setDataNascimento('');
      setNome('');
      setContacto('');
      setPassword('');
      setFoto(null);

      setTimeout(() => {
        navigate('/login'); 
      }, 2000);
    } catch (error) {
      toast.error('Erro ao atualizar dados: ' + error.message);
    }
  };

  return (
    <div>
      <Navbar />
    <div className="page-content-update">
      
      <div className="update-container">
        <h1>Atualizar Dados</h1>
        <Input value={data_nascimento} onChange={(e) => setDataNascimento(e.target.value)} placeholder="Data de Nascimento" type="date"/>
        <Input value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Nome" type="text" variant="default"/>
        <Input value={contacto} onChange={(e) => setContacto(e.target.value)} placeholder="Contacto" type="number" variant="default"/>
        <Input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" variant="default"/>
        <Input onChange={(e) => setFoto(e.target.files[0])} type="file" variant="default"/>
       
        <div className="btn-update-wrapper">
          <Button className='btn' variant= "login" onClick={handleUpdate} text={"Atualizar"}>Atualizar</Button>
        </div>
      </div>
      <ToastContainer />
    </div>
    </div>

  );
};

export default AtualizarDados;