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

const Tabela = ({ colunas, dados }) => {
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
        <label htmlFor="globalFilter">Procure: </label>
        <input
          id="globalFilter"
          type="text"
          value={filtroGlobal}
          onChange={e => setFiltroGlobal(e.target.value)}
          placeholder="Filtre por qualquer coluna"
          className={styles.inputPesquisa}
        />
    <table className={styles.tabela}>
      <thead>
        {tabela.getHeaderGroups().map(headerGroup => (
          <tr key ={headerGroup.id} className={styles.cabecalho}>
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
    </>
  );
};

export default Tabela;