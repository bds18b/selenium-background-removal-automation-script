from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time


# Selenium Python Script that is used to automate background removal using Adobe's background removal tool.
# This is a free tool, so you can only do one image at a time, but this script automates the process so you don't have to.

# -----EXPECTED CRASHES-----
# 1. Script will crash if when logging in you are prompted to setup 2FA or backup email.
#    all you need to do is click no and restart the script.
#    these 2 cases typically occur consecutively and it is random.
# 2. After around 5 runs, Adobe will lock your account for around 1 hour (if the runs are within a close time period). 
#    This is because Adobe counts these as failed login attempts for some reason. 
#    You will get an error that says "Your account has been locked due to multiple failed login attempts."

# First the script will login to your account, then it will be able to remove the bg from all the images
# within a folder called 'images' within the same directory as the script. The new images with no backgrounds
# will be saved in a new (or existing) folder called 'images-with-no-bg'.

# All that is needed is an Adobe account, and that you create a forwarding filter on your email so that
# the adobe verification codes are sent to a tmail inbox. The script accesses the most recent email in the
# tmail inbox and grabs the code in order to login to the Adobe account.



# account information and variables 
adobe_email = 'seleniumbgremover@gmail.com'                                     # your adobe email
adobe_email2 = 'torytexturepacks@gmail.com'     
adobe_email3 = 'phearpvp@gmail.com'                                 
adobe_password = 'Cheese1234!'                                                  # your adobe password
inbox_link = 'https://tmail.link/inbox/denise.TORB383737duhd@tmail.link/'       # must be a tmail inbox (https://tmail.link/)
output_path = os.path.join(os.getcwd(), 'images-with-no-bg')                    # output folder path
input_path = os.path.join(os.getcwd(), 'images')                                # input folder path
os.makedirs(input_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)                        


# gets the paths of the images and stores in an array from a folder called 'images
# within the same directory as the script
file_paths = []
for root, dirs, files in os.walk(input_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)


# User Input
delete_files_user_input = input("Would you like the original images to be deleted after their background is removed? (Y/N): ")
while delete_files_user_input.upper() not in ['Y', 'N']:
    print("Invalid input. Please enter Y or N.")
    delete_files_user_input = input("Please enter your choice (Y/N): ")


# driver options and arugments
prefs = {'download.default_directory' : output_path}
chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("test-type")
chrome_options.add_experimental_option('prefs', prefs)

# create the driver and open adobe background removal tool page
driver = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
driver.get('https://express.adobe.com/tools/remove-background')
wait_time = 10

# click the login button
element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".feds-login-text")))
element.click()

# enters the email into the field and click continue
time.sleep(2)
input_field = driver.find_element("css selector", "#EmailPage-EmailField")
input_field.send_keys(adobe_email)
button = driver.find_element("css selector", "[data-id='EmailPage-ContinueButton']")
button.click()

# click continue button on verify identity page
button = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-id='Page-PrimaryButton']")))
button.click()

# allow time for the email to send
time.sleep(10)

# open a new tab to get to the verification email
driver.execute_script("window.open('about:blank', '_blank');")
driver.switch_to.window(driver.window_handles[-1])
driver.get(inbox_link)

# Click on the most recent email
list_item = driver.find_element("css selector", "ul li:first-child a")
list_item.click()


# the verification code is in an iframe, so we need to switch to that frame to access it
iframe_index = 0 
driver.switch_to.frame(iframe_index)

# Now you are inside the iframe context, you can locate the element
strong_element = driver.find_element(By.TAG_NAME, 'strong')
text_within_strong = strong_element.text

# Switch back to the default content
driver.switch_to.default_content()

# Switch back to the original tab
driver.switch_to.window(driver.window_handles[0])

# enter the code into the inputs
ctr=0
for x in text_within_strong:
    input_field = driver.find_element("css selector", f"[data-id='CodeInput-{ctr}']")
    input_field.send_keys(x)
    ctr = ctr + 1


# allow the page to load, then enter the password and press continue
time.sleep(5)
input_field = driver.find_element("css selector", "[data-id='PasswordPage-PasswordField']")
input_field.send_keys(adobe_password) 
button = driver.find_element("css selector", "[data-id='PasswordPage-ContinueButton']")
button.click()

# Loop through all images within the images file and remove their backgrounds
counter=0
for x in file_paths:
    
    counter = counter+1

    # Wait for the shadow root wrapper element to be present
    shadow_root_wrapper = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#quick-task-container > cclqt-remove-background"))
    )

    # Get the shadow root
    shadow_root = shadow_root_wrapper.shadow_root

    # Wait for the image upload area element to be visible within the shadow root
    image_upload_area = WebDriverWait(shadow_root, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "sp-theme > cclqt-workspace > cclqt-image-upload"))
    )

    # Get the inner shadow root
    inner_shadow_root = image_upload_area.shadow_root

    # upload the image
    upload_button = inner_shadow_root.find_element(By.CSS_SELECTOR, "button")
    z = inner_shadow_root.find_element(By.CSS_SELECTOR, "#file-input")
    z.send_keys(x)
     
    # access the download button and click it
    shadow_root_wrapper = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#quick-task-container > cclqt-remove-background"))
    )
    shadow_root = shadow_root_wrapper.shadow_root

   # TimeoutException
    try:
        image_upload_area = WebDriverWait(shadow_root, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "sp-theme > cclqt-workspace > cclqt-image-export"))
    )
    except:
        driver.refresh()
        # Wait for the shadow root wrapper element to be present
        shadow_root_wrapper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#quick-task-container > cclqt-remove-background"))
        )

        # Get the shadow root
        shadow_root = shadow_root_wrapper.shadow_root

        # Wait for the image upload area element to be visible within the shadow root
        image_upload_area = WebDriverWait(shadow_root, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "sp-theme > cclqt-workspace > cclqt-image-upload"))
        )

        # Get the inner shadow root
        inner_shadow_root = image_upload_area.shadow_root

        # upload the image
        upload_button = inner_shadow_root.find_element(By.CSS_SELECTOR, "button")
        z = inner_shadow_root.find_element(By.CSS_SELECTOR, "#file-input")
        z.send_keys(x)
        
        # access the download button and click it
        shadow_root_wrapper = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#quick-task-container > cclqt-remove-background"))
        )
        shadow_root = shadow_root_wrapper.shadow_root
        image_upload_area = WebDriverWait(shadow_root, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "sp-theme > cclqt-workspace > cclqt-image-export"))
        )


    shadow_root_2 = image_upload_area.shadow_root

    end = WebDriverWait(shadow_root_2, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div"))
    )
    time.sleep(10)
    x = end.find_elements(By.CSS_SELECTOR, "sp-button")
    x[1].click()


    # wait for the image to download
    # the code below waits until a new file is created within the output directory
    _, _, files = next(os.walk(output_path))
    starting_value = len(files)
    value = starting_value
    starttime = time.time()
    while starting_value == value:
        _, _, files = next(os.walk(output_path))
        value = len(files)
        time.sleep(2)

    # when image is downloaded, go back to previous page (upload page) and start loop over
    print("Image #" + str(counter) + f" of {len(file_paths)}" + " successfully downloaded!")
    if delete_files_user_input == 'Y':
        os.remove(x)
    driver.back()

driver.close()










