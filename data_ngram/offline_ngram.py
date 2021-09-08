import requests as req
import glob
import random as rand

glob_files = glob.glob("/Users/quinones/work/prog/pyproj/games/ngram/data_ngram/*_data")
data_files = []
for f in glob_files:
	data_files.append(f[62:-5])

# read in possible words
file = open('ngram_list', 'r')
words = []
for line in file.readlines():
	if line[-1] == '\n':
	    words.append(line[:-1])
	else:
		words.append(line)
file.close()

for trend_word in words:
	if trend_word in data_files:
		#print("skipping this one")
		continue
	else:
		print( "on: ",trend_word)
	# pick min year, between 1800 and 1950
	# pick max year, between 1990 and 2020  --> round both to nearest 5, for ease of considering 
	min_year = 5*round(rand.randint(1850,1950)/5)
	max_year = 5*round(rand.randint(1990,2020)/5)
	
	# test request
	#trend_word = rand.choice(words)
	response = req.get("https://books.google.com/ngrams/json?content="+trend_word+"&year_start="+str(min_year)+"&year_end="+str(max_year)+"&corpus=26&smoothing=3")
	if not response:
		print("trend_word, min, max: ", trend_word, min_year, max_year)
		print('An error has occurred.')
		print(response)
	if response:
		print(response.json())
	
	ys = response.json()[0]["timeseries"]
	file = open(trend_word+"_data","w+")
	print(file.name)
	file.write("max:"+str(max_year)+"\n")
	file.write("min:"+str(min_year)+"\n")
	for datum in ys:
		print("writing: ", datum)
		file.write(str(datum)+"\n")
	file.close()
	# dont need xs ? just add from start to end
	#return min_year,max_year,trend_word, ys
