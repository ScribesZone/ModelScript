--=========================================================================
-- CyberCinemas
--=========================================================================
-- Based on the course of M.C. Fauvet
---------------------------------------------------------------------------



---------------------------------------------------------------------------
-- Prolog for sqlite
---------------------------------------------------------------------------

PRAGMA foreign_keys = ON;

---------------------------------------------------------------------------
-- Movies
---------------------------------------------------------------------------

INSERT INTO Movies VALUES ('Guardians Of The Galaxy','2014');
INSERT INTO Movies VALUES ('The Inbetweeners 2','2014');
INSERT INTO Movies VALUES ('The Hundred Foot Journey','2014');
INSERT INTO Movies VALUES ('Lucy','2014');
INSERT INTO Movies VALUES ('If I Stay','2014');
INSERT INTO Movies VALUES ('The Green Hornet','2011');
INSERT INTO Movies VALUES ('The Company Men','2011');
INSERT INTO Movies VALUES ('Every Day','2011');
INSERT INTO Movies VALUES ('Last Lions','2011');
INSERT INTO Movies VALUES ('Pretty Woman','1990');
INSERT INTO Movies VALUES ('Edward Scissorhands','1990');
INSERT INTO Movies VALUES ('Hamlet','1990');
INSERT INTO Movies VALUES ('I. Robot','2004');
INSERT INTO Movies VALUES ('Crooks in Clover','1963');
INSERT INTO Movies VALUES ('America America','1963');
INSERT INTO Movies VALUES ('A Child Is Waiting','1963');
INSERT INTO Movies VALUES ('Australia','2008');


---------------------------------------------------------------------------
-- Cinemas
---------------------------------------------------------------------------

INSERT INTO Cinemas VALUES ('Hoyts CBD','Sydney');
INSERT INTO Cinemas VALUES ('Hoyts','Brisbane');
INSERT INTO Cinemas VALUES ('Event Cinema Myer','Brisbane');
INSERT INTO Cinemas VALUES ('Event Cinema','Cairns');
INSERT INTO Cinemas VALUES ('Birch Carroll and Coyles','Brisbane');
INSERT INTO Cinemas VALUES ('Event Cinema Red Center','Alice Spring');


---------------------------------------------------------------------------
-- Spectators
---------------------------------------------------------------------------

INSERT INTO Spectators VALUES ('Marie','1970','Sydney');
INSERT INTO Spectators VALUES ('Adrian','1950','Cairns');
INSERT INTO Spectators VALUES ('Phil','1960','Sydney');
INSERT INTO Spectators VALUES ('Jackie','1965','Sydney');
INSERT INTO Spectators VALUES ('Tom','1986','Brisbane');
INSERT INTO Spectators VALUES ('Alizee','1988','Alice Spring');
INSERT INTO Spectators VALUES ('Lauranne','1986','Amsterdam');

---------------------------------------------------------------------------
-- Opinions
---------------------------------------------------------------------------

