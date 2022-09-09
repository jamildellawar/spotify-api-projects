

def defineVariations():
    """
    Defines the words we have different variations of and 
    what those variations are.

    Returns:
        listsOfVariations (List) = list of all variations in separate lists
    """
    youVariations = ['you', 'u']
    yourVariations = ['your', 'ur']
    youreVariations = ['youre', 'ur', 'you\'re']
    toVariations = ['to', '2']
    andVariations = ['and', '&']
    broVariations = ['bro', 'dude', 'bruh', 'homie', 'yo']
    theVariations = ['the', 'da']
    pleaseVariations = ['please', 'pls']
    forVariations = ['for', '4', 'four']

    listsOfVariations = [
        youVariations,
        yourVariations,
        youreVariations, 
        youreVariations,
        toVariations,
        andVariations, 
        broVariations,
        theVariations,
        pleaseVariations,
        forVariations
    ]
        
    return listsOfVariations

def whichVariation(listsOfVariations, wordToCheck):
    """
    Returns list of words that are similar to wordToCheck

    Args:
        listsOfVariations (List): list of all variations in separate lists
        wordToCheck (String): _description_

    Returns:
        wordsToCheck (List): the list of possible variations for the wordToCheck
    """
    for wordsToCheck in listsOfVariations:
        if wordToCheck in wordsToCheck:
            return wordsToCheck
    
    return [wordToCheck]


