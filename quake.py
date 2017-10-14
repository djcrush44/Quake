import urllib.request
import urllib.parse
import time
import math

# inputs responses until valid response is given
def field_input(l):
	test = input("Input %s: " %l)
	while (not is_number(test)):
		test = input("Not a valid number. Try again: ")
	return test

# inputs responses until valid positive integer is given	
def field_integer(i):
	test = input("Input %s: " %i)
	while (not str.isdecimal(test) or int(test)<=0):
		test = input("Not a valid positive integer. Try again: ")
	return test

# returns probablity of quake in next x years as a percentile	
def get_prob(lam,x):
	return (1-math.pow(math.e,-lam*x)) * 100
	
# checks that input is a valid decimal number	
def is_number(s):
    try:
        complex(s)
        return True
    except ValueError:
        return False


		
		
# calculate starting year from user input
userYears = field_integer('number of years to search')
date = time.gmtime(time.time())
year = date[0] - int(userYears)

# create parameters for web query
data = {}
data['starttime'] = str(year) + time.strftime('-%m-%d')
data['latitude'] = field_input('latitude')
data['longitude'] = field_input('longitude')
data['maxradiuskm'] = field_input('search radius (km)')

# create complete url 
url_values = urllib.parse.urlencode(data)
url = 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=quakeml&' + url_values

# fetch query from database
with urllib.request.urlopen(url) as response:
		query = response.read()

		
# compute total quake count and lambda
count = int(query)
avg = count/int(userYears)

# compute mean, median, and starting probabilites from exponential distribution
if avg == 0:
	beta = 0
else:
	beta = 1/avg
median = beta * math.log(2)
prob = {}

prob['day'] = get_prob(avg, 1/365)
prob['month'] = get_prob(avg,1/12)
prob[1] = get_prob(avg,1)
prob[5] = get_prob(avg,5)
prob[10] = get_prob(avg,10)

# print results
print("\nRESULTS\nNumber of recorded quakes: %d" % count)
print("Median time until next quake: %f years" % median)
print("Mean time until next quake: %f years\n" % beta)


# print each time period calculated above
for year in prob:
	if type(year) == int:
		print("Probability that a quake will occur within %d year(s): %f%%" % (int(year),prob[year]))
	else:
		print("Probability that a quake will occur within a %s: %f%%" % (year,prob[year]))


# field user input for custom time search		
keepSearching = input("Would you like to check the probability of other years? Response may be a decimal. [y/n] ")
while keepSearching == 'y' or keepSearching == 'Y':
	year = field_input("number of years")
	p = get_prob(avg,float(year))
	print("There is a %f%% probability of a quake within the next %s year(s)" % (p,year))
	keepSearching = input("Would you like to check the probability of other years? [y/n] ")
	