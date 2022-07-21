from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import pandas as pd

driver = webdriver.Firefox(executable_path=r'C:\Users\abhis\OneDrive\Desktop\scrapping_python\linkedin_scarp\geckodriver.exe')
driver.get("https://www.linkedin.com")

user_box = driver.find_element(By.NAME,"session_key")
user_box.send_keys("abhishekbiswas772@gmail.com")

user_pass = driver.find_element(By.NAME, "session_password")
user_pass.send_keys("194dcf8606305e7ac14cded073506f2b682d353ff893584a8dc23aacd94c10c6")

login_pass = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button")
login_pass.click()

print("Done")


link_arr = []
anch = driver.find_elements(By.TAG_NAME, "a")
for i in anch:
    link_arr.append(i.get_attribute('href'))
# print(link_arr)

job_main_link = ""
for i in link_arr:
    urlP = urlparse(i)
#     print(urlP)
    if urlP.path == '/jobs/':
        job_main_link += 'https://www.linkedin.com/' + str(urlP.path)
# print(job_main_link)

driver.get(job_main_link)

names_jobs = driver.find_elements(By.CSS_SELECTOR, '.ember-view.job-card-container__link.job-card-list__title')
job_names = []
for i in names_jobs:
    i = i.get_attribute("text").strip()
    job_names.append(i)
    
print(len(job_names))

role_jobs = driver.find_elements(By.XPATH, "//span[@class='job-card-container__primary-description']/a[@class='app-aware-link']")
role_names = []
for i in role_jobs:
    i = i.get_attribute("text")
    role_names.append(i)
    
print(len(role_names))

place_jobs = driver.find_elements(By.CSS_SELECTOR, 'li.job-card-container__metadata-item')
place_names = []
for i in place_jobs:
    i = i.get_attribute("innerHTML")
    i = i.strip()
    i = i.split("<!---->")
    place_names.append(i)
    
place = []
res_place = []
for i in range(0, len(place_names)):
    for j in range(0, len(place_names[i])):
        place.append(place_names[i][j])
        
for ele in place:
    if ele.strip():
        res_place.append(ele) 
        
print(len(res_place))

time_drive = driver.find_elements(By.CLASS_NAME, 'job-card-container__footer-item')
time_arr = []
for i in time_drive:
    i = i.get_attribute("innerHTML").strip().split("\n")
    time_arr.append(i)
# print(len(time_arr))
ftime = []
for i in range(0, len(time_arr)):
    if len(time_arr[i]) == 3:
        ftime.append(time_arr[i])

months_time = []
for i in range(0, len(ftime)):
    j = ftime[i][1].strip()
#     print(j)
    months_time.append(j)
    
print(len(months_time))


col = ["Company Name", "Job Position", "Location", "Job Posting Date"]
data = pd.DataFrame({"Company Name": role_names, "Job Position": job_names, "Location": res_place, "Job Posting Date": pd.Series(months_time)})

data.to_csv("linkedIn_Scraped_Jobs.csv")