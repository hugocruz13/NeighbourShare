import { useAuth } from "../context/AuthContext";
import { Link } from 'react-router-dom';
import "../styles/Menu.css";
import Navbar2 from "../components/Navbar2.js";
function Residente() {
    const { user } = useAuth();

    return (
      <div className="page-content">
        <Navbar2 />
        <div className="home-containerMenu">

          <p className="menu-title">Menu Principal</p>
          <div className="botoes">
            <Link className="btnMenu" to="/recursosDisponiveis">Recursos Disponiveis</Link><br></br>
            <Link className="btnMenu" to="/perfil">Perfil</Link><br></br>
            <Link className="btnMenu" to="/meusRecursos">Meus Recursos</Link><br></br> 
            <Link className="btnMenu" to="/listaPedidosReserva">Pedidos de Reserva</Link><br></br>
            <Link className="btnMenu" to="/listaReserva">Lista Reservas</Link><br></br>
            <Link className="btnMenu" to="/realizarPedidoNovoRecurso">Realizar Pedido Novo Recurso</Link><br></br>
            <Link className="btnMenu" to="/notificacoes">Notificações</Link><br></br>
            <Link className="btnMenu" to="/realizarPedidoManutencao">Realizar Pedido Manutenção</Link><br></br>
            <Link className="btnMenu" to="/votacoes">Votações</Link><br></br>
            <Link className="btnMenu" to="/pedidosNovosRecursosPendentesVoto">Votar Pedidos Novos Recursos (Pendentes)</Link><br></br>

            {user?.role === "gestor" || user?.role === "admin" && (
              <>
              <Link className="btnMenu" to="/pedidosNovosRecursos">Pedidos Novos Recursos (Pendentes)</Link><br></br>
              <Link className="btnMenu" to="/pedidosManutencao">Pedidos Manutenção (Pendentes)</Link><br></br>
              <Link className="btnMenu" to="/orcamentos">Orçamentos</Link><br></br>
              <Link className="btnMenu" to="/registar">Registar</Link><br></br>
              </>
              
            
          )}
          </div>
        </div>
        </div>
      );
  }
  
  export default Residente;
  