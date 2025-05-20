import "../styles/Images.css";

function MainImg({ path, alt, titulo, frase }) {
  return (
    <div className="container-main">
      <div className="left">
        <h1 className="text">{titulo}</h1>
        <p className="frase">{frase}</p>
        <button className="cta-button">Começar agora</button>
      </div>
      <div className="right">
        <img className="img" src={path} alt={alt} />
      </div>
    </div>
  );
}

export { MainImg };
