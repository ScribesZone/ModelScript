SELECT title, releaseYear
FROM Movies JOIN
    (   SELECT movie
        FROM Opinions
        WHERE stars=5

        EXCEPT

        SELECT movie
        FROM IsOn
        WHERE cinema='Hoyts') AS R
    ON (movie=title) ;

