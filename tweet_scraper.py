import time
import datetime
import snscrape.modules.twitter as sntwitter
import numpy as np
import pandas as pd
import re
from konlpy.tag import Okt

okt = Okt()

# Generate dates list
def generate_dates(year, date_only):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dates_list = []
    dates_tuple = []

    for i in range(len(days)):
        month = i+1
        for j in range(days[i]):
            day = j+1
            date = str(year) + '-' + str(month) + '-' + str(day)
            dates_list.append(date)
            dates_tuple.append([year, month, day])

    if date_only: 
        return dates_list
    else:
        return dates_tuple

# Generate integer unix time list
def generate_times(start_time, end_time, duration):
    start_unix = int(time.mktime(start_time.timetuple()))
    end_unix = int(time.mktime(end_time.timetuple()))

    list_time = np.arange(start_unix, end_unix, duration).tolist()

    #list_time = []

    #for t in range(start_unix, end_unix):
    #    list_time.append(t)

    return list_time

# Scrape data and locate them in respective folders
def scrape_data_tmp(lang, dates_list):
    tweet_directory = 'collected_tweets/' + lang + '/'
    tweet_df = pd.DataFrame(columns=["DateTime", "Text"])

    for i in range(len(dates_list)-1):
        file_name = tweet_directory + lang + '_' + dates_list[i]
        search_quote = '\s since:' + dates_list[i] + ' until:' + dates_list[i+1] + ' filter:safe lang:' + lang

        cur_file = open(file_name + '.txt', 'w')

        for tweet in (sntwitter.TwitterSearchScraper(search_quote).get_items()):
            cur_file.write(str(tweet.date) + "\t" + tweet.content + "\n")
            tweet_df.loc[len(tweet_df)] = [tweet.date, tweet.content]

        cur_file.close()

        tweet_df.to_csv(file_name+ '.csv', index=False, encoding='utf8')
        tweet_df = tweet_df.head(0)

# Scrape data and locate them in respective folders
def scrape_data(lang, list_time):
    tweet_directory = 'collected_tweets/' + lang + '/'
    tweet_df = pd.DataFrame(columns=["DateTime", "Text"])
    file_name = ''

    for i in range(len(list_time)-1):    
        if (i % 86400 == 0):
            if (i != 0):
                cur_file.close()

                tweet_df.to_csv(tweet_directory + 'csv/' + file_name + '.csv', index=False, encoding='utf8')
                tweet_df = tweet_df.head(0)

            date = datetime.datetime.fromtimestamp(list_time[i]).strftime('%Y-%m-%d')
            file_name = lang + '_' + date

            cur_file = open(tweet_directory + 'txt/' + file_name + '.txt', 'w')
            print("Opening file for " + date)

        search_quote = '\s since_time:' + str(list_time[i]) + ' until_time:' + str(list_time[i+1]) + ' filter:safe lang:' + lang

        for tweet in (sntwitter.TwitterSearchScraper(search_quote).get_items()):
            print("\t" + tweet.rawContent)
            cur_file.write(str(tweet.date) + "\t" + tweet.rawContent + "\n")
            tweet_df.loc[len(tweet_df)] = [tweet.date, tweet.rawContent]
            break

        #cur_file.close()

        #tweet_df.to_csv(tweet_directory + 'csv/' + file_name + '.csv', index=False, encoding='utf8')
        #tweet_df = tweet_df.head(0)

def basic_cleaning(tweet):
    tweet = re.sub('@[^\s]+', '', tweet)    # Remove people tags
    tweet = re.sub('#[^\s]+', '', tweet)    # Remove hash tags
    tweet = re.sub('http[^\s]+', '', tweet)    # Remove web address

    return tweet

def ko_cleaning(tweet):
    tweet = re.findall('[ㄱ-ㅎㅏ-ㅣ가-힣]+', tweet)   # Remove non-korean
    tweet = " ".join(tweet)
    
    morphs = okt.morphs(tweet, norm=True, stem=True)

    return morphs

def process_csv(lang, date):
    tweet_directory = 'collected_tweets/' + lang + '/'
    filename = tweet_directory + 'csv/' + lang + '_' + date + '.csv'
    processed_file = tweet_directory + 'processed/' + lang + '_' + date + '.csv'

    tweet_df = pd.read_csv(filename, names=["DateTime", "Text"], lineterminator='\n')

    tweet_df['Text'] = tweet_df['Text'].apply(basic_cleaning)
    tweet_df['Popped Text'] = tweet_df['Text'].apply(ko_cleaning)

    tweet_df.to_csv(processed_file, index=False, encoding='utf8')

#dates_list = generate_dates(2019)
#dates_list.append('2020-1-1')

start_time = datetime.datetime(2019, 1, 1, 0, 0) 
end_time = datetime.datetime(2020, 1, 1, 0, 0)

list_time = generate_times(start_time, end_time, 5)
print("Time list generated")

scrape_data('en', list_time)

#half_point = int(len(dates_list) / 2)
#new_list = dates_list[half_point:]

#scrape_data('en', new_list)

#process_csv('ko', '2019-12-31')

#for i in range(len(dates_list)-1):
#    process_csv('ko', dates_list[i])
