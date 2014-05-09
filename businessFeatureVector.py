import numpy as np

class Business(list):
    def __init__ (self, bus_dic, default = 0, include_cats = True):
        self.default = default
        self.dico = bus_dic
        self.id = self.dico.get("business_id")
        self.name = self.dico.get("name").encode('utf-8')
        self.vec = {}
        self.features = []
        self.vector = None

        if include_cats:
            self.makeCategories() #Includes the top categories in the vector
        self.makeFlatDic() #Makes self.vec as a dictionary with all attributes
        self.extractFeatures() #Makes self.features with all the features in self.vec
        self.processVect(self.vec) #Cleans self.vec (True -> 1, false -> 0, None -> self.default)
        self.npVector() #Makes a numpy vector with the features and the dictionary.


        
        
    def npVector(self):
        self.vector = np.array([self.vec[feat] for feat in self.features])
        
    def makeFlatDic(self):
        self.vec["review_count"] = self.dico.get("review_count")
        self.vec["stars"] = self.dico.get("stars")

        attributes = self.dico.get("attributes", {})
        self.makeFlatAttributes(attributes)


    def makeFlatAttributes(self, attributes):
        self.vec["Take-out"] = attributes.get("Take-out")

        self.vec["Noise Level"] = self.processNoise( attributes.get("Noise Level") )
        self.vec["Takes Reservations"] = attributes.get("Takes Reservations")
        self.vec["Has TV"] = attributes.get("Has TV")
        self.vec["Delivery"] = attributes.get("Delivery")
        #self.vec["Wheelchair Accessible"] = attributes.get("Wheelchair Accessible")
        self.vec["Outdoor Seating"] = attributes.get("Outdoor Seating")
        self.vec["Attire"] = self.processAttire( attributes.get("Attire")) #Not boolean 
        self.vec["Alcohol"] = self.processAlcohol(attributes.get("Alcohol"))  #Not boolean 
        self.vec["Waiter Service"] = attributes.get("Waiter Service")
        #self.vec["Accepts Credit Cards"] = attributes.get("Accepts Credit Cards")
        self.vec["Good for Kids"] = attributes.get("Good for Kids")
        self.vec["Good For Groups"] = attributes.get("Good For Groups")
        self.vec["Price Range"] = attributes.get("Price Range")
        
        good_for = attributes.get("Good For", {})
        self.makeGoodFor(good_for)

        ambience = attributes.get("Ambience", {})
        self.makeAmbience(ambience)

        parking = attributes.get("Parking", {})
        self.makeParking(parking)
        
    def makeGoodFor(self, good_for):
        self.vec["dessert"] = good_for.get("dessert")
        self.vec["latenight"] = good_for.get("latenight")
        self.vec["lunch"] = good_for.get("lunch")
        self.vec["dinner"] = good_for.get("dinner")
        self.vec["brunch"] = good_for.get("brunch")
        self.vec["breakfast"] = good_for.get("breakfast")
        
        
        
    def makeAmbience(self, ambience):
        self.vec["romantic"] = ambience.get("romantic")
        self.vec["intimate"] = ambience.get("intimate")
        self.vec["touristy"] = ambience.get("touristy")
        self.vec["hipster"] = ambience.get("hipster")
        self.vec["divey"] = ambience.get("divey")
        self.vec["classy"] = ambience.get("classy")
        self.vec["trendy"] = ambience.get("trendy")
        self.vec["upscale"] = ambience.get("upscale")
        self.vec["casual"] = ambience.get("casual")

    def makeParking(self, parking):
        return None
        #self.vec["garage"] = parking.get("garage")
        #self.vec["street"] = parking.get("street")
        #self.vec["validated"] = parking.get("validated")
        #self.vec["lot"] = parking.get("lot")
        #self.vec["valet"] = parking.get("valet")

        
        #self.hours = dico.get("hours")
        #if self.hours is None:
        #    raise Exception("Business with no hours: " + self.name)

    def extractFeatures(self):
        self.features = self.vec.keys()

    """ Some attributes need processing"""
    def processVect(self, d):
        for key, value in d.iteritems():
            if value is None:
                d[key] = self.default
            elif value is True :
                d[key] = 1
            elif value is False :
                d[key] = -1

    def processNoise(self, noise):
        if noise is None:
            return 0
        elif noise == "quiet":
            return 1
        elif noise == "average":
            return 0
        elif noise == "loud":
            return -1
        elif noise == "very_loud":
            return -2
        else:
            raise Exception("Unknown noise level "+ str(noise))

    def processAttire(self, att):
        if att is None:
            return 0
        elif att == "casual":
            return 0
        elif att == "dressy":
            return 1
        elif att == "formal":
            return 2
        else:
            raise Exception("Unknown attire type: "+ str(att))

    def processAlcohol(self, alc):
        if alc is None:
            return 0
        elif alc == "none":
            return 0
        elif alc == "beer_and_wine":
            return 1
        elif  alc == "full_bar":
            return 2
        else:
            raise Exception("Unknown alcohol type: "+ str(alc))


    def makeCategories(self):
        """I start with a hard coded list of top categories"""
        """For more info See getCategories.py"""
        cats = [u'Hair Salons', u'Ice Cream & Frozen Yogurt', u'Nail Salons', u'Pets', u'Breakfast & Brunch', u'Auto Repair', u'Hotels', u'Chinese', u'Italian', u'Home & Garden', u'Burgers', u'Arts & Entertainment', u'Coffee & Tea', u'Grocery', u'American (New)', u'Hotels & Travel', u'Local Services', u'Event Planning & Services', u'Pizza', u'Fast Food', u'American (Traditional)', u'Sandwiches', u'Bars', u'Active Life', u'Fashion', u'Nightlife', u'Home Services', u'Health & Medical', u'Mexican', u'Automotive', u'Beauty & Spas', u'Food', u'Shopping', u'Restaurants']
        # cats = ['Coffee & Tea', 'Grocery', 'American (New)', 'Hotels & Travel', 'Local Services', 'Event Planning & Services', 'Pizza', 'Fast Food', 'American (Traditional)', 'Sandwiches', 'Bars', 'Active Life', 'Fashion', 'Nightlife', 'Home Services', 'Health & Medical', 'Mexican', 'Automotive', 'Beauty & Spas', 'Food', 'Shopping', 'Restaurants']
        #cats = ['Fast Food', 'American (Traditional)', 'Sandwiches', 'Bars', 'Active Life', 'Fashion', 'Nightlife', 'Home Services', 'Health & Medical', 'Mexican', 'Automotive', 'Beauty & Spas', 'Food', 'Shopping', 'Restaurants']
        for cat in cats:
            self.vec[cat] = -1
        myCategories = self.dico.get("categories", [])
        for cat in myCategories:
            if cat in cats:
                self.vec[cat] = 1
        

    """Define a list format, which I can customize"""
    def __len__(self):
        return len(self.vector)
    def __getitem__(self, ii):
        return self.vector[ii]
    def __delitem__(self, ii):
        del self.vector[ii]
    def __setitem__(self, ii, val):
        return self.vector[ii]
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return """<{name}>""".format(name = self.name)
    def insert(self, ii, val):
        self.vector.insert(ii, val)
    def append(self, val):
        list_idx = len(self._list)
        self.insert(list_idx, val)

                
        
