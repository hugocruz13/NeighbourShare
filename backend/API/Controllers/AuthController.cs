using BLL;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using Models;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        /// <summary>
        /// Controllador que regista um utilizador no sistema
        /// </summary>
        /// <param name="utilizador">Utilizador a registar</param>
        [HttpPost("registar")]
        public async Task<IActionResult> Registar([FromForm] Utilizador utilizador)
        {
            try
            {
                //BUG -> TEM QUE SER FEITA NO BLL
                byte[] img = await AuthBLL.Instance.ConvertIFormFileToByteArray(utilizador.Foto);

                if (await AuthBLL.Instance.Registar(utilizador,img))
                {
                    return Ok("Registado");
                }

                return NotFound();
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Internal Server Error: " + ex.Message);
            }
        }

    }
}
