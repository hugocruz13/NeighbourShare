import { useState } from "react";
import "../styles/Notificacoes.css";
import Navbar2 from "../components/Navbar2.js";

const notificacoesExemplo = [
  {
    id: 1,
    titulo: "Pedido de Recurso Aprovado",
    resumo: "O seu pedido para o recurso 'Projetor' foi aprovado.",
    data: "14/04/2025",
    conteudo: "O seu pedido de utilização do projetor comunitário foi aprovado. Pode utilizá-lo no dia 15/04 das 14h às 16h. Obrigado pela colaboração.",
  },
  {
    id: 2,
    titulo: "Reserva Cancelada",
    resumo: "A sua reserva da sala de reuniões foi cancelada.",
    data: "13/04/2025",
    conteudo: "Infelizmente, a sua reserva da sala de reuniões no dia 14/04 foi cancelada por motivos técnicos. Pedimos desculpa pelo incómodo.",
  },
  {
    id: 3,
    titulo: "Novo Recurso Disponível",
    resumo: "Foi adicionado um novo recurso: Barbecue.",
    data: "12/04/2025",
    conteudo: "Temos o prazer de anunciar que um novo recurso está disponível: o barbecue comunitário! Já pode reservá-lo através da plataforma.",
  },
];

function Notificacoes() {
  const [notificacoes] = useState(notificacoesExemplo);
  const [selecionada, setSelecionada] = useState(notificacoes[0]);

  return (
    <div className="page-content">
  
    <div className="notificacoes-container">
      
      <div className="notificacoes-lista">
        {notificacoes.map((noti) => (
          <div
            key={noti.id}
            className={`notificacao-preview ${
              selecionada.id === noti.id ? "ativa" : ""
            }`}
            onClick={() => setSelecionada(noti)}
          >
            <h4>{noti.titulo}</h4>
            <p>{noti.resumo}</p>
            <span className="data">{noti.data}</span>
          </div>
        ))}
      </div>
      <div className="notificacao-detalhe">
        {selecionada && (
          <>
            <h2>{selecionada.titulo}</h2>
            <span className="data">{selecionada.data}</span>
            <p>{selecionada.conteudo}</p>
          </>
        )}
      </div>
    </div>
</div>
  );
}

export default Notificacoes;
