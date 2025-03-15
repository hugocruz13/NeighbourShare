/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/11/2025 10:23:28 AM</date>
*	<description>Ficheiro onde consta a classe relativa a um Utilizador</description>
**/
using System;

namespace ObjetosNegocio
{
    /// <summary>
    /// Purpose: Classe que representa um Utilzador
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/11/2025 10:23:28 AM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class Utilizador
    {
        #region Attributes

        int id;
        string nome;
        DateTime dataNasc;
        int contacto;
        string email;
        string password;
        byte[] foto;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Utilizador()
        {
            id = 0;
            nome = null;
            dataNasc = DateTime.Now;
            contacto = 0;
            email = null;
            password = null;
            foto = null;
        }


        #endregion

        #region Properties

        /// <summary>
        /// Propriedade do atributo id
        /// </summary>
        public int Id { get => id;}
        /// <summary>
        /// Propriedade do atributo nome
        /// </summary>
        public string Nome { get => nome; set => nome = value; }
        /// <summary>
        /// Propriedade do atributo dataNasc
        /// </summary>
        public DateTime DataNasc { get => dataNasc; set => dataNasc = value; }
        /// <summary>
        /// Propriedade do atributo contacto
        /// </summary>
        public int Contacto { get => contacto; set => contacto = value; }
        /// <summary>
        /// Propriedade do atributo email
        /// </summary>
        public string Email { get => email; set => email = value; }
        /// <summary>
        /// Propriedade do atributo password
        /// </summary>
        public string Password { get => password; set => password = value; }
        /// <summary>
        /// Propriedade do atributo foto
        /// </summary>
        public byte[] Foto { get => foto; set => foto = value; }
        #endregion

        #region Overrides
        #endregion

        #region OtherMethods

        #endregion

        #region Destructor
        /// <summary>
        /// The destructor.
        /// </summary>
        ~Utilizador()
        {
        }
        #endregion

        #endregion
    }
}
