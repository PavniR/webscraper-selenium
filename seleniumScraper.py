from selenium import webdriver   #allow launching browser
from selenium.webdriver.common.by import By     #allow search with parameters 
from selenium.webdriver.support.ui import WebDriverWait   #allow waiting for page to load 
from selenium.webdriver.support import expected_conditions as EC   #determine whether the page has loaded 
from selenium.common.exceptions import TimeoutException #handling timeout situation 
import pandas 


#driver_setting = webdriver.ChromeOptions()       #creates new broswer window SETTING 
#driver_setting.add_argument("--incognito")       #opens in incognito mode, passing the argument to setting


#browser = webdriver.Chrome(options=driver_setting)  #webdriver.chrome creates new browser with option argument and named browser 
browser = webdriver.Chrome()
browser.get("https://github.com/collections/machine-learning")   #opens github in incognito

print("site opened", browser.title)

try:
    WebDriverWait(browser, 40).until(
        EC.presence_of_all_elements_located((By.XPATH, "//h1[@class='h3 lh-condensed']"))
    )
    print("page loaded!")
except:
    print("couldn't load page in time")

projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")
#this will store each h1 element and their children tags in list

#now we fetch url and project name from this list
projects_list = []    #empty list to store dictionaries of project and url (key:value pairs)

for repo in projects:
    project_name = repo.text.strip()
    project_url = repo.find_elements(By.XPATH, "a")[0].get_attribute('href')
    projects_list.append({                        #adding each dict as list item to list
        "Project Name": project_name,
        "URL": project_url
    })

#print(browser.page_source)
#closing the connection 
browser.quit()

#converts dictionary items to a list of tuples and each tuple becomes a row, then we name how columns should be recognised 
data = pandas.DataFrame(projects_list)
#DataFrame arranges data in tabular form 
data.columns = ['project_url', 'project_name'] #identifying the columns of dataframe

#print(data) 

#exporting to CSV file
data.index += 1  #index starts from 0, this initialises it from 1 for our "data" table
data.to_csv("best_projects.csv", index_label="s.no.")

#print(projects_dict)  to check if it is retrieving the info
