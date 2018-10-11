-- Participant
--     ParticipantClass
--         Actor
--         Stakeholder
--         TeamRole
--     ParticipantInstance
--         Person
--         Personage
--         Personae

participant model Demo

actor Cashier
    | The documentation of the user
    | using two lines

actor Client

actor SpecialClient < Client

stakeholder StoreManager
    | StoreManagers want the cash machine to
    | collect the exact amount of money and
    | to store safely this money.


team role Developer
    | A developer is responsible to develop and maintain
    | some pecises of Code

team role QualityManager
    | The QualityManager is responsible to ensure that the
    | quality of the product stay in line with quality
    | requirements.

team role CodeQualityManager < QualityManager
    | A `CodeQualityManager` do something with code.

team role ScrumMaster
    | A scrum master is a facilitator in the context of
    | a `ScrumTeam`

team role ProductOwner

person mariaStafani : Developer, QualityManager
    trigram: MSI
    | blabla blabla

personae marco : Cashier
    | Marco is 32 years old.
    | He is used to computers and phones software.

personage jean : Cashier, Client
    | Jean is 50 years old.
    | He is used to computers and phones software.