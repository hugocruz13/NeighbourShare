import "../styles/Images.css";
import { Link } from "react-router-dom";

function MainImg({ path, alt, titulo, frase }) {
  return (
    <div className="container-main">
      <div className="left">
        <h1 className="text">{titulo}</h1>
        <p className="frase">{frase}</p>
        <Link to="/contactos" className="link"><button className="cta-button">Fala connosco</button></Link>
      </div>
      <div className="right">
        <img className="img" src={path} alt={alt} />
      </div>
    </div>
  );
}

export { MainImg };
