import React from "react";
import styles from './Tabela.module.css';

// Função para obter valores aninhados com segurança
const getNestedValue = (obj, path) => {
    return path.split('.').reduce((acc, part) => acc && acc[part], obj);
  };

const Tabela = ({ colunas, dados, aoClicarAcao, tipoAcao, mensagemVazio }) => {
    return(
        <table className={styles.tabela}>
            <thead className={styles.cabecalho}>
                <tr>
                    {colunas.map((coluna, index) => (
                        <th key={index}>{coluna}</th>
                    ))}
                </tr>
            </thead>
            {Array.isArray(dados) && dados.length > 0 ? (
            <tbody className={styles.corpo}>
                {dados.map((linha, index) => (
                    <tr key={index}>
                        {colunas.map((coluna, colunaIndex) => (
                            <td key={colunaIndex}>
                                {coluna !== 'Ação' ? (
                                    getNestedValue(linha, coluna) ?? ''
                                ) : tipoAcao === 'botao' ? (
                                    <button
                                    className={styles.btnConfirmacoes}
                                    onClick={() => aoClicarAcao(linha)}
                                    disabled={linha.disabled}
                                    >
                                    {linha.acaoTexto}
                                    </button>
                                ) : tipoAcao === 'link' ? (
                                    <a
                                    className={styles.linkStyle}
                                    onClick={() => aoClicarAcao(linha)}
                                    >
                                    {linha.acaoTexto}
                                    </a>
                                ) : null}
                            </td>
                        ))}
                    </tr>
                ))}
            </tbody>
            ) : (
                <tbody>
                    <tr>
                    <td colSpan={colunas.length} className={styles.semDados}>
                        {mensagemVazio || 'Nenhum dado disponível'}
                    </td>
                    </tr>
                </tbody>
            )}
        </table>
    )


}

export default Tabela;