--=========================================================================
-- CyberCinemas
--=========================================================================
-- Based on the course of M.C. Fauvet
---------------------------------------------------------------------------


---------------------------------------------------------------------------
-- Database schema
---------------------------------------------------------------------------

--  relation Movies(_title_:s, releaseYear:i)
--      | The movies considered by the study.
--      columns
--          title : Integer
--              | The original title of the movie in the
--              | language of the country it was released.
--          releaseYear : Integer
--              | The year of release
--      constraints
--          key title

CREATE TABLE Movies(
    title VARCHAR(100),
    releaseYear INTEGER,

    CONSTRAINT PK
        PRIMARY KEY (title)
);

--  relation Cinemas(_name_, city)
--      | All the cinemas considered by the study.
--      columns
--          name : String
--              | The name of the cinema with enough details
--              | so that it is unique for all cinemas.
--          city : String
--              | The city of the cinema.*
--      constraints
--          key name

CREATE TABLE Cinemas(
    name VARCHAR(100),
    city VARCHAR(100),

    CONSTRAINT PK
        PRIMARY KEY (name)
);

--  relation Spectators( _name_:s, birthYear:i, city:s )
--      | The registered spectators with a cinema card.
--      | Other spectators are not counted as they are anonymous.
--     columns
--          name : String
--              | The name of the spectator.
--          birthYear: Integer
--              | The birth year of the spectator as declared
--              | when the card was delivered.
--          city : String
--              | The city where the spectator declared to live.
--      constraints
--          key name


CREATE TABLE Spectators(
    name VARCHAR(100),
    birthYear INTEGER,
    city VARCHAR(100),

    CONSTRAINT PK
        PRIMARY KEY (name)
);


--  relation IsOn(_movie_, _cinema_)
--      | The cinemas that display or displayed movies.
--      columns
--          movie : String
--              | The title of the movie displayed at the cinema.
--          cinema : String
--              | The name of the cinema displaying the movie.
--      constraints
--          key movie, cinema
--          IsOn[movie] C= Movies[title]
--          IsOn[cinema] C= Cinemas[name]



CREATE TABLE IsOn(
    movie VARCHAR(100),     -- => Movies.title
    cinema VARCHAR(100),    -- => Cinema.name

    CONSTRAINT PK
        PRIMARY KEY (movie, cinema)
    CONSTRAINT FK_movie
        FOREIGN KEY (movie) REFERENCES Movies(title),
    CONSTRAINT FK_cinema
        FOREIGN KEY (cinema) REFERENCES Cinemas(name)
);


--  relation Opinions(_spectator_:s, _movie_:s, stars:i)
--      | The number of stars given by a spectator on a movie.
--      columns
--          spectator : Sting
--              | The name of the spectator.
--          movie : String
--              | The name of the movie.
--          stars : Integer
--              | The number of stars between 0 and 5.
--      constraints
--          key spectator, movie
--          dom(stars) = {0,1,2,3,4,5}
--          Opinions[spectator] C= Spectators[name]
--          Opinions[movie] C= Movies[name]


CREATE TABLE Opinions(
    spectator VARCHAR(100),     -- => Spectators.name
    movie VARCHAR(100),         -- => Movies.title
    stars INTEGER,              -- BETWEEN 0 AND 5

    CONSTRAINT PK
        PRIMARY KEY (spectator, movie),
    CONSTRAINT Dom_stars
        CHECK (stars IN ('0', '1', '2', '3', '4', '5')),
    CONSTRAINT FK_spectator
        FOREIGN KEY (spectator) REFERENCES Spectators(name),
    CONSTRAINT FK_movie
        FOREIGN KEY (movie) REFERENCES Movies(title)
);

--  relation Frequents(_spectator_:s, _cinema_:s)
--      |The frequentation of cinemas by spectators.
--      intention
--          (s,c) in Frequents <=>
--          | the spectator <s> is known to frequent the cinema <c>.
--
--      columns
--          spectator : String
--              | The name of the spectator that frequents the cinema.
--          cinema : String
--              | The name of the cinema frequented.
--      constraints
--          key spectator, cinema
--          Frequents[spectator] C= Spectators[name]
--          Frequents[movie] C= Movies[title]



CREATE TABLE Frequents(
    spectator VARCHAR(100),     -- => Spectators.name
    cinema VARCHAR(100),        -- => Cinemas.name

    CONSTRAINT PK
        PRIMARY KEY (spectator, cinema),
    CONSTRAINT FK_spectator
        FOREIGN KEY (spectator) REFERENCES Spectators(name),
    CONSTRAINT FK_cinema
        FOREIGN KEY (cinema) REFERENCES Cinemas(name)
);