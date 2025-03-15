/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 4:31:11 PM</date>
*	<description>Ficheiro onde consta a classe relativa a uma notificação</description>
**/
using System;
using System.Security.Cryptography;

namespace Models
{
    /// <summary>
    /// Purpose: Classe que representa uma notificação
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 4:31:11 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class Notificacao
    {
        #region Attributes

        int id;
        string mensagem;
        DateTime dataHora;
        int processoId;
        bool estado; //Lida ou não lida
        int tipoProcessoID;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Notificacao()
        {
            id = 0;
            mensagem = string.Empty;
            dataHora = DateTime.Now;
            processoId = 0;
            estado = false;
            tipoProcessoID = 0;
        }

        #endregion

        #region Properties

        /// <summary>
        /// Propriedade do atributo id
        /// </summary>
        public int Id { get => id; }

        /// <summary>
        /// Propriedade do atributo mensagem
        /// </summary>
        public string Mensagem { get => mensagem; set => mensagem = value; }

        /// <summary>
        /// Propriedade do atributo dataHora
        /// </summary>
        public DateTime DataHora { get => dataHora; set => dataHora = value; }

        /// <summary>
        /// Propriedade do atributo processoId
        /// </summary>
        public int ProcessoId { get => processoId; set => processoId = value; }

        /// <summary>
        /// Propriedade do atributo estado
        /// </summary>
        public bool Estado { get => estado; set => estado = value; }

        /// <summary>
        /// Propriedade do atributo tipoProcessoID
        /// </summary>
        public int TipoProcessoID { get => tipoProcessoID; set => tipoProcessoID = value; }
        #endregion



        #region Overrides
        #endregion

        #region OtherMethods
        #endregion

        #region Destructor
        /// <summary>
        /// The destructor.
        /// </summary>
        ~Notificacao()
        {
        }
        #endregion

        #endregion
    }
}
