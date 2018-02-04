from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
class Player():

    def __init__(self):
        self.name = ""
        self.link = ""
        self.Height = ""
        self.Weight = ""
        self.pts=""

def getlist():

    driver = webdriver.Chrome(executable_path = r'D:\Programmes\chromedriver.exe')

    url = 'http://stats.nba.com/players/list/'

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    div = soup.find('div', class_= 'large-10 columns')

    player_list = []

    for a in div.find_all('a'):

        new_play = Player()
        new_play.name = a.text
        new_play.link = a['href']
        player_list.append(new_play)

    driver.quit()

    return player_list


def getdetail(player_list):

 driver = webdriver.Chrome(executable_path = r'D:\Programmes\chromedriver.exe')

 for p in player_list:

    url = 'http://stats.nba.com'+p.link
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    Height=""
    Weight=""
    Pts=""
    h_span = soup.find('div', string = 'HT')

    for span in h_span.findNextSiblings():
      Height = Height + span.text

    w_span = soup.find('div', string = 'WT')
    for span in w_span.findNextSiblings():
      Weight = Weight + span.text

    p_span = soup.find('div', string = 'PTS')
    for span in p_span.findNextSiblings():
      Pts = Pts + span.text

    p.Height = Height
    p.Weight = Weight[:3]
    p.pts=Pts

 driver.quit()

 return player_list

player_list = getdetail(getlist())

for p in player_list:
    print('\n')
    print(p.name)
    print(p.link)
    print(p.Height.replace('-','.'))
    print(p.Weight)
    print(p.pts)
    print('\n')

for p in player_list:

   p.Height=p.Height.replace('-','.')
   p.Height=p.Height.replace(" ","")
   p.Height=float(p.Height)
   p.Weight=float(p.Weight)
   p.pts=float(p.pts)

h=[]
x=[]
w=[]
for p in player_list:
    h.append(p.Height)
    w.append(p.Weight)
    x.append(p.pts)
datax={'Height':h,'Weight':w,'Pts':x}
datax=pd.DataFrame(data=datax)
sb.lmplot(data=datax,x='Height',y='Pts',hue='Weight')
plt.show()

