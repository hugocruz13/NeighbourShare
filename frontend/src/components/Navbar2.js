import { Link, useNavigate } from "react-router-dom";
import "../styles/Navbar2.css"

function Navbar2() {
    const navigate = useNavigate();

    const handlePerfilClick = () => {
        navigate("/perfil");
    };

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
                    <Link to="/contactos"className="link">Contactos</Link>
                </li>
            </ul>
            </div>


            <img src="" alt="foto" className="fotoPerfilNav" onClick={handlePerfilClick}></img>
    
            
        </div>
    );
}

export default Navbar2;
