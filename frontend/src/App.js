import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home.js";
import Login from "./pages/Login.js";
import Admin from "./pages/Admin.js"
import Menu from "./pages/Menu.js"
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext.js";
import "./App.css";
import RecursosDisponiveis from "./pages/RecursosDisponiveis.js";
import PedidosNovosRecursos from "./pages/PedidosNovosRecursos.js";
import PedidosReserva from "./pages/PedidosReserva.js";
import Perfil from "./pages/Perfil.js";
import MeusRecursos from "./pages/MeusRecursos.js";
import ListaPedidosReserva from "./pages/ListaPedidosReserva.js";
import ListaReserva from "./pages/ListaReservas.js";

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="/admin" element={<ProtectedRoute allowedRoles={["admin"]}><Admin /></ProtectedRoute>}/>
            <Route path="/menu" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><Menu /></ProtectedRoute>}/>
            <Route path="/recursosDisponiveis" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><RecursosDisponiveis /></ProtectedRoute>}/>
            <Route path="/pedidosNovosRecursos" element={<ProtectedRoute allowedRoles={["gestor", "admin"]}><PedidosNovosRecursos /></ProtectedRoute>}/>
            <Route path="/pedidosReserva/:id" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><PedidosReserva /></ProtectedRoute>}/>
            <Route path="/perfil" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><Perfil /></ProtectedRoute>}/>
            <Route path="/meusRecursos" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><MeusRecursos /></ProtectedRoute>}/>
            <Route path="/listaPedidosReserva" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><ListaPedidosReserva /></ProtectedRoute>}/>
            <Route path="/listaReserva" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><ListaReserva /></ProtectedRoute>}/>
          </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
