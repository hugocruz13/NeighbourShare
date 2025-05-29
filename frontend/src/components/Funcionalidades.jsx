import styles from "./Funcionalidades.module.css";

function Funcionalidades({ titulo, desc }) {
  return (
    <div className={styles["func-card"]}>
      <h2>{titulo}</h2>
      <p>{desc}</p>
    </div>
  );
}

export default Funcionalidades;