INSERT INTO Opinions VALUES ('Marie','The Inbetweeners 2','0');
INSERT INTO Opinions VALUES ('Adrian','The Inbetweeners 2','0');
INSERT INTO Opinions VALUES ('Phil','The Inbetweeners 2','2');
INSERT INTO Opinions VALUES ('Jackie','The Inbetweeners 2','2');
INSERT INTO Opinions VALUES ('Tom','The Inbetweeners 2','5');
INSERT INTO Opinions VALUES ('Alizee','The Inbetweeners 2','4');
INSERT INTO Opinions VALUES ('Lauranne','The Inbetweeners 2','0');
INSERT INTO Opinions VALUES ('Marie','Pretty Woman','5');
INSERT INTO Opinions VALUES ('Adrian','Pretty Woman','4');
INSERT INTO Opinions VALUES ('Phil','Pretty Woman','4');
INSERT INTO Opinions VALUES ('Jackie','Pretty Woman','3');
INSERT INTO Opinions VALUES ('Tom','Pretty Woman','5');
INSERT INTO Opinions VALUES ('Alizee','Pretty Woman','4');
INSERT INTO Opinions VALUES ('Marie','Edward Scissorhands','3');
INSERT INTO Opinions VALUES ('Adrian','Edward Scissorhands','4');
INSERT INTO Opinions VALUES ('Alizee','Edward Scissorhands','4');
INSERT INTO Opinions VALUES ('Lauranne','Edward Scissorhands','5');
INSERT INTO Opinions VALUES ('Marie','Lucy','3');
INSERT INTO Opinions VALUES ('Adrian','Lucy','4');
INSERT INTO Opinions VALUES ('Phil','Lucy','5');
INSERT INTO Opinions VALUES ('Jackie','Lucy','2');
INSERT INTO Opinions VALUES ('Tom','Lucy','1');
INSERT INTO Opinions VALUES ('Alizee','Lucy','5');
INSERT INTO Opinions VALUES ('Lauranne','Lucy','5');
INSERT INTO Opinions VALUES ('Marie','I. Robot','5');
INSERT INTO Opinions VALUES ('Adrian','I. Robot','5');
INSERT INTO Opinions VALUES ('Marie','Crooks in Clover','5');
INSERT INTO Opinions VALUES ('Tom','Crooks in Clover','5');
INSERT INTO Opinions VALUES ('Alizee','Crooks in Clover','5');
INSERT INTO Opinions VALUES ('Lauranne','Crooks in Clover','5');
INSERT INTO Opinions VALUES ('Marie','Australia','0');
INSERT INTO Opinions VALUES ('Adrian','Australia','5');


---------------------------------------------------------------------------
-- IsOn
---------------------------------------------------------------------------

INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Hoyts CBD');
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Hoyts');
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Event Cinema Myer');
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Event Cinema');
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Birch Carroll and Coyles');
INSERT INTO IsOn VALUES ('Crooks in Clover','Hoyts CBD');
INSERT INTO IsOn VALUES ('Crooks in Clover','Hoyts');
INSERT INTO IsOn VALUES ('Crooks in Clover','Event Cinema Myer');
INSERT INTO IsOn VALUES ('Crooks in Clover','Event Cinema');
INSERT INTO IsOn VALUES ('The Company Men','Birch Carroll and Coyles');
INSERT INTO IsOn VALUES ('The Company Men','Hoyts CBD');
INSERT INTO IsOn VALUES ('The Company Men','Hoyts');
INSERT INTO IsOn VALUES ('America America','Event Cinema Myer');
INSERT INTO IsOn VALUES ('America America','Event Cinema');
INSERT INTO IsOn VALUES ('America America','Birch Carroll and Coyles');
INSERT INTO IsOn VALUES ('Australia','Event Cinema Myer');
INSERT INTO IsOn VALUES ('Australia','Event Cinema');
INSERT INTO IsOn VALUES ('Australia','Birch Carroll and Coyles');
INSERT INTO IsOn VALUES ('Pretty Woman','Event Cinema Myer');
INSERT INTO IsOn VALUES ('Pretty Woman','Event Cinema');
INSERT INTO IsOn VALUES ('Pretty Woman','Birch Carroll and Coyles');


---------------------------------------------------------------------------
-- Frequents
---------------------------------------------------------------------------

INSERT INTO Frequents VALUES ('Marie','Hoyts CBD');
INSERT INTO Frequents VALUES ('Adrian','Hoyts CBD');
INSERT INTO Frequents VALUES ('Phil','Hoyts CBD');
INSERT INTO Frequents VALUES ('Jackie','Hoyts CBD');
INSERT INTO Frequents VALUES ('Tom','Hoyts');
INSERT INTO Frequents VALUES ('Alizee','Event Cinema');
INSERT INTO Frequents VALUES ('Marie','Hoyts');
INSERT INTO Frequents VALUES ('Adrian','Hoyts');
INSERT INTO Frequents VALUES ('Phil','Event Cinema');
INSERT INTO Frequents VALUES ('Jackie','Event Cinema');
INSERT INTO Frequents VALUES ('Tom','Birch Carroll and Coyles');