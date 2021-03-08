SELECT spectator
FROM Opinions
WHERE movie='Australia' AND stars=5

UNION

SELECT spectator
FROM Frequents
WHERE cinema='Hoyts';

