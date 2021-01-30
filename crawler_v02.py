from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

option = Options()
option.headless = False

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'en-US')
driver = webdriver.Firefox(options=option, firefox_profile=profile)

baseUrl = 'https://youtube.com/'

MusicTag = ['music official video', 'piano music', 'guitar music', 'violin music', 'rock music', 'electronic music', 'cover song', 'country music']
ProgrammingTag = ['datamining', 'python tutorial', 'backend', 'javascript basics', 'machine learning projects', 'php programming', 'mongodb tutorial', 'hadoop architecture']
NewsTag = ['news', 'daily news', 'sports news live', 'president', 'war economics', 'murders news', 'financial news', 'international news']
MovieTag = ['trailer', 'movie 2019', 'cartoon movie', 'top anime movies', 'science fiction movies', 'superhero movies', 'action movies', 'short films']
TravelingTag = ['traveling england', 'place must go in usa', 'visit japan', 'traveling korea', 'vacation in hawaii', 'travel vlog', 'travel blogs', 'travel blogs thailand']
BeautyTag = ['fashion and beauty', 'fashion', 'makeup tutorial', 'fashion style', 'skin care tips', 'acne skin care', 'hair care tips', 'nails']

dataset = []

def getChannelUrl(keyword):
	driver.get(f'{baseUrl}/search?q={keyword}&sp=CAASAlgD')
	time.sleep(3)
	ChannelList=driver.find_elements_by_css_selector('#text.style-scope.ytd-channel-name.complex-string a.yt-simple-endpoint.style-scope.yt-formatted-string')
	ChannelLinkList = list(dict.fromkeys(map(lambda a: a.get_attribute('href'), ChannelList)))
	return (ChannelLinkList)

def getVideoUrl(ChannelLinkList):
	VideoLinkList = []
	for url in ChannelLinkList:
		driver.get(f'{url}/videos')
		VideoList=driver.find_elements_by_css_selector('#video-title.yt-simple-endpoint.style-scope.ytd-grid-video-renderer')
		VideoLink = list(dict.fromkeys(map(lambda a: a.get_attribute('href'), VideoList)))
		VideoLinkList.extend(VideoLink)
	return VideoLinkList

def getVideoDetail(VideoLinkList, tag):
	for url in VideoLinkList:
		driver.get(url)
		try:
			Title = driver.find_element_by_xpath('//ytd-video-primary-info-renderer/div/h1/yt-formatted-string').text
			View = driver.find_element_by_xpath('//ytd-video-primary-info-renderer/div/div/div[1]/div[1]/yt-view-count-renderer/span[1]').text
			Like = driver.find_elements_by_css_selector('#text.style-scope.ytd-toggle-button-renderer.style-text')[0].text
			Dislike = driver.find_elements_by_css_selector('#text.style-scope.ytd-toggle-button-renderer.style-text')[1].text
			Detail = {
				'Title': Title,
				'View': View,
				'Like': Like,
				'Dislike': Dislike,
				'Category': tag
			}
			print(Detail)
			dataset.append(Detail)
		except: #NoSuchElementException:
			pass

def unique(list1): 
    unique_list = [] 
    for x in list1:  
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

MusicChannelLinkList = []
for keyword in MusicTag:
	try:
		ChannelLinkList = getChannelUrl(keyword)
		MusicChannelLinkList.extend(ChannelLinkList)
	except:
		pass
try:
	MusicVideoLinkList = getVideoUrl(unique(MusicChannelLinkList))
	getVideoDetail(MusicVideoLinkList, 'Music')
except:
	pass

ProgrammingChannelLinkList = []
for keyword in ProgrammingTag:
	try: 
		ChannelLinkList = getChannelUrl(keyword)
		ProgrammingChannelLinkList.extend(ChannelLinkList)
	except:
		pass
try:
	ProgrammingVideoLinkList = getVideoUrl(unique(ProgrammingChannelLinkList))
	getVideoDetail(ProgrammingVideoLinkList, 'Programming')
except:
	pass

NewsChannelLinkList = []
for keyword in NewsTag:
	try:
		ChannelLinkList = getChannelUrl(keyword)
		NewsChannelLinkList.extend(ChannelLinkList)
	except:
		pass
try:
	NewsVideoLinkList = getVideoUrl(unique(NewsChannelLinkList))
	getVideoDetail(NewsVideoLinkList, 'News')
except:
	pass

MovieChannelLinkList = []
for keyword in MovieTag:
	try:
		ChannelLinkList = getChannelUrl(keyword)
		MovieChannelLinkList.extend(ChannelLinkList)
	except:
		pass
try:
	MovieVideoLinkList = getVideoUrl(unique(MovieChannelLinkList))
	getVideoDetail(MovieVideoLinkList, 'Movie')
except:
	pass

TravelingChannelLinkList = []
for keyword in TravelingTag:
	try:
		ChannelLinkList = getChannelUrl(keyword)
		TravelingChannelLinkList.extend(ChannelLinkList)
	except:
		pass
try:
	TravelingVideoLinkList = getVideoUrl(unique(TravelingChannelLinkList))
	getVideoDetail(TravelingVideoLinkList, 'Traveling')
except:
	pass

BeautyChannelLinkList = []
for keyword in BeautyTag:
	try:
		ChannelLinkList = getChannelUrl(keyword)
		BeautyChannelLinkList.extend(ChannelLinkList)
	except:
		pass
try:
	BeautyVideoLinkList = getVideoUrl(unique(BeautyChannelLinkList))
	getVideoDetail(BeautyVideoLinkList, 'Beauty')
except:
	pass

print('dataset', dataset)
data = pd.DataFrame(dataset)
data.to_csv('data_02.csv', index = False)
driver.close()