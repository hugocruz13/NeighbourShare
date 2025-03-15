/*
*	<copyright file="DAL.cs" company="IPCA">
*		Copyright (c) 2025 All Rights Reserved
*	</copyright>
* 	<author>hugoc</author>
*   <date>3/15/2025 5:25:41 PM</date>
*	<description></description>
**/
using Microsoft.Data.SqlClient;
using System.Data;
using Models;

namespace DAL
{
    /// <summary>
    /// Purpose:
    /// Created by: hugoc
    /// Created on: 3/15/2025 5:25:41 PM
    /// </summary>
    /// <remarks></remarks>
    /// <example></example>
    public class AuthDAL
    {
        #region Singleton 

        /// <summary>
        /// Implementação Singleton que garante que apenas uma instância desta classe seja criada e reutilizada.
        /// </summary>
        static AuthDAL instance;

        public static AuthDAL Instance
        {
            get
            {
                if (instance == null)
                {
                    instance = new AuthDAL();
                }

                return instance;
            }
        }

        /// <summary>
        /// Construtor da classe "AuthBLL".
        /// </summary>
        private AuthDAL()
        {

        }
        #endregion
        /// <summary>
        /// Método assíncrono que verifica a existência de um e-mail na base de dados, executando um stored procedure para verificar.
        /// </summary>
        public async Task<bool> VerificaEmail(string email)
        {
            string procedure = "VerificarExistenciaEmail";

            try
            {
                using (SqlConnection connection = DatabaseService.Instance.GetConnection())
                {
                    using (SqlCommand command = new SqlCommand(procedure, connection))
                    {
                        command.CommandType = CommandType.StoredProcedure;
                        command.Parameters.AddWithValue("@Email", email);
                        connection.Open();

                        using (SqlDataReader reader = await command.ExecuteReaderAsync())
                        {
                            if (reader.Read())
                            {
                                int result = reader.GetInt32(0);
                                return Convert.ToBoolean(result);
                            }
                        }
                    }
                }

                return false;
            }
            catch (Exception ex)
            {
                throw new Exception("DAL" + ex.Message);
            }
        }
        /// <summary>
        /// Método assíncrono que insere um novo utilizador na base de dados executando um stored procedure para criar.
        /// </summary>
        public async Task<bool> InserirUtilizador(Utilizador utilizador,string salt, byte[] foto)
        {
            string procedure = "RegistarNovoUtilizador";

            try
            {
                using (SqlConnection connection = DatabaseService.Instance.GetConnection())
                {
                    using (SqlCommand command = new SqlCommand(procedure, connection))
                    {
                        command.CommandType = CommandType.StoredProcedure;
                        command.Parameters.AddWithValue("@Nome", utilizador.Nome);
                        command.Parameters.AddWithValue("@Data", utilizador.DataNasc);
                        command.Parameters.AddWithValue("@Contacto", utilizador.Contacto);
                        command.Parameters.AddWithValue("@Email", utilizador.Email);
                        command.Parameters.AddWithValue("@Password", utilizador.Password);
                        command.Parameters.AddWithValue("@Salt", salt);
                        command.Parameters.AddWithValue("@Foto", foto);
                        command.Parameters.AddWithValue("@Role", utilizador.Role);
                        connection.Open();
                        command.ExecuteNonQuery();
                        return true;
                            
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("DAL" + ex.Message);
            }
        }
    }
}
