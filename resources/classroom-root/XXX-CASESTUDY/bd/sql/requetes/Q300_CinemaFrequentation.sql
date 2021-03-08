SELECT cinema, spectator
FROM Frequents

UNION

SELECT name as cinema, NULL
FROM Cinemas
WHERE name NOT IN (
       SELECT cinema
       FROM Frequents) ;