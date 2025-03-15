/**
*	<copyright file="PasswordHasher.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>Igor</author>
*   <date>3/15/2025 3:51:00 PM</date>
*	<description></description>
***/

using System;
using System.Security.Cryptography;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;

namespace Utilities
{
    /// <summary>
    /// Purpose: Classe com um conjunto de métodos estáticos para conversõese verficações da password e hash
    /// Created by: igor
    /// Created on: 3/15/2025 15:51:00 PM
    /// </summary>
    /// <remarks>
    ///    password: string password,
    ///    salt: Uma conjunto de 16 bytes aleatórios que servem de assinatura que só está presente na base de dados,
    ///    prf: Derivação do algoritmo, neste caso foi escolhido HMAC SHA256,
    ///    iterationCount: número de iterações que o algoritmo PBKDF2 (Password-Based Key Derivation Function 2) executa para derivar a chave,
    ///    numBytesRequested: Tamanho da chave, default: 32 bytes;
    /// </remarks>
    public class PasswordHasher
    {
        /// <summary>
        /// Cria uma hash PBKDF2 com a password 
        /// </summary>
        public static (string hash, string salt) HashPassword(string password)
        {
            // Gera um salt aleatório
            byte[] salt = new byte[16];
            using (var aleatorioEngine = RandomNumberGenerator.Create()) { 
                aleatorioEngine.GetBytes(salt);
            }

            //Hash da senha com salt, algoritmo PBKDF2
            string hashedPassword = Convert.ToBase64String(KeyDerivation.Pbkdf2(
                password: password,
                salt: salt,
                prf: KeyDerivationPrf.HMACSHA256,
                iterationCount: 100000,
                numBytesRequested: 32));

            // Converte salt para string para armazenamento
            string saltString = Convert.ToBase64String(salt);

            return (hashedPassword, saltString);
        }

        /// <summary>
        /// Verificar password comparando a password e a hash fornecida
        /// </summary>
        public static bool VerificarPassword(string password, string storedHash, string storedSalt)
        {
            // Converte o salt armazenado para bytes
            byte[] salt = Convert.FromBase64String(storedSalt);

            // Hash da password fornecida
            string hashedPassword = Convert.ToBase64String(KeyDerivation.Pbkdf2(
                password: password,
                salt: salt,
                prf: KeyDerivationPrf.HMACSHA256,
                iterationCount: 100000,
                numBytesRequested: 32));

            // Compara o hash gerado com o hash armazenado
            return hashedPassword == storedHash;
        }

    }
}
