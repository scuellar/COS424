580.7268815923588
657.8565990886929
747.5089198036075
841.2477020818736
821.5981108630444

import json
from pprint import pprint

json_data=open('yelp/yelp_academic_dataset_review.json')
lines0 = json_data.readlines()
lines = lines0[:]
print "pass"
smart_lines = [ json.loads(line) for line in lines]
print "pass"
length = len(lines)
print "Length: ", length
#stars = [0 for _ in range(length)]
#txt_len = [0 for _ in range(length)]
data_hist = [[] for _ in range(5)]
data_hist_all = [[] for _ in range(5)]
data = [[] for _ in range(5)]
data_all = [0 for _ in range(length)]
for i in range(5):
    data_hist[i] = [0 for _ in range(5002)]
data_hist_all = [0 for _ in range(5002)]
for n in range(length):
    star = smart_lines[n]["stars"]
    review_len = len(smart_lines[n]["text"])+1
    data_hist[star-1][review_len] +=1
    data_hist_all[review_len] +=1
    data[star-1].append(review_len)
    data_all[n] = review_len
    

json_data.close()
print "pass"
    
import numpy as np
import matplotlib.pyplot as plt

import scipy.stats as ss
import scipy as sp

#data_to_plot = data_all #data_all, data[i]
#hist_to_plot = data_hist_all #data_hist_all, data_hist[i]

#length_to_plot = len(data_to_plot)
#print "beta fit: ", ss.beta.fit(data_all)
fit_alpha = [ 0 for _ in range(5)]
fit_loc  = [ 0 for _ in range(5)] 
fit_beta = [ 0 for _ in range(5)]
length_to_plot = len(data[0])
for i in range(5):
    fit_alpha[i], fit_loc[i], fit_beta[i] = ss.gamma.fit(data[i], loc=0)
    print "For star ", (i+1)
    print fit_alpha[i], fit_loc[i], fit_beta[i]
#fit_alpha, fit_loc, fit_beta, scale = ss.gamma.fit(data_to_plot, loc=0)

#fake_data = ss.gamma.rvs(fit_alpha, loc=fit_loc, scale=fit_beta, size=5000)
real_fake_data = [ 0 for _ in range(5)]
for i in range(5):
    print "here ", i
    print length_to_plot
    real_fake_data[i] = [length_to_plot * ss.gamma.pdf(j, fit_alpha[i], fit_loc[i], fit_beta[i]) for j in range(5000)]

print "New length: ", length_to_plot

#print data_hist[4]
for i in range(5):
    #plt.plot(hist_to_plot, 'g+')
    plt.plot(real_fake_data[i], '-')
plt.xlim(0,5000)

plt.show()


