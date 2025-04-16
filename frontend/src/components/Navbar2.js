import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/Navbar2.css";

function Navbar2() {
    const navigate = useNavigate();
    const [showMenu, setShowMenu] = useState(false);
    const [showNotifications, setShowNotifications] = useState(false);
    const [notifications, setNotifications] = useState([
        { id: 1, message: "Nova reserva aprovada", read: false },
        { id: 2, message: "Recurso foi devolvido com sucesso", read: true },
        { id: 3, message: "Pedido de novo recurso foi aceite", read: false },
    ]);

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

    const toggleRead = (id) => {
        setNotifications(notifications.map(n =>
            n.id === id ? { ...n, read: !n.read } : n
        ));
    };

    useEffect(() => {
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
        className="notification-icon"
    />
    {notifications.some(n => !n.read) && <span className="noti-dot"></span>}
</div>


                {/* Painel lateral de notificações */}
                {showNotifications && (
                    <div className="notification-container">
                        <div className="notification-header">
                            <Link to="/notificacoes" className="ver-todas">Ver todas as notificações</Link>
                        </div>
                        <div className="notification-list">
                            {notifications.map(notif => (
                                <div
                                    key={notif.id}
                                    className={`notification-item ${notif.read ? "lida" : "nao-lida"}`}
                                >
                                    <span>{notif.message}</span>
                                    <button onClick={() => toggleRead(notif.id)}>
                                        Marcar como {notif.read ? "não lida" : "lida"}
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Foto de perfil */}
                <img src="123.png" alt="foto" className="fotoPerfilNav" onClick={handlePerfilClick} />
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
