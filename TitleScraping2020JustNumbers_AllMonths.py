#!/usr/bin/env python3
# -*- coding: utf-8 -*

#%% Importing Libraries

# other imports
import configparser
import time
import pandas as pd
import os
import ipdb

# selenium specific imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException 

from MisspellingsList import words


#%% Initial Configuration 

# configuration parser initialization
config = configparser.ConfigParser()
config.read('./config.ini')
delay = 10 # waits for 10 seconds for the correct element to appeaar

#%% Read in File

stream_data = pd.DataFrame(columns=['Word', 'Titles', 'Unique Channels', 'Hours Watched', 'Airtime'])

#%% Login

def login_streamhatchet():
    driver.get("https://app.streamhatchet.com/")
    time.sleep(5) # sleep for 3 seconds to let the page load
    #driver.find_element_by_id("hs-eu-confirmation-button").click()

    username = driver.find_element_by_name("loginEmail")
    username.clear()
    username.send_keys(config['login_credentials']['email'])

    password = driver.find_element_by_name("loginPassword")
    password.clear()
    password.send_keys(config['login_credentials']['password'])

    driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    time.sleep(3) # sleep for 3 seconds to let the page load

#%% Stream Title Search
def stream_title_search(query):
    #driver.get("https://app.streamhatchet.com/search/toolstatus")
    driver.get("https://app.streamhatchet.com/streamtitles")
    time.sleep(1)
    
    # Enters query into 'Stream title query'
    stream_title_query_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='status-query']")))
    stream_title_query_input.send_keys(query)

    # # Makes twitch the only platform to search
    platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    platform_input.click()
    for x in range(0,13):
        platform_input.send_keys(Keys.BACKSPACE)
    # platform_input.send_keys(Keys.BACKSPACE)
    # platform_input.send_keys(Keys.BACKSPACE)

###FB
    # platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    # platform_input.click()
    # driver.find_element_by_xpath("//a[@data-value='twitch']//i[@class='delete icon']").click()
    # driver.find_element_by_xpath("//a[@data-value='ytg']//i[@class='delete icon']").click()
    # driver.find_element_by_xpath("//a[@data-value='mixer']//i[@class='delete icon']").click() 
    # for x in range(0,10):
    #     platform_input.send_keys(Keys.BACKSPACE)
    
        # Makes Youtube the only platform to search
    # platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    # platform_input.click()
    # driver.find_element_by_xpath("//a[@data-value='twitch']//i[@class='delete icon']").click()
    # #driver.find_element_by_xpath("//a[@data-value='ytg']//i[@class='delete icon']").click()
    # driver.find_element_by_xpath("//a[@data-value='mixer']//i[@class='delete icon']").click() 
    # for x in range(0,11):
    #     platform_input.send_keys(Keys.BACKSPACE)
    # # platform_input.send_keys(Keys.BACKSPACE)
    # # platform_input.send_keys(Keys.BACKSPACE)

    # Click to Expand Date Options
    driver.find_element_by_xpath("//div[@id='NewRangePicker']").click()
    
    # change the hours and minutes to 0:00 for date from and to 
    driver.find_element_by_xpath("//div[@class='calendar left']//select[@class='hourselect']//option[1]").click()
    driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'00')]").click()
    driver.find_element_by_xpath("//div[@class='calendar right']//select[@class='hourselect']//option[1]").click()
    driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'00')]").click()
    
      # Keep clicking on left_arrow
    for x in range(0,14):
        #while driver.find_element_by_xpath("//i[@id='icon-down-New']").is_displayed() == True:
        try:
            driver.find_element_by_xpath("//i[@class='fa fa-chevron-left glyphicon glyphicon-chevron-left']").click()
        except:
            break
                
     # Click on first day of the month:  
    day_one_element = driver.find_element_by_xpath("//div[@class='calendar left']//tr[1]//td[2]")
    try:
        day_one_element.click()
    except WebDriverException:
        print("First Day element is not clickable")   
    
    while driver.find_element_by_xpath("//i[@id='icon-down-New']").is_displayed() == True:
        try:
            driver.find_element_by_xpath("//i[@class='fa fa-chevron-right glyphicon glyphicon-chevron-right']").click()
        except:
            break
    
    driver.find_element_by_xpath("//div[@class='calendar left']//td[@data-title='r1c6']").click()

    # Runs the search
    driver.find_element_by_xpath("//button[@class='applyBtn btn btn-sm btn-success ui google plus button']").click()
    run_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='medium ui google plus submit button']")))
    run_button.click()
    
    # Scrape the Number of Titles
    num_titles = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-count']")))
    num_titles = num_titles.text
    #print(num_titles)
    
    unique_channels = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-uniquechannels']")))
    unique_channels = unique_channels.text
    #print(unique_channels)
    
    hours_watched = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-hourswatched']")))
    hours_watched = hours_watched.text
   # print(hours_watched)
  
    messages_airtime = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-airtime']")))
    messages_airtime = messages_airtime.text
    #print(messages_airtime) 
    
  
    # #Scrolling to bottom of page to pull table data
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # prev_num_rows = 0
    # while True:
    #     #Scroll down to bottom

    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    
    #     #Wait to load page
    #     time.sleep(4)
    #     table_rows = driver.find_elements_by_xpath("//table[@id='table_discovery']/tbody/tr")
    #     num_rows = len(table_rows)
    #     print("NUMBER OF ROWS: ---> " + str(num_rows))
    #     for i in range(prev_num_rows, num_rows):
    #         df.append(table_rows[i].text.split("\n"))
        
    #     #Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    #     prev_num_rows = num_rows
    
   # WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//table[@id='table_discovery']/tbody/tr")))

    # Pulls table data
    # table_rows = driver.find_elements_by_xpath("//table[@id='table_discovery']/tbody/tr")
    # #df = [i.text for i in table_rows]
    # ipdb.set_trace()
    # print("Number of ROWS: " + str(len(table_rows)))
    # for i in table_rows:
    #     df.append(i.text.split("\n"))
    #for 
    #print(driver.find_element_by_xpath("//table/tbody"))#.split("\n")
   
    #print(driver.find_element_by_xpath("//table/tbody").text)#.split("\n")

    #df = driver.find_element_by_id("table_discovery").text.split(",")
    #df = driver.find_element_by_xpath("//*[@id='table_discovery']").text.split("t")

    return(num_titles, unique_channels, hours_watched, messages_airtime)

