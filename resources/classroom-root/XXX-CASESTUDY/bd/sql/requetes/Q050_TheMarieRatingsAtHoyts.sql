SELECT IsOn.movie, stars
FROM Opinions JOIN IsOn ON (Opinions.movie=IsOn.movie)
WHERE cinema='Hoyts' AND spectator='Marie';


