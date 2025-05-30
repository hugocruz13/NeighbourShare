import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import styles from "./Navbar2.module.css";

function Navbar2() {
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [profileImage, setProfileImage] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  // Refs para detectar cliques fora dos elementos
  const fotoPerfilRef = useRef(null);
  const dropdownMenuRef = useRef(null);
  const notificationContainerRef = useRef(null);
  const notificationBellRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handlePerfilClick = () => setShowMenu(!showMenu);
  const handleBellClick = () => setShowNotifications(!showNotifications);

  const handleOutsideClick = (event) => {
    const target = event.target;
    if (
      fotoPerfilRef.current && !fotoPerfilRef.current.contains(target) &&
      dropdownMenuRef.current && !dropdownMenuRef.current.contains(target) &&
      notificationContainerRef.current && !notificationContainerRef.current.contains(target) &&
      notificationBellRef.current && !notificationBellRef.current.contains(target)
    ) {
      setShowMenu(false);
      setShowNotifications(false);
    }
  };

  const handleLinkClick = () => {
    if (menuOpen) setMenuOpen(false);
  };

  const handleLogout = async () => {
    try {
      await fetch("http://localhost:8000/api/logout", {
        method: "GET",
        credentials: "include",
      });
      navigate("/login");
    } catch (error) {
      console.error("Erro ao fazer logout:", error);
    }
  };

  const marcarComoLida = async (NotificacaoID) => {
    try {
      const res = await fetch(`http://localhost:8000/api/notificacoes/${NotificacaoID}/lida`, {
        method: "PUT",
        credentials: "include",
      });
      if (!res.ok) throw new Error("Erro ao marcar notificação como lida");

      setNotifications(
        notifications.map((n) =>
          n.NotificacaoID === NotificacaoID ? { ...n, Estado: true } : n
        )
      );
    } catch (error) {
      console.error("Erro ao marcar notificação como lida:", error);
    }
  };

  useEffect(() => {
    const fetchNotificacoes = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/notificacoes/", {
          method: "GET",
          credentials: "include",
        });
        const data = await res.json();
        setNotifications(data);
      } catch (error) {
        console.error("Erro ao buscar notificações:", error);
      }
    };

    const fetchProfileImage = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/perfil", {
          method: "GET",
          credentials: "include",
        });
        const data = await res.json();
        setProfileImage(data.imagem);
      } catch (error) {
        console.error("Erro ao buscar imagem de perfil:", error);
      }
    };

    fetchNotificacoes();
    fetchProfileImage();
    document.addEventListener("click", handleOutsideClick);
    return () => document.removeEventListener("click", handleOutsideClick);
  }, []);

  return (
    <nav className={`${styles.navbar} ${scrolled ? styles.scrolled : ""}`}>
      <div className={styles.navbarContainer}>
        <div
          className={`${styles.menuIcon} ${menuOpen ? styles.active : ""}`}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </div>

        <div className={`${styles.navElements} ${menuOpen ? styles.active : ""}`}>
          <ul className={styles.links}>
            <li><Link to="/" className={styles.link} onClick={handleLinkClick}>Home</Link></li>
            <li><Link to="/menu" className={styles.link} onClick={handleLinkClick}>Menu</Link></li>
          </ul>

          <div className={styles.profileSection}>
            <div ref={notificationBellRef} className={styles.notificationBell} onClick={handleBellClick}>
              <img
                src="https://cdn-icons-png.flaticon.com/512/1827/1827392.png"
                alt="Notificações"
                className={styles.notificationIconNavbar}
              />
              {notifications.some((n) => !n.Estado) && <span className={styles.notiDot}></span>}
            </div>

            {showNotifications && (
              <div ref={notificationContainerRef} className={styles.notificationContainer}>
                <div className={styles.notificationHeader}>
                  <h3>Notificações</h3>
                  <Link to="/notificacoes" className={styles.verTodas}>Ver todas</Link>
                </div>
                <div className={styles.notificationList}>
                  {notifications.filter((n) => !n.Estado).length > 0 ? (
                    notifications
                      .filter((n) => !n.Estado)
                      .map((notif) => (
                        <div key={notif.NotificacaoID} className={`${styles.notificationItem} ${styles.naoLida}`}>
                          <span>{notif.Titulo.substring(0, 100)}...</span>
                          <button onClick={() => marcarComoLida(notif.NotificacaoID)}>Marcar como lida</button>
                        </div>
                      ))
                  ) : (
                    <p>Sem notificações de momento</p>
                  )}
                </div>
              </div>
            )}

            <img
              ref={fotoPerfilRef}
              src={profileImage || "default-profile.png"}
              alt="foto"
              className={styles.fotoPerfilNav}
              onClick={handlePerfilClick}
            />
            {showMenu && (
              <div ref={dropdownMenuRef} className={styles.dropdownMenu}>
                <Link to="/perfil" className={styles.dropdownItem}>Perfil</Link>
                <Link to="#" className={styles.dropdownItem} onClick={handleLogout}>Terminar Sessão</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar2;