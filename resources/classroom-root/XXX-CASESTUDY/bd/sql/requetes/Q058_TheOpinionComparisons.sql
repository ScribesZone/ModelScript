SELECT O1.movie,
    O1.spectator AS spectator1, O1.stars AS stars1,
    O2.spectator AS spectator2, O2.stars AS stars2
FROM Opinions O1 JOIN Opinions O2
     ON (O1.movie=O2.movie and O1.spectator<>O2.spectator) ;

