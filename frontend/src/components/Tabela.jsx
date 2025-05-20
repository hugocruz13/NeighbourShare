import React,{useState, useEffect} from "react";
import styles from './Tabela.module.css';

// Função para obter valores aninhados com segurança
const getNestedValue = (obj, path) => {
    return path.split('.').reduce((acc, part) => acc && acc[part], obj);
  };

const Tabela = ({ colunas, dados, aoClicarAcao, tipoAcao, mensagemVazio }) => {

    const [filtros, setFiltros] = useState({});
    const [ordem,setOrdem] = useState(null);
    const [dadosFiltrados, setDadosFiltrados] = useState(dados);

    const handleFiltroChange = (coluna, valor) => {
        setFiltros((prev) => ({ ...prev, [coluna]: valor }));
    };

    useEffect(() => {
      const dadosFiltrados = dados.filter((linha) =>
        colunas.every((coluna) => {
          if (!filtros[coluna] || coluna === 'Ação') return true;
          const valor = getNestedValue(linha, coluna);
          return valor?.toString().toLowerCase().includes(filtros[coluna].toLowerCase());
        })
      );
      setDadosFiltrados(dadosFiltrados);
    }, [filtros]);

    // Função para aplicar a ordenação dos dados
    const handleSort = (coluna) => {
      let novaOrdem = 'asc';
      if (ordem?.coluna === coluna && ordem.direcao === 'asc') {
        novaOrdem = 'desc';
      }
      setOrdem({ coluna, direcao: novaOrdem });

      const dadosOrdenados = [...dadosFiltrados].sort((a, b) => {
        const valorA = getNestedValue(a, coluna);
        const valorB = getNestedValue(b, coluna);

        if (valorA < valorB) return novaOrdem === 'asc' ? -1 : 1;
        if (valorA > valorB) return novaOrdem === 'asc' ? 1 : -1;
        return 0;
      });
      setDadosFiltrados(dadosOrdenados);
    };

    // Função para reiniciar a ordenação
    const resetSort = () => {
      setOrdem(null);
      setDadosFiltrados(dados);
    };


    return(
        <div className={styles.containerTabela}>
        <table className={styles.tabela}>
        <thead className={styles.cabecalho}>
          <tr>
            {colunas.map((coluna, index) => (
              <th key={index}onClick={()=>handleSort(coluna)}>
                {coluna}
                {ordem?.coluna === coluna && (ordem.direcao === 'asc' ? ' ↑' : ' ↓')}
                </th>
            ))}
          </tr>
          <tr>
            {colunas.map((coluna, index) => (
              <th key={index}>
                {coluna !== 'Ação' && (
                  <input
                    type="text"
                    placeholder={`Filtrar`}
                    value={filtros[coluna] || ''}
                    onChange={(e) => handleFiltroChange(coluna, e.target.value)}
                    className={styles.inputFiltro}
                  />
                )}
              </th>
            ))}
          </tr>
        </thead>
        {Array.isArray(dados) && dados.length > 0 ? (
            <tbody className={styles.corpo}>
                {dadosFiltrados.map((linha, index) => (
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
        </div>
    )
}

export default Tabela;