def reviewsPerUser(dic):
    revPerUser = {}    
    for n, review in enumerate(dic):
        user_ID = review.get("user_id", None)
        bus_ID = review.get("business_id", None)
        stars = review.get("stars", None)
        if (user_ID is None or bus_ID is None):
            print "Useless review here without User ID, Business ID or stars. Number", n
        prev = revPerUser.get(user_ID, {})
        prev[bus_ID] = stars
        revPerUser[user_ID] = prev
        
        if n>0 and n%5000==0:
            print n," Reviews processed..."
    return revPerUser
