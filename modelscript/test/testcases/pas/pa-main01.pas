// Participant
//     ParticipantClass
//         Actor
//         Stakeholder
//         TeamRole
//     ParticipantInstance
//         Person
//         Persona



participant model Demo


actor Cashier
    | Cashiers are employee of `Cinemas`. The role of `Cashiers`
    | is to sell `Ticket` to `Spectators`. They also manage
    | `Subscriptions`. To perform these tasks`Cashiers` should have a
    | desktop application at their disposal.

actor HighCashier < Cashier
    | HighCashiers can cancel `Transactions` and launch
    | `MoneyBack` operations.


stakeholder role Treasurer
    | The role of the Treasurers in the process is to check
    | that `FinancialTransaction` with be processed accurately
    | in the system to be build.

team role Developer
    | A developer is responsible to design, develop, test and
    | maintain models and pieces of code.

team role QualityManager
    | The QualityManager is responsible to define, with other
    | members of the development team, `QA` standard.
    | She also monitors `QC` process although she can to delegate
    | actual controls to other team members.
    |

team role QualityMaster < QualityManager
    | A `QualityMaster` has all duties and privileges of
    |`QualityManager` but she also has the power to change
    | the content of `QA` and `QC` standard.

team role ScrumMaster
    | The `ScrumMaster` is the team role responsible for
    | ensuring the team lives agile values and principles and
    | follows the processes and practices that the team
    | agreed they would use.
    | The responsibilities of this role include:
    | * clearing obstacles,
    | * Establishing an environment where the team can be effective
    | * Addressing team dynamics
    | * Ensuring a good relationship between the team and
    |   product owner as well as others outside the team
    | Protecting the team from outside interruptions and distractions.

team role ProductOwner
    | The `ProductOwner` responsibility is to have a vision of
    | what she wishes to build, and convey that vision to the
    | `ScrumTeam`.

person marieDupont : Developer, QualityManager
    name : "Marie Dupont Laurent"
    trigram : MDL
    portrait : './mdupont.png'
    attitudes
    aptitudes
        age : 12
    skills
    motivations
    | trigram: MSI
    | blabla blabla

persona marco : Cashier, Client
    name : "Marco Gonzales"
    trigram : MGS
    | Marco is 45 years old.
    | He is used to computers and phones.
    | Some more description about marco
    attitudes
        | marco likes playing football.
        | He also loves eating pizza and playing with this
        | damned computer system.
    aptitudes
        education
            | master software engineering (1992)
            | PhD in medio chemicals (1999)
        languages
            | english (fluent)
            | spanish (novice)
        age : 45
        disabilities : "blind"
        learning ability : low
        | Marco is kind to learn but he also knows already
        | very much.
    motivations
        why
            | Marco is really reluctant to use the system.
            | Her boss, anna, told him that he will be fired
            | if he do not get good results.
        level : low
        kind : obliged
        | Some additional remark or documentation
    skills
        | Marco is an expert in playing with the mouse.
        level : novice
        culture
            | occidental
        modalities
            "labtop" : expert
            "smartphone" : novice
            "iPhone 10.3" : expert
        environments
            "Ubuntu" : expert
            "Windows" : intermediate
            "Android 18.5" : novice


adhoc persona jean : Cashier, Client
    | Jean is 50 years old.
    | He is used to computers and phones software.