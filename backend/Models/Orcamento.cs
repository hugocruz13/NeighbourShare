/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 3:54:33 PM</date>
*	<description>Ficheiro onde consta a classe relativa a um orçamento</description>
**/
using Microsoft.SqlServer.Server;
using System;
using System.Runtime.InteropServices.ComTypes;

namespace ObjetosNegocio
{
    /// <summary>
    /// Purpose: Classe que representa um orçamento
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 3:54:33 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class Orcamento
    {
        #region Attributes

        int orcamentoID;
        string nomeFornecedor;
        double valor;
        string desc;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Orcamento()
        {

            orcamentoID = 0;
            nomeFornecedor = string.Empty;
            valor = 0;
            desc = string.Empty;

        }

        #endregion

        #region Properties

        /// <summary>
        /// Propriedade do atributo orcamentoID
        /// </summary>
        public int OrcamentoID { get => orcamentoID; }

        /// <summary>
        /// Propriedade do atributo nomeFornecedor
        /// </summary>
        public string NomeFornecedor { get => nomeFornecedor; set => nomeFornecedor = value; }

        /// <summary>
        /// Propriedade do atributo valor
        /// </summary>
        public double Valor { get => valor; set => valor = value; }

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
        ~Orcamento()
        {
        }
        #endregion

        #endregion
    }
}
