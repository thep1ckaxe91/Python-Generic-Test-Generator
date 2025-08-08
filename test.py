# import the required libraries 
import random 
import matplotlib.pyplot as plt 
  
# store the random numbers in a list 
nums = [] 
mu = 30
sigma = 7
  

for i in range(1000000): 
    temp = random.normalvariate(mu, sigma) 
    nums.append(temp) 
      
# plotting a graph 
plt.hist(nums, bins = 'auto') 
plt.show()