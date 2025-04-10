import { useAuth } from "../context/AuthContext";
import { Link } from 'react-router-dom';
import "../styles/Menu.css";

function Residente() {
    const { user } = useAuth();

    return (
        <div className="home-container">
          <div className="botoes">

          <div className="btnMenu">
            <Link className="textBtn" to="/recursosDisponiveis">Recursos Disponiveis</Link><br></br>
          </div>
          <div className="btnMenu">
            <Link className="textBtn" to="/pedidosReserva">Pedidos Reserva</Link><br></br>
          </div>
          <div className="btnMenu">
            <Link className="textBtn" to="/perfil">Perfil</Link><br></br>
          </div>
          <div className="btnMenu">
            <Link className="textBtn" to="/meusRecursos">Meus Recursos</Link><br></br>
          </div>

          {user?.role === "gestor" || user?.role === "admin" && (
            
            <div>
              <div className="btnMenu">
                <Link className="textBtn" to="/pedidosNovosRecursos">Pedidos Novos Recursos - Pendentes</Link><br></br>
              </div>
              
            </div>
            
          )}
          </div>
        </div>
      );
  }
  
  export default Residente;
  