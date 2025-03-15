CREATE PROCEDURE VerificarExistenciaEmail
    @Email VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM Utilizador WHERE Email = @Email)
        SELECT 1 AS Resultado;
    ELSE
        SELECT 0 AS Resultado;
END;

CREATE PROCEDURE RegistarNovoUtilizador
    @Nome VARCHAR(255),
    @Data DATE,
    @Contacto VARCHAR(255),
    @Email VARCHAR(255),
    @Password VARCHAR(64),
    @Salt VARCHAR(32),
    @Foto IMAGE,
    @Role VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @RoleCode INT;

    Select @RoleCode =TUID 
    From TipoUtilizador
    Where DescTU = @Role

    INSERT INTO Utilizador (NomeUtilizador, DataNasc, Contacto, Email, PasswordHash, Salt, Foto, TUID)
    VALUES (@Nome, @Data, @Contacto, @Email, @Password, @Salt, @Foto, @RoleCode);

END;

