participant model Demo

actor Cashier
    | The documentation of the user
    | using two lines

actor Client

actor SpecialClient < Client

personage marco : Cashier
    | Marco is 32 years old.
    | He is used to computers and phones software.

personage jean : Cashier, Client
    | Jean is 50 years old.
    | He is used to computers and phones software.

role Developer
    | A developer is responsible to develop and maintain
    | some pecises of Code

role QualityManager
    | The QualityManager is responsible to ensure that the
    | quality of the product stay in line with quality
    | requirements.

role CodeQualityManager < QualityManager
    | A `CodeQualityManager` do something with code.

role ScrumMaster
    | A scrum master is a facilitator in the context of
    | a `ScrumTeam`

role ProductOwner

participant mariaStafani : Developer, QualityManager
    trigram: MSI
    |