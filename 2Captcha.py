
import requests
from selenium import webdriver
import time
import json
import re
# Step 1: Obtain the "data-s" value using Selenium
url = 'https://www.google.com/recaptcha/api2/demo'
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)  # Allowing time for the page to load

# Use Selenium to extract the value of "data-s"
# data_s_value = driver.execute_script("return YOUR_SCRIPT_TO_GET_DATA_S_VALUE")

# Step 2: Send a request to 2Captcha API with the "data-s" value and other necessary parameters
api_key = ''
site_key = ''
# Sending request to 2Captcha API
data = {
    'key': api_key,
    'method': 'userrecaptcha',
    'googlekey': site_key,
    'pageurl': url,
    # 'data-s': data_s_value,  # Including the "data-s" value
    # 'proxy': 'YOUR_PROXY',  # Replace with your proxy
    # 'cookies': 'YOUR_COOKIES'  # Replace with your cookies
}

response = requests.post('http://2captcha.com/in.php', data=data)
print(response.content)
# request_result = response.json()


pattern = r'\b\d+\b'

text = str(response.content)
matches = re.findall(pattern, text)

print(matches)
# print(request_result)
# request_result=
# if request_result['status'] == 0:
#     print(f"Error occurred: {request_result['request']} - {request_result['error']}")
# else:
#     captcha_id = request_result['request']
#     print(f"Captcha ID: {captcha_id}")
captcha_id=matches[0]  
# Step 3: Continuously check for the solution of the captcha
while True:
    captcha_result = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1').json()
    if captcha_result['status'] == 0:
        print("Captcha not yet solved. Waiting for solution...")
        time.sleep(5)
    else:
        print(f"Captcha solved: {captcha_result['request']}")
        break

driver.quit()