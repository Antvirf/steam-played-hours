#-*- coding: utf-8 -*-

'''
Made on 20th March 2017. Zero guarantee it will work afterwards; may break if/when steam
changes their webpage.
Requires requests, bs4 and json modules for main functionality
Requires numpy and matplotlib for plots
'''

import requests, bs4, json

username = str(input('Please enter your steam username: '))
savepath = str(input('Please enter path to save output file: '))
page = requests.get('http://steamcommunity.com/id/'+username+'/games/?tab=all')
games = bs4.BeautifulSoup(page.text, 'lxml').select('script')
games = games[12].getText()

Done = False
for i in range(len(games)):
    if (games[i] == '[') and (not Done):
        startindex = i
        Done = True
    if (games[i] == ']'):
        if (games[i+1] == ';'):
            endindex = i
            break
jscript = json.loads(games[startindex:endindex+1])


labels= []
hours = []
for i in range(len(jscript)):
    labels.append(jscript[i]['name'])
    try:
        hours.append(float(jscript[i]['hours_forever'].replace(",", "")))
    except:
        hours.append(float(0)) #If hours played doesn't exist, it's 0


# Plotting stuff
def plot(data):
    import matplotlib.pyplot as plt
    import numpy as np
    ind = np.arange(len(data))
    width = 0.35
    fig, ax = plt.subplots()
    hrgraph = ax.bar(ind, data, width)
    plt.show()

# Txt export for ez copypaste to excel
def export(data, labels, path):
    text='ID\tGame\tHours\n'
    for i in range(len(labels)):
        text+=str(1+i)+'\t'+labels[i]+'\t'+str(data[i])+'\n'
    file = open(path+'out.txt', 'w')
    file.write(text)
    file.close()


export(hours, labels, savepath)
