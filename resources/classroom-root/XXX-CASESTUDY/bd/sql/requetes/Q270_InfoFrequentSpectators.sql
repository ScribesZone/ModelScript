SELECT  spectator,
        MAX(stars) AS maxRating,
        COUNT(DISTINCT cinema) AS nb
FROM Opinions NATURAL JOIN Frequents
GROUP BY spectator
HAVING COUNT(DISTINCT movie)>2 ;