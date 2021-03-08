SELECT name, city FROM Cinemas
WHERE name IN ( SELECT cinema
                FROM  Frequents
                WHERE spectator = 'Phil' ) ;