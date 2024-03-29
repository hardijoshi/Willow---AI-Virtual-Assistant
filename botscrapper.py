from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver. common.by import By
import warnings
from selenium.webdriver.chrome. service import Service
from selenium. common. exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings. simplefilter("ignore")
url = f'https://cdn.botpress.cloud/webchat/v1/index.html?options=%7B%22config%22%3A%7B%22composerPlaceholder%22%3A%22Talk%20to%20Willow%22%2C%22botConversationDescription%22%3A%22Willow%20-%20Virtual%20Assistant%22%2C%22botId%22%3A%22704d11b2-af6b-4cf4-b87d-79df1dd2a255%22%2C%22hostUrl%22%3A%22https%3A%2F%2Fcdn.botpress.cloud%2Fwebchat%2Fv1%22%2C%22messagingUrl%22%3A%22https%3A%2F%2Fmessaging.botpress.cloud%22%2C%22clientId%22%3A%22704d11b2-af6b-4cf4-b87d-79df1dd2a255%22%2C%22webhookId%22%3A%22bb8de174-f7d8-4de4-a6b8-17807b37795f%22%2C%22lazySocket%22%3Atrue%2C%22themeName%22%3A%22prism%22%2C%22botName%22%3A%22Willow%20-%20Virtual%20Assistant%22%2C%22stylesheet%22%3A%22https%3A%2F%2Fwebchat-styler-css.botpress.app%2Fprod%2F273f0563-bca9-4dde-a9e4-347bf38e6be8%2Fv29652%2Fstyle.css%22%2C%22frontendVersion%22%3A%22v1%22%2C%22useSessionStorage%22%3Atrue%2C%22enableConversationDeletion%22%3Atrue%2C%22theme%22%3A%22prism%22%2C%22themeColor%22%3A%22%232563eb%22%2C%22chatId%22%3A%22bp-web-widget%22%2C%22encryptionKey%22%3A%22cSY1Y93aJomBvTulx0zuLAat4YgYVw6p%22%7D%7D'

chrome_driver_path = 'C:\\Users\\db2ha\\Chatbot\\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument('--log-level=3') # Set Chrome Log Level
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get(url)
sleep(3)

# chatnumber = 1

def wait_for_element(by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def click_on_chat_button():
    button = driver.find_element(By.XPATH, '/html/body/div/div/button').click()
    sleep(2)
    while True:
        try:
            loader = driver.find_element(
                By.CLASS_NAME, 'bpw-msg-list-loading')
            is_visible = loader.is_displayed()
            print('Initializing Willow ... ')

            if not is_visible:
                break
            else:
                pass
        except NoSuchElementException:
            print('Willow is Initializing.')
            break
        sleep(1)

def sendQuery(text):
# Find and interact with the textarea element
    textarea = driver.find_element(By. ID, 'input-message')
    textarea.send_keys(text)
    sleep(1)

    send_btn = driver.find_element(By.ID, 'btn-send').click()
    sleep(1)

def isBubbleLoadervisible():
    print('Willow Is Typing ... ')
    while True:
        try:
            bubble_loader = driver.find_element(
                By.CLASS_NAME, 'bpw-typing-group')
            is_visible = bubble_loader.is_displayed()

            if not is_visible:
                break
            else:
                pass
        except NoSuchElementException:
            print('Willow Is Sending Mesage ... ')
            break
        sleep(1)

chatnumber = 2



def retrieveData():
    print('Retrieving Chat ... ')
    global chatnumber
    sleep(1)
    xpath = f'/html/body/div/div/div/div[2]/div[1]/div/div/div[{chatnumber}]/div/div[2]/div/div/div/div/div/p'
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    print("\nWillow: " + element.text)
    chatnumber += 2
    return element.text

click_on_chat_button()  # Assuming this starts the chat session

# Send query
# while True:
#     query = input('\n You: ')
#     sendQuery(query)

# Retrieve and print response
    # response = retrieveData()
# if response is not None:
#     print("Response received:", response)
# else:
#     print("No response received.")
