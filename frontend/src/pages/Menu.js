import { useAuth } from "../context/AuthContext";

function Residente() {
    const { user } = useAuth();

    return (
        <div>
          <h1>Menu após Login</h1>
    
          {user?.role === "gestor" || user?.role === "admin" && (
            <h2>Mensagem só para gestor ou admin</h2>
          )}
        </div>
      );
  }
  
  export default Residente;
  