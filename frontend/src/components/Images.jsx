import styles from "./Images.module.css";
import { Link } from "react-router-dom";

function Img_Right({ path, alt, titulo, frase }) {
  return (
    <div className={styles["container-main"]}>
      <div className={styles.left}>
        <h1 className={styles.text}>{titulo}</h1>
        <p className={styles.frase}>{frase}</p>
        <Link to="/contactos" className={styles.link}>
          <button className={styles["cta-button"]}>Fala connosco</button>
        </Link>
      </div>
      <div className={styles.right}>
        <img className={styles.img} src={path} alt={alt} />
      </div>
    </div>
  );
}

function Img_Left({ path, alt }) {
  return (
    <div className={styles["container-main"]}>
      <div className={styles.right}>
        <img className={styles.img} src={path} alt={alt} />
      </div>
      <div className={styles.left}>
        <div className={styles["sobre-container"]}>
          <section className={styles.intro}>
            <h1 className={styles.text}>Sobre a DEVESI</h1>
            <p className={styles["frase-2"]}>
              A <strong>DEVESI</strong> é uma empresa dedicada ao desenvolvimento de soluções tecnológicas que promovem a inovação social, a sustentabilidade e a eficiência comunitária.
            </p>
          </section>

          <section className={styles.projeto}>
            <h2>O Projeto: NeighbourShare</h2>
            <p className={styles["frase-2"]}>
              <strong>NeighbourShare</strong> é uma plataforma criada com o objetivo de facilitar a partilha e gestão de recursos entre vizinhos. Com esta solução, promovemos uma cultura de colaboração, reduzimos desperdícios e aumentamos a acessibilidade a equipamentos e espaços comuns.
            </p>
          </section>

          <section className={styles.objetivos}>
            <h2>Objetivos do Projeto</h2>
            <ul className={styles.ul}>
              <li>🔁 Promover o reaproveitamento de recursos dentro da comunidade.</li>
              <li>🤝 Incentivar a cooperação entre vizinhos e o espírito de entreajuda.</li>
              <li>💡 Facilitar a reserva e utilização de espaços e objetos comuns.</li>
              <li>🛠️ Agilizar pedidos de manutenção e aquisição de novos recursos.</li>
              <li>🗳️ Garantir transparência na tomada de decisões através de votações em orçamentos.</li>
            </ul>
          </section>

          <section className={styles.valores}>
            <h2>Os Nossos Valores</h2>
            <p className={styles["frase-2"]}>
              Na DEVESI, acreditamos na tecnologia como motor de mudança positiva. Valorizamos a <strong>inovação com propósito</strong>, o <strong>compromisso com a comunidade</strong> e a <strong>responsabilidade ambiental</strong>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}


export { Img_Right, Img_Left };
