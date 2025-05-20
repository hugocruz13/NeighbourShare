import "../styles/Functionality.css";

function Funcionalidades({ titulo, desc }) {
  return (
    <div className="func-card">
        <h2>{titulo}</h2>
        <p>{desc}</p>
    </div>
  );
}

export default Funcionalidades;


