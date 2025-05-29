import React, { useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getFilteredRowModel,
  getSortedRowModel
} from '@tanstack/react-table';
import {motion, AnimatePresence} from 'framer-motion';
import styles from './Tabela.module.css';
import Input from './Input.jsx';

const Tabela = ({ titulo,colunas, dados, destaqueId, botoesOpcoes = [] }) => {
  const [ordenacao, setOrdenacao] = useState([]);
  const [filtroGlobal, setFiltroGlobal] = useState('');
  const tabela = useReactTable({
        data: dados,
        columns: colunas,
        getCoreRowModel: getCoreRowModel(),
        onGlobalFilterChange: setFiltroGlobal,
        getFilteredRowModel: getFilteredRowModel(),
        globalFilterFn: 'includesString',
        onSortingChange: setOrdenacao,
        state: {
          globalFilter: filtroGlobal,
          sorting: ordenacao,
        },
        getSortedRowModel: getSortedRowModel(),
  });

  return (
    <>
    <div className={styles.fundo}>
      <p className={styles.titulo}>{titulo}</p>
        <div className={styles.containerOpcoes}>
          <div className={styles.leftGroup}>
            <label htmlFor="globalFilter">Procure: </label>
            <Input
              id="globalFilter"
              type="text"
              placeholder="Filtre por qualquer coluna"
              value={filtroGlobal}
              onChange={e => setFiltroGlobal(e.target.value)}
              className={styles.inputPesquisa}
            />
          </div>
           <div className={styles.rightGroup}>
              {botoesOpcoes.map((botao, idx) => (
                <React.Fragment key={idx}>{botao}</React.Fragment>
              ))}
            </div>
        </div>
    <div className={styles.tabelaWrapper} >
    <table className={styles.tabela}>
      <thead className={styles.cabecalho}>
        {tabela.getHeaderGroups().map(headerGroup => (
          <tr key ={headerGroup.id} >
            {headerGroup.headers.map(header => (
              <th key={header.id} onClick={header.column.getToggleSortingHandler()}>
                {flexRender(header.column.columnDef.header, header.getContext())}
                  {{
                    asc: ' 🔼',
                    desc: ' 🔽',
                  }[header.column.getIsSorted()] ?? null}
              </th>
            ))} 
            </tr>
        ))}
      </thead>
      <tbody className={styles.corpo}>
      {tabela.getRowModel().rows.length === 0 ? (
        <tr>
          <td colSpan={colunas.length}>Sem resultados.</td>
        </tr>
        ) : (
        <AnimatePresence>
          {tabela.getRowModel().rows.map(row => (
            <motion.tr
              key={row.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2, ease: "easeOut" }}
              className={
                row.original.EntidadeID === destaqueId ? styles.highlightedRow : ''
              }
            >
              {row.getVisibleCells().map(cell => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </motion.tr>
          ))}
        </AnimatePresence>
        )}
      </tbody>
    </table>
    </div>
    </div>
    </>
  );
};

export default Tabela;