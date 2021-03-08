SELECT DISTINCT movie FROM Opinions
WHERE stars = ( SELECT stars from Opinions
                WHERE spectator = 'Marie' and movie = 'Australia') ;