import Navbar from "../components/Navbar.jsx";
import { MainImg } from "../components/Images.jsx";
import "../styles/Home.css";

function Home() {
  return (
    <div className="home-container">
      <header>
        <Navbar />
      </header>
      <main>
        <MainImg 
        path="/img/main.jpg" 
        alt="Prédios" 
        titulo="Juntos, cuidamos melhor do nosso espaço — peça, compartilhe e colabore para uma convivência mais harmoniosa." 
        frase="Este é o lema de uma plataforma digital que promove a colaboração entre moradores de um mesmo edifício ou comunidade. Através de funcionalidades acessíveis, os usuários podem fazer pedidos, compartilhar recursos e manter uma comunicação eficiente, contribuindo para um ambiente mais organizado e agradável para todos." />
      </main>
    </div>
  );
}

export default Home;
