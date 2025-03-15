using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAL
{
    internal class DatabaseService
    {
        #region Singleton
        /// <summary>
        /// Singleton instance of the Materials class.
        /// </summary>
        static DatabaseService instance;

        /// <summary>
        /// Garante que a classes apenas é instanciada uma vez
        /// </summary>
        public static DatabaseService Instance
        {
            get
            {
                if (instance == null)
                {
                    instance = new DatabaseService();
                }

                return instance;
            }
        }

        /// <summary>
        /// Defaut ClienteDAL
        /// </summary>
        protected DatabaseService()
        { }
        #endregion

        private readonly string _connectionString = "Server=localhost,1433;Database=NeighbourShare;User Id=sa;Password=DEVesi2025;TrustServerCertificate=True;";

        internal SqlConnection GetConnection()
        {
            return new SqlConnection(_connectionString);
        }
    }
}
