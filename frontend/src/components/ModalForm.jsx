import {motion,AnimatePresence} from 'framer-motion';
import React, {useState,useEffect} from 'react';
import styles from './ModalForm.module.css';
import Input from '../components/Input.jsx';

const Modal = ({show, onclose, title, fields = [], formData, onChange, onSubmit, textBotao}) => {  
    return(
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
                    onClick={(e) => e.stopPropagation()} // para o clique dentro do modal não fechar
                >
                {title && <h3 className={styles.titulo}>{title}</h3>}
                <form onSubmit={onSubmit}>
                    {fields.map((field) => (
                    <div key={field.name} className={styles.inputContainer}>
                        <label htmlFor={field.name} className={styles.label}>
                        {field.label}
                        </label>
                        <Input id={field.name} name={field.name} value={formData[field.name]} onChange={onChange} required={field.required} placeholder="Digite aqui..." type={field.type} className={styles.inputContainer} variant="modal"/>
                       
                    </div>
                    ))}

                    <div>
                        <button type="submit">{textBotao}</button>
                    </div>
                </form>
                </motion.div>
            </>
            )}
        </AnimatePresence>
    );
};

export default Modal;