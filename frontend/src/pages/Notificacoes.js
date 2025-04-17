import React, { useState, useEffect } from "react";
import "../styles/Notificacoes.css";
import Navbar2 from "../components/Navbar2.js";

function Notificacoes() {
  const [notificacoes, setNotificacoes] = useState([]);
  const [selecionada, setSelecionada] = useState(null);

  useEffect(() => {
    const fetchNotificacoes = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/notificacoes/', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await res.json();
        console.log(data);
        setNotificacoes(data);
      } catch (error) {
        console.error('Erro ao buscar notificações:', error);
      }
    };

    fetchNotificacoes();
  }, []);

  const marcarComoLida = async (NotificacaoID) => {
    try {
      const res = await fetch(`http://localhost:8000/api/notificacoes/${NotificacaoID}/lida`, {
        method: 'PUT',
        credentials: 'include'
      });
      if (!res.ok) {
        throw new Error('Erro ao marcar notificação como lida');
      }
      // Atualiza o estado para refletir que a notificação foi lida
      setNotificacoes((prevNotificacoes) =>
        prevNotificacoes.map((noti) =>
          noti.NotificacaoID === NotificacaoID ? { ...noti, lida: true } : noti
        )
      );
    } catch (error) {
      console.error('Erro ao marcar notificação como lida:', error);
    }
  };

  const handleNotificacaoClick = (noti) => {
    setSelecionada(noti);
    if (!noti.lida) {
      marcarComoLida(noti.NotificacaoID);
    }
  };

  return (
    <div className="page-content">
      <Navbar2 />
      <div className="notificacoes-container">
        <div className="notificacoes-lista">
          {notificacoes.map((noti) => (
            <div
              key={noti.NotificacaoID}
              className={`notificacao-preview ${
                selecionada && selecionada.NotificacaoID === noti.NotificacaoID ? "ativa" : ""
              }`}
              onClick={() => handleNotificacaoClick(noti)}
            >
              <h4>{noti.Titulo}</h4>
              <p>{noti.Mensagem.substring(0, 100)}...</p>
              <span className="data">{noti.data}</span>
            </div>
          ))}
        </div>
        <div className="notificacao-detalhe">
          {selecionada && (
            <>
              <h2>{selecionada.Titulo}</h2>
              <span className="data">{selecionada.DataHora}</span>
              <p>{selecionada.Mensagem}</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Notificacoes;
