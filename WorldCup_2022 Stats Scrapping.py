from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import pandas as pd

#Function to click the cache and cookies pop up, so we can access the page
def accept_cookies(driver_object):
    """
    locates and presses cookies 'I Accept'
    """
    #Sleep for 7 second for the page load
    time.sleep(7)
    cookies_button_xpath = '//button[ @id="onetrust-accept-btn-handler"]'#the accept cookies button
    accept_cookies_button = driver_object.find_element(By.XPATH, cookies_button_xpath)
    accept_cookies_button.click()

def animate_scroll (driver_object):
    """
    Scroll the web page down.
    """
    for i in range (4):
        time.sleep(1)
        driver_object.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)# scroll down

def extract_data (driver_object):
    match_kind = driver_object.find_element(By.XPATH,'//p[@class="ff-m-0 ff-p-0"]').text.replace('•','') #return text ,access directly the page tag <p
    date_time = driver_object.find_element(By.XPATH,'//p[@class="ff-p-0"]').text.replace('•','-') #return text ,access directly the page tag <p
    first_team = driver_object.find_element(By.XPATH,'//div[@class="match-score_TeamName__519Ix text-align-end justify-content-end ff-m-0 ff-mr-16 ff-my-8 ff-mr-md-8"]').text
    second_team = driver_object.find_element(By.XPATH,'//div[@class="match-score_TeamName__519Ix ff-m-0 ff-ml-16 ff-my-8 ff-ml-md-8"]').text
    score_first_team = driver_object.find_element(By.XPATH,'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]').text
    score_second_team = driver_object.find_element(By.XPATH,'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[2]/div[4]/div[1]/div[2]/div[3]').text

# General Infromation
    first_team_posession = driver_object.find_element(By.XPATH, '//div[@class="single-stat-possession-component_StatText__DfCey single-stat-possession-component_Left__n8x91"]').text
    second_team_possession = driver_object.find_element(By.XPATH, '//div[@class="single-stat-possession-component_StatText__DfCey single-stat-possession-component_Right__Xljbj"]').text
    other_metrices_divs = driver_object.find_elements(By.XPATH, '//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]')
    pk = f'{match_kind}{first_team}{second_team}'.replace(' ', '').replace('-', '').lower()
    print(f"fetching {match_kind} {first_team} vs {second_team}")
    general_info = [
        pk,
        match_kind,
        date_time,
        first_team,
        second_team,
        score_first_team,
        score_second_team,
        first_team_posession,
        second_team_possession
    ]
