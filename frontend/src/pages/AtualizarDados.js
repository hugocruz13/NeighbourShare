import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const AtualizarDados = () => {
  const [dataNascimento, setDataNascimento] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [foto, setFoto] = useState(null);

  const location = useLocation();

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const tokenFromUrl = queryParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    }
  }, [location]);

  const handleUpdate = async () => {
    const formData = new FormData();
    formData.append('dataNascimento', dataNascimento);
    formData.append('email', email);
    formData.append('password', password);
    formData.append('token', token);
    if (foto) {
      formData.append('foto', foto);
    }

    try {
      const res = await fetch('http://localhost:8000/api/register/atualizar_dados', {
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
      setEmail('');
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
        <input
          type="date"
          placeholder="Data de Nascimento"
          value={dataNascimento}
          onChange={(e) => setDataNascimento(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="file"
          onChange={(e) => setFoto(e.target.files[0])}
        />
        <button onClick={handleUpdate}>Atualizar</button>
      </div>
      <ToastContainer />
    </div>
  );
};

export default AtualizarDados;
