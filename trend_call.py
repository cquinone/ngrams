from pytrends.request import TrendReq
import pandas as pd
import random as rand
import time


def get_day_month():
	 month = rand.randint(1,12)
	 if month != 2: # not february
	      day = str(rand.randint(1,28))
	 else:
	      day = str(rand.randint(1,30))
	 if len(str(month)) < 2:
	      # in case its 1,2,3,4,5..
	      month = "0"+str(month)
	 month = str(month) # string-tize it anyway
	 if len(day) < 2:
	      day = "0"+day
	 return "-"+month+"-"+day


def get_data():
	 pytrend = TrendReq(hl='en-US')
	 
	 # pull the keywords, and set up what to pull
	 colnames = ["keywords"]
	 df = pd.read_csv("trend_list.csv", names=colnames)
	 df.drop(df.index[[0]],inplace=True) # remove spurious "Keywords"
	 rand_index = rand.randint(0,df.shape[0]-1)
	 df = df.iloc[[rand_index]]
	 df2 = df["keywords"].values.tolist()
	 
	 # get the date to check
	 start_year = rand.randint(2005,2019)
	 end_year = str(rand.randint(start_year,2020))
	 start_year = str(start_year)
	 date1 = get_day_month()
	 date2 = get_day_month()
	 pull_range = start_year+date1+" "+end_year+date2
	 
	 # actually build the data sets
	 dataset = []
	 for x in range(0,len(df2)):
	      keywords = [df2[x]]
	      pytrend.build_payload(kw_list=keywords, cat=0, timeframe=pull_range, geo='US')
	      data = pytrend.interest_over_time()
	      if not data.empty:
	           data = data.drop(labels=['isPartial'],axis='columns')
	           dataset.append(data)
	 
	 
	 result = pd.concat(dataset, axis=1)
	 trend_word = result.columns[0]
	 trend_data = []
	 for i in range(result.shape[0]):
	      trend_data.append(result.iat[i,0]) 
	 
	 return start_year+date1,end_year+date2, trend_word, trend_data