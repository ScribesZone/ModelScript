SELECT spectator, COUNT(cinema) AS nb
FROM Frequents
GROUP BY spectator ;