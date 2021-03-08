SELECT Cinemas.name, Cinemas.city
FROM Cinemas JOIN Frequents ON (Cinemas.name = Frequents.cinema)
where Frequents.spectator = 'Phil' ;