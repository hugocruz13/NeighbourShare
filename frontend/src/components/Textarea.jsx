import React from 'react';
import styles from './Textarea.module.css';

/**
 * Textarea Component
 * 
 * Props:
 * - value: texto controlado do textarea
 * - onChange: função para atualizar o valor
 * - placeholder: texto placeholder
 * - rows: número de linhas visíveis
 * - className: classes CSS adicionais
 * - variant: estilo visual ("default", "error", etc.)
 * - ...props: outras props HTML válidas
 */
const Textarea = ({
  value,
  onChange,
  placeholder = '',
  rows = 4,
  className = '',
  variant = 'default',
  ...props
}) => {
  const variantClasses = {
    default: styles.textarea,
    error: styles.textareaError,
    desc: styles.textareaDescricao,
  };

  const baseClass = variantClasses[variant] || variantClasses.default;

  return (
    <textarea
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      rows={rows}
      className={`${baseClass} ${className}`}
      {...props}
    />
  );
};

export default Textarea;
