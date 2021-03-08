CREATE VIEW NbOfSpectatorsPerCinema
AS
    SELECT Cinema, COUNT(spectator) AS nbOfSpectators
    FROM Frequents
    GROUP BY Cinema ;

SELECT cinema
FROM NbOfSpectatorsPerCinema JOIN (
        SELECT MAX(nbOfSpectators) AS maxSpectators
        FROM NbOfSpectatorsPerCinema)
    ON (nbOfSpectators = maxSpectators) ;

DROP VIEW NbOfSpectatorsPerCinema ;