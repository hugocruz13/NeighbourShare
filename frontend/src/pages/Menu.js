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

          {/* Links comuns a todos */}
          <Link className="btnMenu" to="/perfil">Perfil</Link><br />
          <Link className="btnMenu" to="/notificacoes">Notificações</Link><br />
          <Link className="btnMenu" to="/listaPedidosReserva">Pedidos de Reserva</Link><br />
          <Link className="btnMenu" to="/listaReservas">Reservas</Link><br />
          <Link className="btnMenu" to="/meusRecursos">Meus Recursos</Link><br />
          <Link className="btnMenu" to="/realizarPedidoManutencao">Realizar Pedido Manutenção</Link><br />
          <Link className="btnMenu" to="/realizarPedidoNovoRecurso">Realizar Pedido Novo Recurso</Link><br />
          <Link className="btnMenu" to="/recursosDisponiveis">Recursos Disponíveis</Link><br />
          <Link className="btnMenu" to="/votacoes">Votações</Link><br />

          {/* Apenas Gestores */}
          {user?.role === "gestor" && (
            <>´
              <Link className="btnMenu" to="/manutencao">Manutenções</Link><br />
              <Link className="btnMenu" to="/entidadeExterna">Entidades Externas</Link><br />
              <Link className="btnMenu" to="/orcamentos">Orçamentos</Link><br />
              <Link className="btnMenu" to="/pedidosManutencao">Pedidos Manutenção</Link><br />
              <Link className="btnMenu" to="/pedidosNovosRecursos">Pedidos Novos Recursos</Link><br />
            </>
          )}

          {/* Apenas Admins */}
          {user?.role === "admin" && (
            <>
              <Link className="btnMenu" to="/registar">Registar</Link><br />
            </>
          )}

        </div>
      </div>
    </div>
  );
}

export default Residente;
