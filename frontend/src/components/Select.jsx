import React from "react";
import styles from "./Select.module.css"; // onde defines os estilos
import ReactSelect from "react-select";


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

  const handleChange = (selectedOption) => {
    onChange({
      target: {
        name,
        value: selectedOption ? selectedOption.value : ''
      }
    });
  };

  
  const CustomOption = (props) => {
    const { data, innerRef, innerProps } = props;

    return (
      <div
        ref={innerRef}
        {...innerProps}
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "8px"
        }}
      >
        <span>{data.label}</span>
        {data.url && (
          <button
            onClick={(e) => {
              e.stopPropagation(); // impede o select de fechar
              window.open(data.url, "_blank");
            }}
            style={{
              marginLeft: "10px",
              padding: "4px 8px",
              fontSize: "0.8rem",
              cursor: "pointer"
            }}
          >
            Ver PDF
          </button>
        )}
      </div>
    );
  };

  return (
    <ReactSelect
      name={name}
      value={value}
      onChange={handleChange}
      options={options}
      placeholder={placeholder}
      className={`${baseClass} ${className}`}
      components={{ Option: CustomOption }}
      {...props}
    />
  );
};

export default Select;
