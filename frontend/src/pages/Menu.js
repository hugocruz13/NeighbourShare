import { useAuth } from "../context/AuthContext";
import { Link } from 'react-router-dom';
import "../styles/Menu.css";

function Residente() {
    const { user } = useAuth();

    return (
      <div className="page-content">
        <div className="home-containerMenu">

          <p className="menu-title">Menu Principal</p>
          <div className="botoes">
            <Link className="btnMenu" to="/recursosDisponiveis">Recursos Disponiveis</Link><br></br>
            <Link className="btnMenu" to="/pedidosReserva">Pedidos Reserva</Link><br></br>
            <Link className="btnMenu" to="/perfil">Perfil</Link><br></br>
            <Link className="btnMenu" to="/meusRecursos">Meus Recursos</Link><br></br>
            <Link className="btnMenu" to="/listaPedidosReserva">Pedidos de Reserva</Link><br></br>
            <Link className="btnMenu" to="/listaReserva">Lista Reservas</Link><br></br>
            <Link className="btnMenu" to="/realizarPedidoNovoRecurso">Realizar Pedido Novo Recurso</Link><br></br>
            <Link className="btnMenu" to="/notificacoes">Notificações</Link><br></br>

            {user?.role === "gestor" || user?.role === "admin" && (
            
              <Link className="btnMenu" to="/pedidosNovosRecursos">Pedidos Novos Recursos (Pendentes)</Link>
            
          )}
          </div>
        </div>
        </div>
      );
  }
  
  export default Residente;
  