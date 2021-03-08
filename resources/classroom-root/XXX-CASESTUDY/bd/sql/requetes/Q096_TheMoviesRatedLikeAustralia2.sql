SELECT DISTINCT O1.movie
FROM Opinions O1 JOIN Opinions O2 ON (O1.stars = O2.stars)
WHERE O1.stars = O2.stars
      AND O2.spectator = 'Marie'
      AND O2.movie = 'Australia' ;