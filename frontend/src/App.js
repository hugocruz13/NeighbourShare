import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home.js";
import Login from "./pages/Login.js";
import Admin from "./pages/Admin.js"
import Menu from "./pages/Menu.js"
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext.js";
import "./App.css";

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
          </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
