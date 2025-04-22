import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar2 from "../components/Navbar2.js";
import "../styles/Perfil.css";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ProfilePage = () => {
  const [user, setUser] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/me", {
          method: 'GET',
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Erro ao buscar perfil');
        }

        const data = await response.json();
        console.log(data)
        setUser(data);
      } catch (error) {
        console.error('Erro:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleDeleteAccount = async () => {
    const confirm = window.confirm('Tem a certeza que deseja eliminar a conta?');
    if (!confirm) return;

    try {
      setDeleting(true);
      const response = await fetch("http://localhost:8000/api/deletarPerfil", {
        method: 'DELETE',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Erro ao eliminar conta');
      }

      alert('Conta eliminada com sucesso!');
      setShowModal(false);
      navigate('/login'); // ou outra página adequada
    } catch (error) {
      console.error('Erro:', error);
      alert('Não foi possível eliminar a conta.');
    }
  };

  return (
    <div className="home-container">
      <Navbar2 />

      <div className='fundoPerfil'>

        <div className='itensPerfil'>
          <div className='textosPerfil'>
            <img className='fotoPerfil' src={user?.foto} alt="Foto"></img>
          </div>

          <div className='textosPerfil'>
            <p>Utilizador</p>
            <p className='infoUser'>{user?.nome}</p>
          </div>

          <div className='textosPerfil'>
            <p>Email</p>
            <p className='infoUser'>{user?.email}</p>
          </div>    

          <div className='textosPerfil'>
            <p>Contacto</p>
            <p className='infoUser'>{user?.contacto}</p>
          </div>
        </div>
      </div>


      <button className="btn-deletePerfil" onClick={() => setShowModal(true)}>Eliminar Conta</button>

      {showModal && (
        <>
          <div className="modal-backdropDelete" onClick={() => setShowModal(false)} />
            <div className="modal-contentDelete">
              <h2>Tem a certeza que deseja eliminar a sua conta!</h2>

              <div>
                <button onClick={handleDeleteAccount}>Eliminar</button>
                <button onClick={() => setShowModal(false)}>Cancelar</button>
              </div>
          </div>
        </>

      )}



    </div>
  );
};

export default ProfilePage;
