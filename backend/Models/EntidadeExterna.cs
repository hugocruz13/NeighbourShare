/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 4:20:20 PM</date>
*	<description>Ficheiro onde consta a classe relativa a uma entidade externa</description>
**/
using System;
using System.Security.Cryptography;

namespace Models
{
    /// <summary>
    /// Purpose: Classe que representa uma entidade externa
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 4:20:20 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class EntidadeExterna
    {
        #region Attributes

        int id;
        string nome;
        string especialidade;
        int contacto;
        string email;


        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor padrão
        /// </summary>
        public EntidadeExterna()
        {
            id = 0;
            nome = string.Empty;
            especialidade = string.Empty;
            contacto = 0;
            email = string.Empty;
        }

        #endregion

        #region Properties
        /// <summary>
        /// Propriedade do atributo id
        /// </summary>
        public int Id { get => id; }

        /// <summary>
        /// Propriedade do atributo nome
        /// </summary>
        public string Nome { get => nome; set => nome = value; }

        /// <summary>
        /// Propriedade do atributo especialidade
        /// </summary>
        public string Especialidade { get => especialidade; set => especialidade = value; }

        /// <summary>
        /// Propriedade do atributo contacto
        /// </summary>
        public int Contacto { get => contacto; set => contacto = value; }

        /// <summary>
        /// Propriedade do atributo email
        /// </summary>
        public string Email { get => email; set => email = value; }
        #endregion



        #region Overrides
        #endregion

        #region OtherMethods
        #endregion

        #region Destructor
        /// <summary>
        /// The destructor.
        /// </summary>
        ~EntidadeExterna()
        {
        }
        #endregion

        #endregion
    }
}
