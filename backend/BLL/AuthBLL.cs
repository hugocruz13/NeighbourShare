/*
*	<copyright file="BLL.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>hugoc</author>
*   <date>3/15/2025 3:38:22 PM</date>
*	<description></description>
**/
using System;
using Microsoft.AspNetCore.Http;
using Models;
using DAL;
using Utilities;

namespace BLL
{
    /// <summary>
    /// Purpose:
    /// Created by: hugoc
    /// Created on: 3/15/2025 3:38:22 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class AuthBLL
    {
        #region Singleton 

        /// <summary>
        /// Implementação Singleton que garante que apenas uma instância desta classe seja criada e reutilizada.
        /// </summary>
        static AuthBLL instance;

        public static AuthBLL Instance
        {
            get
            {
                if (instance == null)
                {
                    instance = new AuthBLL();
                }

                return instance;
            }
        }

        /// <summary>
        /// Construtor da classe "AuthBLL".
        /// </summary>
        private AuthBLL()
        {

        }
        #endregion
        /// <summary>
        /// Coloca as string com "regras"
        /// </summary>
        /// <param name="palavra"></param>
        /// <returns></returns>
        string FormatarString(string palavra)
        {
            return palavra.Trim().ToLower();
        }

        /// <summary>
        /// Metódo para verificação de dados de um "Utilizador".
        /// </summary>
        bool VerificarDados(Utilizador utilizador)
        {
            if (utilizador.DataNasc == DateOnly.MinValue || utilizador.Contacto == 0)
            {
                return false;
            }

            return true;
        }
        /// <summary>
        /// Método assíncrono que converte um arquivo IFormFile em um array de bytes.
        /// </summary>
        public async Task<byte[]> ConvertIFormFileToByteArray(IFormFile img)
        {
            if (img == null)
            {
                throw new ArgumentNullException(nameof(img), "Image cannot be null.");
            }

            using (var memoryStream = new MemoryStream())
            {
                await img.CopyToAsync(memoryStream);
                return memoryStream.ToArray();
            }
        }

        public async Task<bool> Registar(Utilizador utilizador, byte[] img1)
        {
            try
            {
                if (VerificarDados(utilizador))
                {
                    utilizador.Nome = FormatarString(utilizador.Nome);
                    utilizador.Email = FormatarString(utilizador.Email);
                    utilizador.Role = FormatarString(utilizador.Role);
                    var hash = PasswordHasher.HashPassword(utilizador.Password);
                    utilizador.Password = hash.hash;


                    if (await AuthDAL.Instance.VerificaEmail(utilizador.Email))
                    {
                        return false;
                    }

                    //verificar se inseriu img se não colocar uma defaut ou converter 

                    byte[] img = img1;

                    return await AuthDAL.Instance.InserirUtilizador(utilizador, hash.salt, img);
                }

                return false;

            }
            catch (Exception ex)
            {
                throw new Exception("BLL: " + ex.Message);
            }
        }
    }
}
