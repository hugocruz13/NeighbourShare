  import { motion, AnimatePresence } from 'framer-motion';
  import React from 'react';
  import styles from './ModalForm.module.css';
  import Input from '../components/Input.jsx';
  import Select from '../components/Select.jsx';  // Select custom
  import Button from './Button.jsx';
  import ModalForm from '../components/ModalForm.jsx';

  const Modal = ({ show, onclose, title, fields = [], formData, onChange, onSubmit, textBotao }) => {
    return (
      <AnimatePresence>
        {show && (
          <>
            <div className={styles.modalbackdrop} onClick={onclose} />

            <motion.div
              className={styles.modalcontent}
              initial={{ opacity: 0, scale: 0.8, rotateY: 15, x: '-50%', y: '-50%' }}
              animate={{ opacity: 1, scale: 1, rotateY: 0, x: '-50%', y: '-50%' }}
              exit={{ opacity: 0, scale: 0.8, rotateY: 15, x: '-50%', y: '-50%' }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
              onClick={(e) => e.stopPropagation()} // impede fechar clicando dentro do modal
            >
              {title && <h3 className={styles.titulo}>{title}</h3>}
              <form onSubmit={onSubmit}>
                {fields.map((field) => (
                  <div key={field.name} className={styles.inputContainer}>
                    <label htmlFor={field.name} className={styles.label}>
                      {field.label}
                    </label>

                    {field.type === 'select' ? (
                      <Select
                        name={field.name}
                        value={
                          field.options.find(option => option.value === formData[field.name]) || null
                        }
                        onChange={(selectedOption, actionMeta) => onChange(selectedOption, actionMeta)}
                        options={field.options || []}
                        placeholder={field.placeholder || 'Selecione uma opção'}
                        variant={field.variant || 'default'}
                        className={styles.select}
                        required={field.required}
                        {...field.props}
                      />                      ) : field.type === 'image' ? (
                      <Input
                        id={field.name}
                        name={field.name}
                        type="file"
                        onChange={onChange}
                        accept="image/*"
                        required={field.required}
                        variant="modal"
                      />
                    ) : field.type === 'file' ? (
                      <Input
                        id={field.name}
                        name={field.name}
                        type="file"
                        onChange={onChange}
                        accept="application/pdf"
                        variant="modal"
                      />
                    ) : (
                      <Input
                        id={field.name}
                        name={field.name}
                        value={formData[field.name]}
                        onChange={onChange}
                        required={field.required}
                        placeholder={field.placeholder || 'Digite aqui...'}
                        type={field.type}
                        className={styles.inputContainer}
                        variant="modal"
                      />
                    )}
                  </div>
                ))}

                <div>
                  <Button type="submit">{textBotao}</Button>
                </div>
              </form>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    );
  };

  export default Modal;
