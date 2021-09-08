import requests as req
import random as rand


def get_data():
	# read in possible words
	file = open('ngram_list', 'r')
	words = []
	for line in file.readlines():
	    if line[-1] == '\n':
	        words.append(line[:-1])
	    else:
	    	words.append(line)
	
	# pick min year, between 1800 and 1950
	# pick max year, between 1990 and 2020  --> round both to nearest 5, for ease of considering 
	min_year = 5*round(rand.randint(1860,1950)/5)
	max_year = 5*round(rand.randint(1990,2020)/5)
	
	# test request
	trend_word = rand.choice(words)
	response = req.get("https://books.google.com/ngrams/json?content="+trend_word+"&year_start="+str(min_year)+"&year_end="+str(max_year)+"&corpus=26&smoothing=3")
	if not response:
		print('An error has occurred.')
	
	ys = response.json()[0]["timeseries"]
	
	# dont need xs ? just add from start to end
	return min_year,max_year,trend_word, ys