SELECT name AS cinema, spectator
FROM  Cinemas
    LEFT OUTER JOIN Frequents
    ON (name = cinema) ;