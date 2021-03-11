import requests


# https://rxnav.nlm.nih.gov/REST/drugs.json?name=cymbalta

def getRXCUI(drugName):
    url = 'https://rxnav.nlm.nih.gov/REST/drugs.json?name='
    url += drugName
    r = requests.get(url)
    drugGroup = r.json()['drugGroup']
    if 'conceptGroup' in drugGroup:
        groups = drugGroup['conceptGroup']
        for item in groups:
            if 'conceptProperties' in item:
                return str(item['conceptProperties'][0]['rxcui'])
    return None


def getInteractionsSingleDrug(drug1):
    RXCUI = getRXCUI(drug1)
    drugInteraction = []
    explanation = []
    severity = []
    if RXCUI is not None:
        url = 'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + RXCUI + '&sources=DrugBank'
        r = requests.get(url)
        groups = r.json()
        if 'interactionTypeGroup' in groups:
            for interactionGroup in groups['interactionTypeGroup']:  # list of interactions from multiple sources?
                for interactionType in interactionGroup['interactionType']:
                    interactionPairs = interactionType['interactionPair']
                    for pair in interactionPairs:
                        # print(pair['description'])
                        drugInteraction.append(pair['interactionConcept'][1]['minConceptItem']['name'])
                        explanation.append(pair['description'])
                        severity.append(pair['severity'])
            return zip(drugInteraction, explanation, severity)
    return None

def getInteractionsBetweenDrugs(drug1, drug2):
    drug1Interactions = getInteractionsSingleDrug(drug1)
    if drug1Interactions is not None:
        drugInteractions = []
        explanations = []
        severities = []
        for drugInteraction, explanation, severity in drug1Interactions:
            if drugInteraction == drug2:
                drugInteractions.append(drugInteraction)
                explanations.append(explanation)
                severities.append(severity)
        if len(drugInteractions) == 0:
            return None
        return zip(drugInteractions, explanations, severities)
    return None
