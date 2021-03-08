SELECT spectator, movie
FROM Opinions
WHERE stars>=4

INTERSECT

SELECT spectator, movie
FROM IsOn NATURAL JOIN Frequents ;