#%% Run Stream Title Search

driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page
#driver = webdriver.Chrome(executable_path = /Users/caitlynedwards/desktop/python/chromedriver.exe)) #Open chrome driver so that it opens in another page

login_streamhatchet() #Log into streamhatchet

for word in words: #For each word
    print("Starting " + word) #Print so you know which line you're on
    tries = 3
    for try_num in range(tries):
        try:
            statistics = stream_title_search(word) #Run above script
        except TimeoutException:
            if try_num < tries - 1:
                continue
            else:
                statistics = ["Timed Out", "Timed Out", "Timed Out", "Timed Out", "Timed Out"]
                print("Too many Timeouts for word: {}".format(word))
        break
    #statistics = stream_title_search(word) #Run above script
    #print(range(len(table_id))[0::8])
    #for i in range(len(table_id))[0::8]: #For table of results, where [0::n], n is number of columns
    
    stream_data = stream_data.append({'Word': word,
                                      'Titles': statistics[0], #Adds unique users, streamers, and total views to data set
                                      'Unique Channels': statistics[1], 
                                      'Hours Watched': statistics[2],
                                      'Airtime': statistics[3]}, ignore_index = True)
            
                                          # 'Title': table_id[1], #Adds unique users, streamers, and total views to data set
                                          # 'Streamer': table_id[2], 
                                          # 'Date': table_id[3],
                                          # 'Hours Watched': table_id[i]}, ignore_index = True)



#%% Run Stream Title Search

# incomplete_queries_list = []
# driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page

# login_streamhatchet() #Log into streamhatchet

# for word in words: #For each word
#     print("Starting " + word) #Print so you know which line you're on
#     num_titles, table_id = stream_title_search(word, incomplete_queries_list) #Run above script
#     # ipdb.set_trace()
#     if len(table_id) == 1: #If no data
#         stream_data = stream_data.append({'Word': word,
#                                           'Titles': "None", #Adds unique users, streamers, and total views to data set
#                                           'Unique Channels': "None", 
#                                           'Hours Watched': "None",
#                                           'Airtime': 0}, ignore_index = True)
        
#     else: #If at least one stream title
#         for i in range(len(table_id)): #For table of results    
#             if (len(table_id[i]) != 7):
#                 print("BREAKING INDEX I: ---- " + str(i))
#             stream_data = stream_data.append({'Word': word,
#                                               'Stream Title': table_id[i][0], #Adds unique users, streamers, and total views to data set
#                                               'Channel': table_id[i][1], 
#                                               'Platform & Date': table_id[i][2],
#                                               'Hours Watched': table_id[i][3],
#                                               'Peak CCV': table_id[i][4],
#                                               'Avg CCV': table_id[i][5],
#                                               'Airtime Title': table_id[i][6]}, ignore_index = True)
# #%% If Stream Title Search Breaks
#driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe"))

#login_streamhatchet()

#for word in words[300:]:
 #   print("Starting " + word)
  #  num_titles, table_id = stream_title_search(word, incomplete_queries_list, df)
   # for i in range(len(table_id))[0::6]:
    #    if len(table_id) == 1:
     #       stream_data = stream_data.append({'Word': word,
      #                                        'Title': "None", #Adds unique users, streamers, and total views to data set
       #                                       'Streamer': "None", 
        #                                      'Date': "None",
         #                                     'Hours Watched': 0}, ignore_index = True)
        #else:
         #   stream_data = stream_data.append({'Word': word,
          #                                'Title': table_id[i], #Adds unique users, streamers, and total views to data set
           #                               'Streamer': table_id[i+1], 
            #                              'Date': table_id[i+2],
             #                             'Hours Watched': table_id[i+3]}, ignore_index = True)

#%% Export Data File
stream_data.to_csv('/Users/caitlynedwards/Desktop/python/StreamTitles_Twitch_HotPocket.csv', index = None, header=True)
