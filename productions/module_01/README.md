# Module 01 : Dunkerque, un port de smoggleurs à comparer, quelle taille du smogglage à Dunkerque par rapport à celui des autes ports français

## Repérer les smoggleurs par ports

Au sujet des destinations :
- "Nord Ferrow" équivaut à `destination_uhgs_id == A1964976` équivaut à `destination_fr == Îles Féroé` (vérifié dans les données)

- Dunkerque :
    - `flag == 'British'`
    - `tonnage == 12`
- Calais :
    - `flag == 'British'`
    - `destination` = `Grande-Bretagne` hors colonies
    - `tonnage >= 50`
- Boulogne-sur-Mer (2 smoggleurs)
    - `flag == 'British'`
    - `destination` = `Grande-Bretagne` hors colonies
- Roscoff
    - `destination == Grande-Bretagne` ou « Iles Feroe », « Bergen », « Cap Nord »
    - `commodity_standardized_fr` = eau-de-vie, genièvre, tafia, tabac, thé
- Lorient
    - `flag == 'British'`
    - `destination` Nord Ferrow, Bergen, Norvège
- Bordeaux
    - `flag == 'British'`
    - `destination` Nord Ferrow, Bergen
    - `commodity_standardized_fr` = vin OU  eau-de-vie OU tabac