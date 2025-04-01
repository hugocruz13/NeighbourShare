import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Menu() {
  const navigate = useNavigate();
  const [role, setRole] = useState(null);

  useEffect(() => {
    async function fetchUserRole() {
      try {
        const response = await fetch("http://localhost:8000/user-role", {
          method: "GET",
          credentials: "include", // Envia cookies na requisição
        });

        const data = await response.json();
        setRole(data.role);
      } catch (error) {
        console.error("Erro ao obter o tipo de utilizador:", error);
        navigate("/login");  // Se houver erro, redireciona para login
      }
    }

    fetchUserRole();
  }, [navigate]);

  return (
    <div className="page">
      <h2>Menu Principal</h2>
      
      {role === "vizinho" && (
        <>
          <h3>Opções para Vizinhos</h3>
          <ul>
            <li><a href="#">Recursos Disponíveis</a></li>
            <li><a href="#">Realizar Pedidos de Manutenção</a></li>
            <li><a href="#">Aquisição de Novos Recursos</a></li>
            <li><a href="#">Os Meus Pedidos</a></li>
            <li><a href="#">As Minhas Reservas</a></li>
          </ul>
        </>
      )}

      {role === "gestor" && (
        <>
          <h3>Opções para Gestores</h3>
          <ul>
            <li><a href="#">Recursos Disponíveis</a></li>
            <li><a href="#">Realizar Pedidos de Manutenção</a></li>
            <li><a href="#">Aquisição de Novos Recursos</a></li>
            <li><a href="#">Os Meus Pedidos</a></li>
            <li><a href="#">As Minhas Reservas</a></li>
            <li><a href="#">Pedidos de Manutenção</a></li>
            <li><a href="#">Pedidos de Novos Recursos</a></li>
          </ul>
        </>
      )}

    
    </div>
  );
}
