import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Register from "./components/Register";
import Login from "./components/Login";
import Menu from "./components/Menu";

function App() {
  const [userRole, setUserRole] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Função para verificar se o utilizador está autenticado e obter o tipo de utilizador
  useEffect(() => {
    const checkUserRole = async () => {
      try {
        const response = await fetch("http://localhost:8000/user-role", {
          method: "GET",
          credentials: "include", // Necessário para enviar os cookies HTTP-Only
        });

        if (!response.ok) throw new Error("Não autenticado");

        const data = await response.json();
        setUserRole(data.role); // Atualiza o estado com o tipo de utilizador
        setIsAuthenticated(true); // Marca como autenticado
      } catch (error) {
        console.error("Erro ao verificar utilizador:", error);
        setIsAuthenticated(false); // Marca como não autenticado
      }
    };

    checkUserRole();
  }, []);

  return (
    <Router>
      <Routes>
        {/* Página de registo */}
        <Route path="/register" element={<Register />} />

        {/* Página de login */}
        <Route path="/login" element={isAuthenticated ? <Navigate to="/menu" /> : <Login />} />

        {/* Página do menu principal */}
        <Route path="/menu" element={isAuthenticated ? <Menu userRole={userRole} /> : <Navigate to="/login" />} />

        

		    {/* Redireciona para o login se a rota não for encontrada */}
        <Route path="*" element={<Navigate to="/login" />} />

      </Routes>
    </Router>
  );
}

export default App;