#Stats Infromation
    match_stats = []
    for i in range(1,5):
        if i == 1 :
            category_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[2]/div[3] /p' 
            category = driver_object.find_element(By.XPATH,category_xpath).text
            for j in range (1,6):
                metric_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[2]/div[4]/div[{j}]/div[1]'
                metric = driver_object.find_element(By.XPATH,metric_xpath).text
                first_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[2]/div[4]/div[{j}]/div[2]/div[1]'
                first_team_metric_values = driver_object.find_element(By.XPATH, first_team_metric_values_xpath).text
                second_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[2]/div[4]/div[{j}]/div[2]/div[3]'
                second_team_metric_values = driver_object.find_element(By.XPATH, second_team_metric_values_xpath).text
                mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
                match_stats.append([
                    mpk,
                    pk,
                    category,
                    metric,
                    first_team_metric_values,
                    second_team_metric_values
                ])
        elif 1<i<4 :
            category_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[{i+1}]/div[1] /p' 
            category = driver_object.find_element(By.XPATH,category_xpath).text
            for j in range (1,6):
                metric_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[{i+1}]/div[2]/div[{j}]/div[1]'
                metric = driver_object.find_element(By.XPATH,metric_xpath).text
                first_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[{i+1}]/div[2]/div[{j}]/div[2]/div[1]'
                first_team_metric_values = driver_object.find_element(By.XPATH, first_team_metric_values_xpath).text
                second_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[{i+1}]/div[2]/div[{j}]/div[2]/div[3]'
                second_team_metric_values = driver_object.find_element(By.XPATH, second_team_metric_values_xpath).text
                mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
                match_stats.append([
                    mpk,
                    pk,
                    category,
                    metric,
                    first_team_metric_values,
                    second_team_metric_values
                ])
        else :
            category_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[9]/div[1] /p' 
            category = driver_object.find_element(By.XPATH,category_xpath).text
            for j in range (1,6):
                metric_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[9]/div[2]/div[{j}]/div[1]'
                metric = driver_object.find_element(By.XPATH,metric_xpath).text
                first_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[9]/div[2]/div[{j}]/div[2]/div[1]'
                first_team_metric_values = driver_object.find_element(By.XPATH, first_team_metric_values_xpath).text
                second_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[9]/div[2]/div[{j}]/div[2]/div[3]'
                second_team_metric_values = driver_object.find_element(By.XPATH, second_team_metric_values_xpath).text
                mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
                match_stats.append([
                    mpk,
                    pk,
                    category,
                    metric,
                    first_team_metric_values,
                    second_team_metric_values
                ])

    #Set Plays 
    category_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[10]/div[1] /p' 
    category = driver_object.find_element(By.XPATH,category_xpath).text
    for j in range (1,4):
        metric_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[10]/div[2]/div[{j}]/div[1]'
        metric = driver_object.find_element(By.XPATH,metric_xpath).text
        first_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[10]/div[2]/div[{j}]/div[2]/div[1]'
        first_team_metric_values = driver_object.find_element(By.XPATH, first_team_metric_values_xpath).text
        second_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[10]/div[2]/div[{j}]/div[2]/div[3]'
        second_team_metric_values = driver_object.find_element(By.XPATH, second_team_metric_values_xpath).text
        #mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
        mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
        match_stats.append([
            mpk,
            pk,
            category,
            metric,
            first_team_metric_values,
            second_team_metric_values
        ])

    #Defending    
    category_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[11]/div[1] /p' 
    category = driver_object.find_element(By.XPATH,category_xpath).text
    for j in range (1,5):
        metric_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[11]/div[2]/div[{j}]/div[1]'
        metric = driver_object.find_element(By.XPATH,metric_xpath).text
        first_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[11]/div[2]/div[{j}]/div[2]/div[1]'
        first_team_metric_values = driver_object.find_element(By.XPATH, first_team_metric_values_xpath).text
        second_team_metric_values_xpath = f'//div[@class="match-details-statistic-tab-component_container__+l3df ff-mt-24 ff-mt-md-32 ff-mt-lg-48 ff-mt-xl-56"]/div[1]/div[11]/div[2]/div[{j}]/div[2]/div[3]'
        second_team_metric_values = driver_object.find_element(By.XPATH, second_team_metric_values_xpath).text
        mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
        match_stats.append([
            mpk,
            pk,
            category,
            metric,
            first_team_metric_values,
            second_team_metric_values
        ])                                                                     
    print(f"general info : {general_info}")
    print(f"match stats : {match_stats}")
    print(f"match len stats : {len(other_metrices_divs)}")

    return general_info, match_stats

#1. To get all hyperlink of all matches
website = 'https://www.fifa.com/en/tournaments/mens/worldcup/qatar2022/scores-fixtures?country=ID&wtw-filter=ALL'
options = Options()
options.add_experimental_option("detach", True)
driver1 = webdriver.Chrome(options=options)
driver1.get(website)
accept_cookies(driver_object=driver1)
anchor_xpath = '//div[@ class="match-block_wtwOuterMatchBlock__u+Qfu"]/a'#link for every stats of match total 64 links (64 matches)
anchor_elements = driver1.find_elements(By.XPATH, anchor_xpath)

all_h_links = []
for a_e in anchor_elements:
    hlink = a_e.get_attribute('href')#every anchor element convert into link
    all_h_links.append(hlink)
print(len(all_h_links))
print(all_h_links)

animate_scroll(driver_object=driver1)
driver1.quit()

#2. Loop every link and get all statistics
all_matches_general_info = []
all_matches_stats = []
for hlink in all_h_links:
    driver2 = webdriver.Chrome(options=options)
    driver2.get(hlink)
    accept_cookies(driver2)
    stats_tab_xpath = '//div[@class="rail_childContainer__k-6B0 match-details-new-tabs-component_tabsContainer__Gv+i6"]/div[4]'
    stats_tab = driver2.find_element(By.XPATH, stats_tab_xpath)
    stats_tab.click()
    animate_scroll(driver_object=driver2)
    general_info, match_stats = extract_data(driver_object=driver2)
    all_matches_general_info.append(general_info)
    all_matches_stats = all_matches_stats+match_stats
    driver2.quit()

matches_cols = [
        'id',
        'match_kind',
        'date_time',
        'first_team',
        'second_team',
        'first_team_score',
        'second_team_score',
        'first_team_posession',
        'second_team_possession'
    ]
stats_cols = [
    'id',
    'match_id',
    'category',
    'metric',
    'first_team_metric_values',
    'second_team_metric_values',
]

#3. Insert all data to csv file
matches = pd.DataFrame(all_matches_general_info, columns=matches_cols)
print(matches.head())
matches.to_csv('data/matches.csv', index=False)
stats = pd.DataFrame(all_matches_stats, columns=stats_cols)
stats.to_csv('data/stats.csv', index=False)
print(stats.head())