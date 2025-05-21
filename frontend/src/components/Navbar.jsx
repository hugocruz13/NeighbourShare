import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import Button from "./Button";
import styles from "./Navbar.module.css";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  // Detectar scroll para mudar o estilo do navbar
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const handleLoginClick = () => {
    navigate("/login");
  };

  // Fechar menu móvel após clique em link
  const handleLinkClick = () => {
    if (menuOpen) setMenuOpen(false);
  };

  return (
    <nav className={`${styles.navbar} ${scrolled ? styles.scrolled : ""}`}>
      <div className={styles["navbar-container"]}>
        <Link to="/" className={styles.logo}>
          <span className={styles["logo-text"]}>Neighbour Share</span>
        </Link>

        <div
          className={`${styles["menu-icon"]} ${menuOpen ? styles.active : ""}`}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </div>

        <div
          className={`${styles["nav-elements"]} ${
            menuOpen ? styles.active : ""
          }`}
        >
          <ul className={styles.links}>
            <li>
              <a
                href="/"
                className={styles.link} 
                onClick={handleLinkClick}
              >
                Home
              </a>
            </li>
            <li>
              <a
                href="#sobre"
                className={styles.link}
                onClick={handleLinkClick}
              >
                Sobre
              </a>
            </li>
            <li>
              <a
                href="#funcionalidades"
                className={styles.link}
                onClick={handleLinkClick}
              >
                  Funcionalidades
              </a>
            </li>
            <li>
              <a
                href="#contacto"
                className={styles.link}
                onClick={handleLinkClick}
              >
                Contactos
              </a>
            </li>
          </ul>
          <Button variant="login" onClick={handleLoginClick}>
            Login
          </Button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
