# -*- coding: utf-8 -*-

"""
Author: Noah Becker
Date: February 17th, 2020
Subject: Causal Inference
Description: Data Scraping
"""

import numpy as np
import pandas as pd
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_event(url, gender, distance, stroke, lanes):
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r)

    names = soup.find_all('tr')

    labels = []
    data = []

    for h in names[0].find_all(['th', 'td']):
        labels.append(h.get_text().strip().replace('\t', '').replace('\n', '').replace('\r\r', ' ').replace('\r', ' '))

    for swimmer in names[1:]:
        swimmer_list = []

        for s in swimmer.find_all(['td', 'th']):
            s_str = s.get_text().strip()

            if s_str.isnumeric():
                swimmer_list.append(float(s_str))
            elif s_str == '':
                swimmer_list.append(np.NaN)
            else:
                swimmer_list.append(s_str)

        data.append(swimmer_list)

    df = pd.DataFrame(data, columns=labels)
    
    df['Gender'] = gender
    df['Distance'] = float(distance)
    df['Stroke'] = stroke
    df['Lanes'] = float(lanes)

    df[['Finals Heat', 'Finals Lane']] = df['Finals HT/LN'].str.split('/', expand=True)
    
    df[['Prelims Heat', 'Prelims Lane']] = df['Prelims HT/LN'].str.split('/', expand=True)

    df = df.dropna(subset=['Finals Pl'])
    
    if 'Club' in df.columns:
        df = df.rename(columns = {'Club':'School'})
        
    return df

df = pd.DataFrame(columns=['Swimmer', 'Gender', 'Stroke', 'Distance', 'Prelims Time', 'Finals Time', 'Finals Lane', 'Lanes', 'School', 'Seed Time', 'Prelims Lane', 'Prelims Heat', 'Finals Heat', 'Prelims Pl', 'Finals Pl', 'Pts'])

# 2019 Big 8 Swimming Championships (Apr 18-20)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289527&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289528&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289531&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289532&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289533&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289534&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289543&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11370&meid=289544&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2019 South Coast Conference Swim and Dive Championships (Apr 18-20)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289356&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289357&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289360&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289361&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289362&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289363&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289372&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11366&meid=289373&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2019 Orange Empire Conference Champs (Apr 18-20)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289452&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289453&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289436&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289437&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289440&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289441&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289442&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11368&meid=289443&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')

# 2019 Western States Conference Championships (Apr 18-20)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289316&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289317&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289320&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289321&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289322&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289323&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289332&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11365&meid=289333&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2019 Coast Conference Championships (Apr 18-20)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310003&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310004&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310007&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310008&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310009&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310010&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310019&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11938&meid=310020&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2019 Pacific Coast Athletic Conference Championships (Apr 18-20)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289396&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289397&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289400&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289401&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289402&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289403&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289412&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=11367&meid=289413&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 CCCAA Swim & Drive State Championships (May 3-5)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252657&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252658&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252661&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252662&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252663&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252664&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252673&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10093&meid=252674&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 Bay Valley Conference Championships (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252743&e=23&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252744&e=24&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252747&e=27&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252748&e=28&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252749&e=29&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252750&e=30&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252761&e=41&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10095&meid=252762&e=42&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 Big 8 Swimming Championships (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255765&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255766&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255769&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255770&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255771&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255772&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255781&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10169&meid=255782&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 Coast Conference Championships (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252785&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252786&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252789&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252790&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252791&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252792&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252801&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10096&meid=252802&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 Orange Empire Conference Champs (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252825&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252826&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252829&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252830&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252831&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252832&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252841&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10097&meid=252842&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 Pacific Coast Athletic Conference Championships (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252865&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252866&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252869&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252870&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252871&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252872&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252881&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10098&meid=252882&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 South Coast Conference Swim and Dive Championships (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252905&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252906&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252909&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252910&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252911&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252912&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252921&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10099&meid=252922&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2018 Western States Conference Championships (Apr 19-21)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252945&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252946&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252949&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252950&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252951&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252952&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252961&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=10100&meid=252962&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 CCCAA Swim & Dive State Championships (May 4-6)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231483&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231484&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231487&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231488&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231489&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231490&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231499&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9070&meid=231500&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 Central Valley Conference Championships (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230405&e=23&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230406&e=24&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230409&e=27&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230410&e=28&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230411&e=29&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230412&e=30&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230423&e=41&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9042&meid=230424&e=42&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 Coast Conference Championships (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211360&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211361&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211364&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211365&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211366&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211367&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211376&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8525&meid=211377&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 South Coast Conference Swim and Dive Championships (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231849&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231850&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231853&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231854&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231855&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231856&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231865&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9079&meid=231866&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 Western States Conference Championships (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230056&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230057&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230060&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230061&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230062&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230063&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230072&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9033&meid=230073&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 Big 8 Championships (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217883&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217884&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217887&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217888&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217889&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217890&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217899&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8693&meid=217900&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 Orange Empire Conference Champs (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211870&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211871&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211874&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211875&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211876&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211877&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211886&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=8548&meid=211887&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# 2017 Pacific Coast Athletic Conference Championships (Apr 20-22)
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230551&e=17&s=finals', 'F', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230552&e=18&s=finals', 'M', 100, 'Fly', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230555&e=21&s=finals', 'F', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230556&e=22&s=finals', 'M', 100, 'Breast', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230557&e=23&s=finals', 'F', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230558&e=24&s=finals', 'M', 100, 'Back', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230567&e=33&s=finals', 'F', 100, 'Free', 8)], join='inner')
df = pd.concat([df, scrape_event('https://www.swimphone.com/meets/event_results.cfm?smid=9045&meid=230568&e=34&s=finals', 'M', 100, 'Free', 8)], join='inner')

# df = pd.concat([df, scrape_event('', '', 100, '', 8)], join='inner')

df['Lane'] = np.NaN
df.loc[(df['Finals Lane'] == '4') | (df['Finals Lane'] == '5'), 'Lane'] = 'Inside'
df.loc[(df['Finals Lane'] == '1') | (df['Finals Lane'] == '8'), 'Lane'] = 'Outside'

df.to_csv('swim.csv', index = False)
