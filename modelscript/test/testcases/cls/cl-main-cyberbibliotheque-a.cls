class model CyberBibliotheque


enumeration TypeDOeuvre
    livre
    film
    musique

enumeration EtatDEmprunt
    ok
    pb

class Personne
    attributes
        nom : String


class Membre < Personne
    attributes
        login : String
        motDePasse : String


class Eleve < Membre


class Enseignant < Membre
    attributes
        matiere : String


class Employe < Membre


class Classe
    attributes
        code : String


class Atelier
    attributes
        debut : String
        fin : String
        titre : String


class Emprunt
    attributes
        debut : String
        retour : String
        etat : EtatDEmprunt


class Prolongation
    attributes
        date : String


class Bibliotheque
    attributes
        nom : String


class Stock
    attributes
        quantite : Integer


class Oeuvre
    attributes
        type : TypeDOeuvre
        titre : String
        isbn : String



association EstInscritDans 
    roles
        inscrits : Eleve [*]
        classe : Classe [1]


association IntervientDans 
    roles
        intervenants : Enseignant [*]
        classe : Classe [*]


association Realise 
    roles
        realisateur : Enseignant [1]
        realises : Atelier [*]


association TravailleSur 
    roles
        travailleuse : Classe [1]
        sujet : Atelier [*]


association AEmprunte 
    roles
        emprunteur : Membre [1]
        emprunt : Emprunt [*]


association Valide 
    roles
        valideur : Employe [1]
        validee : Prolongation [*]


association Prolonge 
    roles
        prolongation : Prolongation [0..3]
        prolonge : Emprunt [1]


association Concerne 
    roles
        concernants : Emprunt [*]
        concerne : Atelier [*]


association Fourni 
    roles
        fournisseur : Bibliotheque [*]
        fourni : Atelier [*]


association Etudie 
    roles
        ateliers : Atelier [*]
        sujets : Oeuvre [*]


association AEnStock 
    roles
        bibliotheque : Bibliotheque [1]
        stocks : Stock [*]


association StockDe 
    roles
        stock : Stock [*]
        oeuvre : Oeuvre [1]


association ObjetDe 
    roles
        oeuvre : Oeuvre [1]
        emprunt : Emprunt [*]


association EstAuteurDe 
    roles
        auteur : Personne [*]
        oeuvre : Oeuvre [*]


association EmprunteDans 
    roles
        emprunt : Emprunt [*]
        bibliotheque : Bibliotheque [1]





