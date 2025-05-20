import { Link, useNavigate } from "react-router-dom";
import "../styles/Navbar.css";

function Navbar() {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <ul className="links">
        <li><Link to="/" className="link">Home</Link></li>
        <li><Link to="/sobre" className="link">Sobre</Link></li>
        <li><Link to="/funcionalidade" className="link">Funcionalidades</Link></li>
        <li><Link to="/contactos" className="link">Contactos</Link></li>
      </ul>
      <button className="login-button" onClick={handleLoginClick}>Login</button>
    </nav>
  );
}

export default Navbar;
