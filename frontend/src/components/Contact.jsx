import "../styles/Contactos.css";

function Contactos() {
  return (
    <div className="contactos-container" id="contactos">
      <h1 className="titulo">Contacte-nos</h1>
      <p>Tem dúvidas, sugestões ou precisa de ajuda? Fale connosco!</p>

      <div className="contact-info">
        <p><strong>Email:</strong> suporte@neighbourshare.com</p>
        <p><strong>Telefone:</strong> +351 912 345 678</p>
        <p><strong>Morada:</strong> Rua da Colaboração, nº 123, Lisboa</p>
      </div>

      <div className="social-media">
        <a href="https://facebook.com/neighbourshare" target="_blank" rel="noreferrer">Facebook</a>
        <a href="https://instagram.com/neighbourshare.pt" target="_blank" rel="noreferrer">Instagram</a>
        <a href="https://linkedin.com/company/neighbourshare" target="_blank" rel="noreferrer">LinkedIn</a>
      </div>
    </div>
  );
}

export default Contactos;
