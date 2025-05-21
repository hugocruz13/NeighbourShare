import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Input from '../components/Input.jsx';

const AtualizarDados = () => {
  const [data_nascimento, setDataNascimento] = useState('');
  const [nome, setNome] = useState('');
  const [contacto, setContacto] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [foto, setFoto] = useState(null);

  const location = useLocation();

  useEffect(() => {
    const search = location.search;
    if (search.startsWith('?')) {
      const tokenFromUrl = search.substring(1); // remove o '?'
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
    if (foto) {
      formData.append('foto', foto);
    }

    try {
      const res = await fetch('http://localhost:8000/api/registar/atualizar_dados', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error(errorData);
        throw new Error(errorData.detail || 'Erro ao atualizar dados');
      }

      toast.success('Dados atualizados com sucesso!');
      setDataNascimento('');
      setNome('');
      setContacto('');
      setPassword('');
      setFoto(null);
    } catch (error) {
      toast.error('Erro ao atualizar dados: ' + error.message);
    }
  };

  return (
    <div className="page-content">
      <div className="update-container">
        <h2>Atualizar Dados</h2>
        <Input value={data_nascimento} onChange={(e) => setDataNascimento(e.target.value)} placeholder="Data de Nascimento" type="date" variant="default"/>
        <Input value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Nome" type="text" variant="default"/>
        <Input value={contacto} onChange={(e) => setContacto(e.target.value)} placeholder="Contacto" type="number" variant="default"/>
        <Input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" variant="default"/>
        <Input onChange={(e) => setFoto(e.target.files[0])} type="file" variant="default"/>
  
        <button onClick={handleUpdate}>Atualizar</button>
      </div>
      <ToastContainer />
    </div>
  );
};

export default AtualizarDados;
