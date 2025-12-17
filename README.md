# TrelloBurndown


Dette lille Python-projekt er egentlig bare noget jeg har skrabet sammen for at lave burndown diagrammer af user stories fra Trello. Det kører på Python, og hoveddelene er to scripts: TrelloJSONExportToCSV.py og TrelloCSVBurndownMaker.py.

Først henter man simpelthen Trello-boardet som JSON via:

https://trello.com/x/x/boardname.json


Derefter kører man TrelloJSONExportToCSV.py, som konverterer JSON’en til CSV. Her er det især vigtigt at få fat i de felter, der markerer om en task/story er færdig – resten er mest for at få noget brugbart data at lege med.

Når CSV’en er klar, smider man den ind i TrelloCSVBurndownMaker.py. Så åbner der et vindue hvor man kan justere tidsramme, tilføje milepæle og alt det andet lort, jeg har fået stablet sammen. Det er ikke verdens mest elegante løsning, men det virker til at få et hurtigt overblik over hvor langt man er i sprinten, og det er præcis sådan jeg ville have det: hjemmelavet og lige til at pille ved.
