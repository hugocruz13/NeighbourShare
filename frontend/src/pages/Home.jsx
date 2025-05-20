import Navbar from "../components/Navbar.jsx";
import { MainImg } from "../components/Images.jsx";
import "../styles/Home.css";

function Home() {
  return (
    <div className="home-container">
      <Navbar />
      <main className="main">
        <header className="home-hero">
          <h1>Bem-vindo ao NeighbourShare</h1>
          <p>Partilha de recursos entre vizinhos de forma simples, justa e eficiente.</p>
        </header>
        <MainImg
          path="/img/main.jpg"
          alt="Prédios"
          titulo="Juntos, cuidamos melhor do nosso espaço — peça, compartilhe e colabore para uma convivência mais harmoniosa."
          frase="Este é o lema de uma plataforma digital que promove a colaboração entre moradores de um mesmo edifício ou comunidade. Através de funcionalidades acessíveis, os usuários podem fazer pedidos, compartilhar recursos e manter uma comunicação eficiente, contribuindo para um ambiente mais organizado e agradável para todos."
        />
      </main>
      <footer className="home-footer">
          <p>&copy; {new Date().getFullYear()} DEVESI | Todos os direitos reservados.</p>
        </footer>
    </div>
  );
}

export default Home;
