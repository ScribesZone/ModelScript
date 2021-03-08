SELECT spectator, city, COUNT(cinema) AS nb
FROM Frequents JOIN Spectators ON (spectator=name)
GROUP BY spectator, city ;