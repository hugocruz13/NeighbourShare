import React from "react";
import styles from "./Select.module.css"; // onde defines os estilos

/**
 * Select Component
 * 
 * Props:
 * - name: nome do campo (usado com handleChange).
 * - value: valor selecionado.
 * - onChange: função chamada ao mudar a opção.
 * - options: array de objetos { value, label }.
 * - placeholder: opção inicial (não selecionável).
 * - variant: estilo visual ("default", "outlined", etc.).
 * - className: classes CSS adicionais.
 * - ...props: outros atributos (disabled, required, etc.).
 */
const Select = ({
  name,
  value,
  onChange,
  options = [],
  placeholder = "Selecione uma opção",
  variant = "default",
  className = "",
  ...props
}) => {
  const variantClasses = {
    default: styles.select,
    outlined: styles["select-outlined"],
    geral: styles["inputGeral"],
  };

  const baseClass = variantClasses[variant] || styles.select;

  return (
    <select
      name={name}
      value={value}
      onChange={onChange}
      className={`${baseClass} ${className}`}
      {...props}
    >
      <option value="" disabled hidden>
        {placeholder}
      </option>
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
};

export default Select;
