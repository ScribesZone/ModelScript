SELECT title, releaseYear
FROM Movies JOIN IsOn ON (title=movie)
WHERE cinema='Hoyts';