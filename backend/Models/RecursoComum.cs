/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 4:28:52 PM</date>
*	<description>Ficheiro onde consta a classe relativa a um recurso comum</description>
**/
using System;

namespace Models
{
    /// <summary>
    /// Purpose: Classe que representa um recurso comum
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 4:28:52 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class RecursoComum
    {
        #region Attributes

        int id;
        string nome;
        string desc;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor padrão
        /// </summary>
        public RecursoComum()
        {
            id = 0;
            nome = string.Empty;
            desc = string.Empty;
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
        /// Propriedade do atributo desc
        /// </summary>
        public string Desc { get => desc; set => desc = value; }

        #endregion



        #region Overrides
        #endregion

        #region OtherMethods
        #endregion

        #region Destructor
        /// <summary>
        /// The destructor.
        /// </summary>
        ~RecursoComum()
        {
        }
        #endregion

        #endregion
    }
}
