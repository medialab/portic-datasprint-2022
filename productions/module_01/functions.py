"""
True si la destination est la Grande-Bretagne et non les colonies anglaises à travers le monde
"""
def is_gb_destination(row):
    row['destination_substate_1789_fr'] = row['destination_substate_1789_fr'].lower()

    if row['destination_state_1789_fr'] == 'Grande-Bretagne' \
        and 'colonies britanniques' not in row['destination_substate_1789_fr']:
        return True
    return False

"""
True si l'un des champs 'commodity_standardized' contient un produit de contrebande
"""
def is_illegal_commodities(row):
    illegal_products = {'Eau-de-vie', 'Genièvre', 'Tafia', 'Tabac', 'Thé', 'Vin'}
    if row['commodity_standardized_fr'] in illegal_products \
        or row['commodity_standardized2_fr'] in illegal_products \
        or row['commodity_standardized3_fr'] in illegal_products \
        or row['commodity_standardized4_fr'] in illegal_products:
        return True
    return False

"""
True 'commodity_standardized_fr' est 'Vide' ou 'Lest' et si tous les autres champs sont empty
"""
def is_empty_strict_commodities(row):
    if (row['commodity_standardized_fr'] == 'Vide' or row['commodity_standardized_fr'] == 'Lest') \
        and row['commodity_standardized2_fr'] == '' \
        and row['commodity_standardized3_fr'] == '' \
        and row['commodity_standardized4_fr'] == '':
        return True
    return False

def is_smoggleur_dunkerque(row):
    if row['departure_fr'] != 'Dunkerque':
        return False
    if row['flag'] == 'British' \
        and row['tonnage'] == 12 :
        return True
    return False

def is_smoggleur_calais(row):
    if row['departure_fr'] != 'Calais':
        return False
    if row['flag'] == 'British' \
        and row['tonnage'] <= 50 \
        and is_gb_destination(row) == True:
        return True
    return False

def is_smoggleur_boulogne(row):
    if row['departure_fr'] != 'Boulogne-sur-Mer':
        return False
    if row['flag'] == 'British' \
        and is_gb_destination(row) == True:
        return True
    return False

def is_smoggleur_roscoff(row):
    if row['departure_fr'] != 'Roscoff':
        return False
    if (is_gb_destination(row) == True or row['destination_uhgs_id'] in {'A1964976', 'A0912818', 'A0864873'}) \
        and is_illegal_commodities(row) == True:
        return True
    return False

def is_smoggleur_lorient(row): # 51 + 5 + 1
    if row['departure_fr'] != 'Lorient':
        return False
    if row['flag'] == 'British' \
        and row['destination_uhgs_id'] in {
            'A0840357', # Norvège
            'A0912818', # Bergen
            'A1964976'}: # Îles Féroé
        return True
    return False

def is_smoggleur_bordeaux(row):
    if row['departure_fr'] != 'Bordeaux':
        return False
    if row['flag'] == 'British' \
        and row['destination_uhgs_id'] in {'A1964976', 'A0912818'} \
        and is_illegal_commodities(row) == True:
        return True
    return False