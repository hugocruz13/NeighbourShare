import { useAuth } from "../context/AuthContext";
import { useNavigate } from 'react-router-dom';
import "../styles/Menu.css";
import Navbar2 from "../components/Navbar2.js";
import Button from "../components/Button.jsx";
import { useState, useEffect } from "react";

function Residente() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) {
      setGreeting("Bom dia");
    } else if (hour >= 12 && hour < 18) {
      setGreeting("Boa tarde");
    } else {
      setGreeting("Boa noite");
    }
  }, []);

  const navigateTo = (path) => {
    navigate(path);
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>{greeting}, <span className="user-name">{user?.name || 'Vizinho'}</span></h1>
          <p className="welcome-text">Bem-vindo ao seu painel de gestão NeighbourShare</p>
        </div>
        
        <div className="dashboard-grid">
          {/* Cards principais para todos os usuários */}
          <div className="dashboard-card" onClick={() => navigateTo('/perfil')}>
            <div className="card-icon user-icon"></div>
            <h3>Meu Perfil</h3>
            <Button variant="default" onClick={() => navigateTo('/perfil')}>Acessar</Button>
          </div>

          <div className="dashboard-card" onClick={() => navigateTo('/notificacoes')}>
            <div className="card-icon notification-icon"></div>
            <h3>Notificações</h3>
            <Button variant="default" onClick={() => navigateTo('/notificacoes')}>Visualizar</Button>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateTo('/recursosDisponiveis')}>
            <div className="card-icon resources-icon"></div>
            <h3>Recursos Disponíveis</h3>
            <Button variant="default" onClick={() => navigateTo('/recursosDisponiveis')}>Explorar</Button>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateTo('/listaReserva')}>
            <div className="card-icon booking-icon"></div>
            <h3>Minhas Reservas</h3>
            <Button variant="default" onClick={() => navigateTo('/listaReserva')}>Gerenciar</Button>
          </div>

          <div className="dashboard-card" onClick={() => navigateTo('/listaPedidosReserva')}>
            <div className="card-icon requests-icon"></div>
            <h3>Pedidos de Reserva</h3>
            <Button variant="default" onClick={() => navigateTo('/listaPedidosReserva')}>Verificar</Button>
          </div>

          <div className="dashboard-card" onClick={() => navigateTo('/meusRecursos')}>
            <div className="card-icon my-resources-icon"></div>
            <h3>Meus Recursos</h3>
            <Button variant="default" onClick={() => navigateTo('/meusRecursos')}>Visualizar</Button>
          </div>          <div className="dashboard-card" onClick={() => navigateTo('/votacoes')}>
            <div className="card-icon vote-icon"></div>
            <h3>Votações Ativas</h3>
            <Button variant="default" onClick={() => navigateTo('/votacoes')}>Participar</Button>
          </div>
          
          <div className="dashboard-card action-card">
            <div className="card-icon maintenance-request-icon"></div>
            <h3>Solicitar Manutenção</h3>
            <Button variant="green" onClick={() => navigateTo('/realizarPedidoManutencao')}>Solicitar</Button>
          </div>
          
          <div className="dashboard-card action-card">
            <div className="card-icon new-resource-icon"></div>
            <h3>Pedir Novo Recurso</h3>
            <Button variant="green" onClick={() => navigateTo('/realizarPedidoNovoRecurso')}>Criar Pedido</Button>
          </div>
        </div>

        {/* Seção para Gestores */}
        {user?.role === "gestor" && (
          <div className="management-section">
            <h2 className="section-title">Gestão do Condomínio</h2>
            <div className="admin-grid">
              <div className="admin-card" onClick={() => navigateTo('/manutencao')}>
                <h3>Manutenções</h3>
                <Button variant="default" onClick={() => navigateTo('/manutencao')}>Acessar</Button>
              </div>
              <div className="admin-card" onClick={() => navigateTo('/entidadeExterna')}>
                <h3>Entidades Externas</h3>
                <Button variant="default" onClick={() => navigateTo('/entidadeExterna')}>Gerenciar</Button>
              </div>
              <div className="admin-card" onClick={() => navigateTo('/orcamentos')}>
                <h3>Orçamentos</h3>
                <Button variant="default" onClick={() => navigateTo('/orcamentos')}>Visualizar</Button>
              </div>
              <div className="admin-card" onClick={() => navigateTo('/pedidosManutencao')}>
                <h3>Pedidos de Manutenção</h3>
                <Button variant="default" onClick={() => navigateTo('/pedidosManutencao')}>Avaliar</Button>
              </div>
              <div className="admin-card" onClick={() => navigateTo('/pedidosNovosRecursos')}>
                <h3>Pedidos de Novos Recursos</h3>
                <Button variant="default" onClick={() => navigateTo('/pedidosNovosRecursos')}>Analisar</Button>
              </div>
              <div className="admin-card" onClick={() => navigateTo('/recursosComuns')}>
                <h3>Recursos Comuns</h3>
                <Button variant="default" onClick={() => navigateTo('/recursosComuns')}>Gerenciar</Button>
              </div>
            </div>
          </div>
        )}

        {/* Seção para Admins */}
        {user?.role === "admin" && (
          <div className="management-section">
            <h2 className="section-title">Administração do Sistema</h2>
            <div className="admin-grid">
              <div className="admin-card" onClick={() => navigateTo('/registar')}>
                <h3>Registrar Novos Usuários</h3>
                <Button variant="default" onClick={() => navigateTo('/registar')}>Registrar</Button>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default Residente;
