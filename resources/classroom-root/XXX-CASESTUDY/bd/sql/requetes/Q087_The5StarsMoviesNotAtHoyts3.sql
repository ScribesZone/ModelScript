WITH
    R(movie) AS (
        SELECT movie
        FROM Opinions
        WHERE stars=5
        EXCEPT
        SELECT movie
        FROM IsOn
        WHERE cinema='Hoyts')
SELECT title, releaseYear
FROM Movies JOIN R ON (movie=title) ;
