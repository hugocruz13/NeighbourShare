import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/Navbar2.css";

function Navbar2() {
    const navigate = useNavigate();
    const [showMenu, setShowMenu] = useState(false);

    const handlePerfilClick = () => {
        setShowMenu(!showMenu);
    };

    const handleOutsideClick = (event) => {
        if (!event.target.closest('.fotoPerfilNav') && !event.target.closest('.dropdown-menu')) {
            setShowMenu(false);
        }
    };

    // Add event listener to close the menu when clicking outside
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
                    <li>
                        <Link to="/" className="link">Home</Link>
                    </li>
                    <li>
                        <Link to="/menu" className="link">Menu</Link>
                    </li>
                    <li>
                        <Link to="/contactos" className="link">Contactos</Link>
                    </li>
                </ul>
            </div>

            <div className="profile-container">
                <img src="123.png" alt="foto" className="fotoPerfilNav" onClick={handlePerfilClick} />
                {showMenu && (
                    <div className="dropdown-menu">
                        <Link to="/perfil" className="dropdown-item">Perfil</Link>
                        <Link to="/reservas" className="dropdown-item">Minhas Reservas</Link>
                        <Link to="/pedidos" className="dropdown-item">Os meus Pedidos</Link>
                        <Link to="/definicoes" className="dropdown-item">Definições</Link>
                        <Link to="/logout" className="dropdown-item">Terminar Sessão</Link>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Navbar2;
