import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/Navbar2.css";

function Navbar2() {
    const navigate = useNavigate();
    const [showMenu, setShowMenu] = useState(false);
    const [showNotifications, setShowNotifications] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [profileImage, setProfileImage] = useState('');

    const handlePerfilClick = () => setShowMenu(!showMenu);
    const handleBellClick = () => setShowNotifications(!showNotifications);

    const handleOutsideClick = (event) => {
        if (
            !event.target.closest('.fotoPerfilNav') &&
            !event.target.closest('.dropdown-menu') &&
            !event.target.closest('.notification-container') &&
            !event.target.closest('.notification-bell')
        ) {
            setShowMenu(false);
            setShowNotifications(false);
        }
    };

    const handleLogout = async () => {
        try {
            await fetch('http://localhost:8000/api/logout', {
                method: 'GET',
                credentials: 'include',
            });
            navigate('/login');
        } catch (error) {
            console.error('Erro ao fazer logout:', error);
        }
    };

    const marcarComoLida = async (NotificacaoID) => {
        try {
            const res = await fetch(`http://localhost:8000/api/notificacoes/${NotificacaoID}/lida`, {
                method: 'PUT',
                credentials: 'include'
            });
            if (!res.ok) {
                throw new Error('Erro ao marcar notificação como lida');
            }
            setNotifications(notifications.map(n =>
                n.NotificacaoID === NotificacaoID ? { ...n, Estado: true } : n
            ));
        } catch (error) {
            console.error('Erro ao marcar notificação como lida:', error);
        }
    };

    useEffect(() => {
        const fetchNotificacoes = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/notificacoes/', {
                    method: 'GET',
                    credentials: 'include'
                });
                const data = await res.json();
                console.log(data);
                setNotifications(data);
            } catch (error) {
                console.error('Erro ao buscar notificações:', error);
            }
        };

        const fetchProfileImage = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/perfil', {
                    method: 'GET',
                    credentials: 'include'
                });
                const data = await res.json();
                setProfileImage(data.imagem); // Assuming the response contains the URL of the profile image
            } catch (error) {
                console.error('Erro ao buscar imagem de perfil:', error);
            }
        };

        fetchNotificacoes();
        fetchProfileImage();
        document.addEventListener('click', handleOutsideClick);
        return () => {
            document.removeEventListener('click', handleOutsideClick);
        };
    }, []);

    return (
        <div className="navbar2">
            <div className="navLink">
                <ul className="links">
                    <li><Link to="/" className="link">Home</Link></li>
                    <li><Link to="/menu" className="link">Menu</Link></li>
                    <li><Link to="/contactos" className="link">Contactos</Link></li>
                </ul>
            </div>

            <div className="profile-section">
                <div className="notification-bell" onClick={handleBellClick}>
                    <img
                        src="https://cdn-icons-png.flaticon.com/512/1827/1827392.png"
                        alt="Notificações"
                        className="notification-icon-navbar"
                    />
                    {notifications.some(n => !n.Estado) && <span className="noti-dot"></span>}
                </div>

                {/* Painel lateral de notificações */}
                {showNotifications && (
                    <div className="notification-container">
                        <div className="notification-header">
                            <h3>Notificações</h3>
                            <Link to="/notificacoes" className="ver-todas">Ver todas</Link>
                        </div>
                        <div className="notification-list">
                            {notifications.filter(n => !n.Estado).length > 0 ? (
                                notifications.filter(n => !n.Estado).map(notif => (
                                    <div
                                        key={notif.NotificacaoID}
                                        className="notification-item nao-lida"
                                    >
                                        <span>{notif.Titulo.substring(0, 100)}...</span>
                                        <button onClick={() => marcarComoLida(notif.NotificacaoID)}>
                                            Marcar como lida
                                        </button>
                                    </div>
                                ))
                            ) : (
                                <p>Sem notificações de momento</p>
                            )}
                        </div>
                    </div>
                )}

                {/* Foto de perfil */}
                <img src={profileImage || "default-profile.png"} alt="foto" className="fotoPerfilNav" onClick={handlePerfilClick} />
                {showMenu && (
                    <div className="dropdown-menu">
                        <Link to="/perfil" className="dropdown-item">Perfil</Link>
                        <Link to="/reservas" className="dropdown-item">Minhas Reservas</Link>
                        <Link to="/pedidos" className="dropdown-item">Os meus Pedidos</Link>
                        <Link to="/definicoes" className="dropdown-item">Definições</Link>
                        <Link to="#" className="dropdown-item" onClick={handleLogout}>Terminar Sessão</Link>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Navbar2;
