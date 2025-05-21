import React from 'react';
import styles from './Input.module.css';

/**
 * Input Component
 * 
 * Um input reutilizável com suporte para diferentes variantes de estilo.
 *
 * Props:
 * - type: Tipo de input (text, password, email, etc.)
 * - value: Valor do input
 * - onChange: Função chamada quando o valor muda
 * - placeholder: Texto de exemplo
 * - className: Classes CSS adicionais
 * - variant: Variante visual do input ("default", "error", "success")
 * - ...props: Outros atributos HTML válidos (id, name, disabled, etc.)
 */
const Input = ({
  type = 'text',
  value,
  onChange,
  placeholder = '',
  className = '',
  variant = '',
  ...props
}) => {
  const variantClasses = {
    default: styles.input,
    error: styles['input-error'],
    success: styles['input-success'],
    modal: styles['input-modal'],
  };

  const baseClass = variantClasses[variant] || styles.input;

  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className={`${baseClass} ${className}`}
      {...props}
    />
  );
};

export default Input;
