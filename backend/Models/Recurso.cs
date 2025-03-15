/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/13/2025 3:13:18 PM</date>
*	<description>Ficheiro onde consta a classe relativa a um Recurso</description>
**/
using System;

namespace ObjetosNegocio
{
    /// <summary>
    /// Purpose: Classe que representa um Recurso
    /// Created by: Gustavo Marques (a27962@alunos.ipca.pt)
    /// Created on: 3/13/2025 3:13:18 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class Recurso
    {
        #region Attributes
        int id;
        string descricao;
        decimal caucao;
        byte[] imagem;
        int utilizadorId;
        int categoriaId;
        #endregion

        #region Methods

        #region Constructors
        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Recurso()
        {
            id = 0;
            descricao = string.Empty;
            caucao = 0;
            imagem = new byte[0];
            utilizadorId = 0;
            categoriaId = 0;
        }
        #endregion

        #region Properties
        /// <summary>
        /// Propriedade do atributo id
        /// </summary>
        public int Id { get => id; }

        /// <summary>
        /// Propriedade do atributo descricao
        /// </summary>
        public string Descricao { get => descricao; set => descricao = value; }

        /// <summary>
        /// Propriedade do atributo caucao
        /// </summary>
        public decimal Caucao { get => caucao; set => caucao = value; }

        /// <summary>
        /// Propriedade do atributo imagem
        /// </summary>
        public byte[] Imagem { get => imagem; set => imagem = value; }

        /// <summary>
        /// Propriedade do atributo utilizadorId
        /// </summary>
        public int UtilizadorId { get => utilizadorId; set => utilizadorId = value; }

        /// <summary>
        /// Propriedade do atributo categoriaId
        /// </summary>
        public int CategoriaId { get => categoriaId; set => categoriaId = value; }

        #endregion
        #region Overrides
        #endregion

        #region OtherMethods
        #endregion

        #region Destructor
        /// <summary>
        /// The destructor.
        /// </summary>
        ~Recurso()
        {
        }
        #endregion

        #endregion
    }
}
