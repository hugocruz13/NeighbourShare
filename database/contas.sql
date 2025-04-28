USE [NeighbourShare]
GO

/*admin*/

INSERT INTO [dbo].[Utilizador]
           ([NomeUtilizador]
           ,[DataNasc]
           ,[Contacto]
           ,[Email]
           ,[PasswordHash]
           ,[Salt]
           ,[Verificado]
           ,[TUID]
           ,[Path])
     VALUES
           ('admin'
           ,'2025-04-18'
           ,123456789
           ,'admin@email.com'
           ,'TsQyUx0vE0xr29BAYX3hFWQAW+bSb2ZRTG/8fR4rUZA='
           ,'b7Cjbu8pIgohV3pkU64fUg=='
           ,1
           ,1
           ,'null')
GO

USE [NeighbourShare]
GO

INSERT INTO [dbo].[Utilizador]
           ([NomeUtilizador]
           ,[DataNasc]
           ,[Contacto]
           ,[Email]
           ,[PasswordHash]
           ,[Salt]
           ,[Verificado]
           ,[TUID]
           ,[Path])
     VALUES
           ('gestor'
           ,'2025-04-18'
           ,123456789
           ,'gestor@email.com'
           ,'ZBzzaidXUwMjNeMd/jc0LJ0GG8WhlU4IMKEEoAgh5ZI='
           ,'lMvfKy4UtMG27ayKFw7yCw=='
           ,1
           ,3
           ,'null')
GO

INSERT INTO [dbo].[Utilizador]
           ([NomeUtilizador]
           ,[DataNasc]
           ,[Contacto]
           ,[Email]
           ,[PasswordHash]
           ,[Salt]
           ,[Verificado]
           ,[TUID]
           ,[Path])
     VALUES
           ('residente'
           ,'2025-04-18'
           ,123456789
           ,'residente@email.com'
           ,'Bdu133f9Obo0yMA0vSEx7I3filBT5/qezrTvpKyM7lw='
           ,'+rNaQUKMZtnMrvYj9g1law=='
           ,1
           ,2
           ,'null')
GO