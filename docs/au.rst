.. .. coding=utf-8

au - AUIs
=========

Abstract space
--------------

Concepts
--------

Links
-----

Transformation
--------------

Examples
--------

..  code-block:: AUIScript

    aui model Demo

    space EntrerLesInformations
        | Some documentation
        concepts
            email
            numerotel
        links
            ChoisirTypeReservation
            EntrerLesInformations


    space EntrerLesInformations "Réservation"
        concepts
            email "email"
            numerotel "numéro de téléphone"
        links
            ChoisirTypeReservation "type"
            EntrerLesInformations "détail"
            back to EntrerLesInformations "précédent"
        transformation
            from
                Informer
            rule R1
            rule R2
            | Some explaination

    space ChoisirTypeReservation
        links
            ReservationSansPayer
            Reserver
            back to EntrerLesInformations

    space ReservationSansPayer
        links
            back to ChoisirTypeReservation
            PreciserCriteresDeRecherche

    space PreciserCriteresDeRecherche
        links
            EntrerLesInformations

    space Reserver
        links
            back to ChoisirTypeReservation
            Payer

    space Payer
        concepts
            modeDePaimement
            numeroDeCarte
        links
            ChoisirTypeDeBillet
            Payer

    space ChoisirTypeDeBillet
        concepts
            pdf
            mobile
        links
            back to PreciserCriteresDeRecherche


    space PreciserCriteresDeRecherche
        links
            EntrerLesInformations