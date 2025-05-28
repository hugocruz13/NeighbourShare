import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext.jsx";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Registar from "./pages/Registar.jsx";
import Menu from "./pages/Menu.jsx"
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import RecursosDisponiveis from "./pages/RecursosDisponiveis.jsx";
import PedidosNovosRecursos from "./pages/PedidosNovosRecursos.jsx";
import PedidosReserva from "./pages/PedidosReserva.jsx";
import Perfil from "./pages/Perfil.jsx";
import MeusRecursos from "./pages/MeusRecursos.jsx";
import ListaPedidosReserva from "./pages/ListaPedidosReserva.jsx";
import ListaReserva from "./pages/ListaReservas.jsx";
import RealizarPedidoNovoRecurso from "./pages/RealizarPedidoNovoRecurso.jsx";
import RealizarPedidoManutencao from "./pages/RealizarPedidoManutencao.jsx";
import PedidosManutencao from "./pages/PedidosManutencao.jsx";
import Notificacoes from "./pages/Notificacoes.jsx";
import Orcamentos from "./pages/Orcamentos.jsx";
import Manutencao from "./pages/Manutencao.jsx";
import Votacoes from "./pages/Votacoes.jsx";
import RecuperarPass from "./pages/RecuperarPass.jsx";
import EntidadeExterna from "./pages/EntidadeExterna.jsx";
import RecursosComuns from "./pages/RecursosComuns.jsx";
import "./App.css";

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="/registar" element={<ProtectedRoute allowedRoles={["admin"]}><Registar /></ProtectedRoute>}/>
            <Route path="/menu" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><Menu /></ProtectedRoute>}/>
            <Route path="/recursosDisponiveis" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><RecursosDisponiveis /></ProtectedRoute>}/>
            <Route path="/pedidosNovosRecursos" element={<ProtectedRoute allowedRoles={["gestor", "admin"]}><PedidosNovosRecursos /></ProtectedRoute>}/>
            <Route path="/pedidosReserva/:id" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><PedidosReserva /></ProtectedRoute>}/>
            <Route path="/perfil" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><Perfil /></ProtectedRoute>}/>
            <Route path="/meusRecursos" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><MeusRecursos /></ProtectedRoute>}/>
            <Route path="/listaPedidosReserva" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><ListaPedidosReserva /></ProtectedRoute>}/>
            <Route path="/listaReserva" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><ListaReserva /></ProtectedRoute>}/>
            <Route path="/realizarPedidoNovoRecurso" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><RealizarPedidoNovoRecurso /></ProtectedRoute>}/>
            <Route path="/realizarPedidoManutencao" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><RealizarPedidoManutencao /></ProtectedRoute>}/>
            <Route path="/pedidosManutencao" element={<ProtectedRoute allowedRoles={["gestor", "admin"]}><PedidosManutencao /></ProtectedRoute>}/>
            <Route path="/notificacoes" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><Notificacoes /></ProtectedRoute>}/>
            <Route path="/orcamentos" element={<ProtectedRoute allowedRoles={["gestor", "admin"]}><Orcamentos /></ProtectedRoute>}/>
            <Route path="/manutencao" element={<ProtectedRoute allowedRoles={["gestor", "admin"]}><Manutencao /></ProtectedRoute>}/>
            <Route path="/votacoes" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><Votacoes /></ProtectedRoute>}/>
            <Route path="/recuperarPass" element={<RecuperarPass  />}/>
            <Route path="/entidadeExterna" element={<ProtectedRoute allowedRoles={["residente","gestor", "admin"]}><EntidadeExterna /></ProtectedRoute>}/>
            <Route path="/recursosComuns" element={<ProtectedRoute allowedRoles={["gestor", "admin"]}><RecursosComuns /></ProtectedRoute>}/>
          </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;