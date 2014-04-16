GOOD_FOR = ["dessert", "latenight", "lunch", "dinner", "brunch", "breakfast"]
G4SIZE = len(GOOD_FOR)
AMBIENCE = ["romantic", "intimate", "touristy", "hipster", "divey", "classy", "trendy", "upscale", "casual"]


""" Function Feature Vectors Bussiness 
Create a dictionary (ordered by ID) of vectors for business with some specific features defined bellow
- "Good For": {"dessert": _, "latenight": _, "lunch": _, "dinner": _, "brunch": _, "breakfast": _},
- "Ambience": {"romantic": _, "intimate": _, "touristy": _, "hipster": _, "divey": _, "classy": _, "trendy": _, "upscale": _, "casual": _},
- "stars": 4.0
"""
def busFeatureVector(dic):
    busFVs = {}
    print "Extracting business vectors..."
    for n, bus in enumerate(dic):
        attributes = bus.get("attributes", None)
        #print "attributes ", attributes
        if attributes is None:
            continue
        ID = bus.get("business_id", None)
        good_for = attributes.get("Good For", None)
        bus_ambience = attributes.get("Ambience", None)
        stars = bus.get("stars", None)
        if (ID and good_for and bus_ambience and stars):
            vector = [0]*(len(GOOD_FOR)+len(AMBIENCE)+1)
            vector[0] = stars
            flag = False
            for i, good4 in enumerate(GOOD_FOR):
                vec_entry = good_for.get(good4, None)
                if vec_entry is None:
                    flag = True
                    break
                vector[i+1] = int(vec_entry)
            for i, amb in enumerate(AMBIENCE):
                vec_entry = bus_ambience.get(amb, None)
                if vec_entry is None:
                    flag = True
                    break
                vector[i+G4SIZE+1] = int(vec_entry)
            if not flag:
                busFVs[ID] = vector
        if n>0 and n%50000==0:
            print n," business processed..."
    print "Done extracting business vectors."
    return (len(busFVs), busFVs)
