import { ImgRight, ImgLeft } from "../components/Images.jsx";
import Navbar from "../components/Navbar.jsx";
import Funcionalidades from "../components/Funcionalidades.jsx";
import Contactos from "../components/Contactos.jsx";
import "../styles/Home.css";

function Home() {
  return (
    <div className="home-container" id="/">
      <Navbar />
      <main className="main">
        <header className="home-hero">
          <h1>Bem-vindo ao NeighbourShare</h1>
          <p>
            Partilha de recursos entre vizinhos de forma simples, justa e
            eficiente.
          </p>
        </header>
        <ImgRight
          path="/img/main.jpg"
          alt="Prédios"
          titulo="Juntos, cuidamos melhor do nosso espaço — peça, compartilhe e colabore para uma convivência mais harmoniosa."
          frase="Este é o lema de uma plataforma digital que promove a colaboração entre moradores de um mesmo edifício ou comunidade. Através de funcionalidades acessíveis, os usuários podem fazer pedidos, compartilhar recursos e manter uma comunicação eficiente, contribuindo para um ambiente mais organizado e agradável para todos."
        />
        <div id="funcionalidades" className="funcionalidades-container">
          <h1 className="titulo">Funcionalidades do Sistema</h1>
          <p className="descricao">
            Este sistema foi desenvolvido para promover a colaboração entre
            vizinhos, facilitando a gestão de recursos comuns de forma simples,
            transparente e eficiente. Conheça abaixo as principais
            funcionalidades:
          </p>
          <div className="cards-container">
            <Funcionalidades
              titulo="Reserva de Recursos"
              desc=" Permite que vizinhos reservem recursos disponíveis como
                materiais, ferramentas ou equipamentos, de forma organizada e
                com controlo."
            />
            <Funcionalidades
              titulo="Pedido de Novos Recursos"
              desc="Os residentes podem sugerir e solicitar a aquisição de novos
                recursos que considerem úteis para o prédio."
            />
            <Funcionalidades
              titulo="Manutenção de Recursos"
              desc="Os residentes podem reportar problemas e solicitar manutenção de
                recursos comuns como churrasqueiras, salas, elevadores, entre
                outros."
            />
            <Funcionalidades
              titulo="Votação em Orçamentos"
              desc="Os utilizadores podem votar nas propostas de orçamento apresentadas para aquisição ou manutenção de recursos."
            />

            <Funcionalidades
              titulo="Outras Funcionalidades"
              desc="Notificações automáticas e entre outras."
            />
          </div>
        </div>
        <br />
        <br />
        <div className="about" id="sobre">
          <ImgLeft path="logo512.png" alt="Prédios" />
        </div>
        <div id="contacto">
          <Contactos/>
        </div>
      </main>
      <footer className="home-footer">
        <p>
          &copy; {new Date().getFullYear()} DEVESI | Todos os direitos
          reservados.
        </p>
      </footer>
    </div>
  );
}

export default Home;
