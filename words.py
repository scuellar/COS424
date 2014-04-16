import readYelp

def getListWords(sentence):
    return sentence.split()

""" Function Bag of Words
BAD NAME: this doesn't return a bag, bur a list with repetitions.
Returns a list of words used for each ratting. It's not a bag, but a repeating list.
"""
def bagOfWords(dic):
    stars = 0
    words = []
    per_ratting_list = [[] for i in range(5)]
    list_of_all_words = []
    print "Extracting words from reviews..."
    for n,review in enumerate(dic):
        stars = review["stars"]
        words = getListWords(review["text"])
        #words = [word for word in words if len(word)>2] #Uncomment to put a lower bownd to the size of the words
        per_ratting_list[stars - 1].append(words)
        #list_of_all_words = list_of_all_words + words #Uncomment to have an overall dictionary (slow)
        if n>0 and n%50000==0:
            print n," reviews processed..."
    print "Done extracting words."
    return (list_of_all_words, per_ratting_list)
