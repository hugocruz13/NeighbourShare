/*
*	<copyright file="ObjetosNegocio.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Gustavo Marques/author>
*   <date>3/11/2025 10:23:28 AM</date>
*	<description>Ficheiro onde consta a classe relativa a um Utilizador</description>
**/
using Microsoft.AspNetCore.Http;
using System;
using System.ComponentModel.DataAnnotations;

namespace Models
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
        DateOnly dataNasc;
        int contacto;
        string email;
        string password;
        IFormFile foto;
        string role;

        #endregion

        #region Methods

        #region Constructors

        /// <summary>
        /// Construtor Padrão
        /// </summary>
        public Utilizador()
        {
            //id = 0;
            nome = null;
            dataNasc = DateOnly.MinValue;
            contacto = 0;
            email = null;
            password = null;
            foto = null;
            role = null;
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
        [Required(ErrorMessage = "O nome é obrigatório.")]
        public string Nome { get => nome; set => nome = value; }
        /// <summary>
        /// Propriedade do atributo dataNasc
        /// </summary>
        public DateOnly DataNasc { get => dataNasc; set => dataNasc = value; }
        /// <summary>
        /// Propriedade do atributo contacto
        /// </summary>
        public int Contacto { get => contacto; set => contacto = value; }
        /// <summary>
        /// Propriedade do atributo email
        /// </summary>
        [EmailAddress(ErrorMessage = "O e-mail fornecido não é válido.")]
        [Required(ErrorMessage = "O e-mail é obrigatório.")]
        public string Email { get => email; set => email = value; }
        /// <summary>
        /// Propriedade do atributo password
        /// </summary>
        [Required(ErrorMessage = "A password é obrigatória.")]
        public string Password { get => password; set => password = value; }
        /// <summary>
        /// Propriedade do atributo foto
        /// </summary>
        public IFormFile Foto { get => foto; set => foto = value; }
        /// <summary>
        /// Propriedade do atributo Cargo
        /// </summary>
        [Required(ErrorMessage = "O cargo é obrigatório.")]
        public string Role { get => role; set => role = value; }
        #endregion

        #region Overrides
        #endregion

        #region OtherMethods

        #endregion

        #region Destructor
        /// <summary>
        /// O destrutor.
        /// </summary>
        ~Utilizador()
        {
        }
        #endregion

        #endregion
    }
}
