/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 3:18:53 PM</date>
*	<description>Ficheiro onde consta a classe relativa a uma votação</description>
**/
using System;

namespace ObjetosNegocio
{
    /// <summary>
    /// Purpose: Classe que representa uma Votação
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 3:18:53 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class Votacao
    {
        #region Attributes

        int votacaoID;
        string titulo;
        string desc;
        DateTime dataInicio;
        DateTime dataFim;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Votacao()
        {
            votacaoID = 0;
            titulo = string.Empty;
            desc = string.Empty;
            dataInicio = DateTime.Now;
            dataFim = DateTime.Now;

        }

#endregion

#region Properties

        /// <summary>
        /// Propriedade do atributo votacaoID
        /// </summary>
        public int VotacaoID { get => votacaoID; }

        /// <summary>
        /// Propriedade do atributo titulo
        /// </summary>
        public string Titulo { get => titulo; set => titulo = value; }

        /// <summary>
        /// Propriedade do atributo desc
        /// </summary>
        public string Desc { get => desc; set => desc = value; }

        /// <summary>
        /// Propriedade do atributo dataInicio
        /// </summary>
        public DateTime DataInicio { get => dataInicio; set => dataInicio = value; }

        /// <summary>
        /// Propriedade do atributo dataFim
        /// </summary>
        public DateTime DataFim { get => dataFim; set => dataFim = value; }

#endregion



#region Overrides
#endregion

#region OtherMethods
#endregion

#region Destructor
/// <summary>
/// The destructor.
/// </summary>
~Votacao()
        {
        }
        #endregion

        #endregion
    }
}
