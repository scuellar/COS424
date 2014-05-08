import numpy as np

class Business:
    def __init__ (self, bus_dic, default = 0):
        self.default = default
        self.dico = bus_dic
        self.name = self.dico.get("name") 
        self.vec = {}
        self.features = []
        self.vector = None
        
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

        #self.vec["Noise Level"] = attributes.get("Noise Level")
        self.vec["Takes Reservations"] = attributes.get("Takes Reservations")
        self.vec["Has TV"] = attributes.get("Has TV")
        self.vec["Delivery"] = attributes.get("Delivery")
        #self.vec["Wheelchair Accessible"] = attributes.get("Wheelchair Accessible")
        self.vec["Outdoor Seating"] = attributes.get("Outdoor Seating")
        #self.vec["Attire"] = attributes.get("Attire") #Not boolean 
        #self.vec["Alcohol"] = attributes.get("Alcohol")  #Not boolean 
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
        
    def processVect(self, d):
        for key, value in d.iteritems():
            if value is None:
                d[key] = self.default
            elif value==True :
                d[key] = 1
            elif value == False :
                d[key] = 0

                
        
