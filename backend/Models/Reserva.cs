/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 3:06:51 PM</date>
*	<description>Ficheiro onde consta a classe relativa a uma Reserva</description>
**/
using System;

namespace Models
{
    /// <summary>
    /// Purpose: Classe que representa uma Reserva
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 3:06:51 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class Reserva
    {
        #region Attributes

        int id;
        int pedidoReservaId;
        bool confirmarCaucaoDono;
        bool confirmarCaucaoUtilizador;
        bool recursoEntregueNovo;
        bool recursoEntregueVelho;
        bool devolucaoCaucao;
        int estadoRecursoId;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Reserva()
        {
            id = 0;
            pedidoReservaId = 0;
            confirmarCaucaoDono = false;
            confirmarCaucaoUtilizador = false;
            recursoEntregueNovo = false;
            recursoEntregueVelho = false;
            devolucaoCaucao = false;
            estadoRecursoId = 0;
        }

        #endregion

        #region Properties

        /// <summary>
        /// Propriedade do atributo id
        /// </summary>
        public int Id { get => id; }

        /// <summary>
        /// Propriedade do atributo pedidoReservaId
        /// </summary>
        public int PedidoReservaId { get => pedidoReservaId; set => pedidoReservaId = value; }

        /// <summary>
        /// Propriedade do atributo confirmarCaucaoDono
        /// </summary>
        public bool ConfirmarCaucaoDono { get => confirmarCaucaoDono; set => confirmarCaucaoDono = value; }

        /// <summary>
        /// Propriedade do atributo confirmarCaucaoUtilizador
        /// </summary>
        public bool ConfirmarCaucaoUtilizador { get => confirmarCaucaoUtilizador; set => confirmarCaucaoUtilizador = value; }

        /// <summary>
        /// Propriedade do atributo recursoEntregueNovo
        /// </summary>
        public bool RecursoEntregueNovo { get => recursoEntregueNovo; set => recursoEntregueNovo = value; }

        /// <summary>
        /// Propriedade do atributo recursoEntregueVelho
        /// </summary>
        public bool RecursoEntregueVelho { get => recursoEntregueVelho; set => recursoEntregueVelho = value; }

        /// <summary>
        /// Propriedade do atributo devolucaoCaucao
        /// </summary>
        public bool DevolucaoCaucao { get => devolucaoCaucao; set => devolucaoCaucao = value; }

        /// <summary>
        /// Propriedade do atributo estadoRecursoId
        /// </summary>
        public int EstadoRecursoId { get => estadoRecursoId; set => estadoRecursoId = value; }

        #endregion



        #region Overrides
        #endregion

        #region OtherMethods
        #endregion

        #region Destructor
        /// <summary>
        /// The destructor.
        /// </summary>
        ~Reserva()
        {
        }
        #endregion

        #endregion
    }
}
