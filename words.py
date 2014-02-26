import readYelp

def getListWords(sentence):
    return sentence.split()

def bagOfWords(dic):
    stars = 0
    words = []
    per_ratting_list = [[] for i in range(5)]
    list_of_all_words = []
    for review in dic:
        stars = review["stars"]
        words = getListWords(review["text"])
        per_ratting_list[stars - 1].append(words)
        list_of_all_words = list_of_all_words + words
    return (list_of_all_words, per_ratting_list)
