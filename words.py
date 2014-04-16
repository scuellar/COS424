import readYelp

def getListWords(sentence):
    return sentence.split()

def bagOfWords(dic):
    stars = 0
    words = []
    per_ratting_list = [[] for i in range(5)]
    list_of_all_words = []
    print "Extracting words from reviews..."
    for n,review in enumerate(dic):
        stars = review["stars"]
        words = getListWords(review["text"])
        #words = [word for word in words if len(word)>2]
        per_ratting_list[stars - 1].append(words)
        #list_of_all_words = list_of_all_words + words
        if n>0 and n%50000==0:
            print n," reviews processed..."
    print "Done extracting words."
    return (list_of_all_words, per_ratting_list)
