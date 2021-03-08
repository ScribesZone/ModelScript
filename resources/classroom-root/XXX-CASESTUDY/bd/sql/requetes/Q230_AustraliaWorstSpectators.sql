SELECT spectator
FROM Opinions JOIN
    (   SELECT MIN(stars) AS minStars
        FROM Opinions
        WHERE movie='Australia')
    ON (stars=minStars)
WHERE movie='Australia' ;