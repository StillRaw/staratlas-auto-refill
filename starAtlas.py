import os
import time
import shutil
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def chrome_driver():
    """Chromedriver starts by using webdriver-manager."""
    global driver
    global username
    global main_path

    main_path =os.getcwd()
    username = getpass.getuser()
    directory = f"C:/Users/{username}/Desktop/iskur/webdriverSetup/"
    os.chdir(directory)

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_argument(
        f'--user-data-dir=C:/Users/{username}/AppData/Local/Google/Chrome/User Data/A-Selenium')
    chrome_options.add_argument('--profile-directory=automate-staratlas')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

def copy_files_folders():
    """To use your default profile we have to clone it.
    We copy folders and files if it is the first time."""
    try:
        directory = f"C:\\Users\\{username}\AppData\Local\\Google\\Chrome\\User Data\\A-Selenium\\automate-staratlas"
        directory_list = os.listdir(directory)

        if 'Local Extension Settings' not in directory_list:

            user_data_dir = f"C:\\Users\\{username}\AppData\Local\\Google\\Chrome\\User Data"
            source_LES = f"Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"
            destination_LES = f"A-Selenium\\automate-staratlas\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"

            files = ['Extension Cookies',
                     'Extension Cookies-journal', 'Secure Preferences']

            for i in files:
                source_default = f'{user_data_dir}\\Default'
                source_staratlas = f'{user_data_dir}\\A-Selenium\\automate-staratlas'

                shutil.copy(f'{source_default}\\{i}',
                            f'{source_staratlas}\\{i}')

                print(f'{source_default}\\{i}')
                print(f'{i} copied!')

            shutil.copytree(f'{user_data_dir}\\Default\\Extensions\\bfnaelmomeimhlpmgjnjophhpkkoljpa',
                            f'{user_data_dir}\\A-Selenium\\automate-staratlas\\Extensions\\bfnaelmomeimhlpmgjnjophhpkkoljpa')

            shutil.copytree(f'{user_data_dir}\\{source_LES}',
                            f'{user_data_dir}\\{destination_LES}')

    except:
        print('Folders and files cannot clone.')

def enter_fleet():
    # Enter Fleet page.
    link = "https://play.staratlas.com/fleet"
    driver.get(link)
    time.sleep(2)

    # Cookies part.
    accept_cookies()

    # Click Wallet.
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/main/div/main/div[2]/div/div/div[3]/div/div/button",
            )
        )
    )
    con_wallet = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div[2]/main/div/main/div[2]/div/div/div[3]/div/div/button",
    )
    driver.execute_script("arguments[0].click();", con_wallet)

    # Agrrement part.
    accept_agreements()

    # Click Phantom.
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(),'connect')]")))
    con_phantom = driver.find_element(
        By.XPATH, "//span[contains(text(),'connect')]")
    driver.execute_script("arguments[0].click();", con_phantom)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//span[contains(text(),'close')]",
            )
        )
    )
    close = driver.find_element(
        By.XPATH, "//span[contains(text(),'close')]")

    driver.execute_script("arguments[0].click();", close)

def accept_cookies():
    # Accept Cookies for the first login.
    try:
        accept_cookies = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div[2]/button[1]"
        )
        driver.execute_script("arguments[0].click();", accept_cookies)
    except:
        print('Cookies passed!')

def accept_agreements():
    # Accept Agreements for the first login.
    for _ in range(1, 3):
        try:
            driver.find_element(
                By.XPATH, "//*[@id='app']/div[9]/div/div/div[3]/label"
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div[2]/div[9]/div/div/div[3]/button"
            ).click()
        except:
            print('Agreement passed!')

def phantom_lock_on():
    """
    Login to Phantom wallet.
    """
    phantom_link = (
        "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/notification.html"
    )
    driver.get(phantom_link)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[1]/div[1]/form/div/input")
        )
    )
    phantom_pass = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[1]/form/div/input"
    )

    # This part will be changed with input metod.
    os.chdir(main_path)
    with open("key.txt","r") as k:
        key = k.readline()
        phantom_pass.send_keys(key)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[1]/div[2]/button")
        )
    )

    phantom_lockon = driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div[2]/button"
    )
    driver.execute_script("arguments[0].click();", phantom_lockon)

def phantom_approve_claim_transaction():
    """ATLAS claim transaction accept."""

    # Wait until new window(phantombwallet) open and go new window.
    WebDriverWait(driver, 20).until(
        EC.new_window_is_opened(driver.window_handles))
    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div[1]/div/div[1]/section[1]/div[2]/div/p",
            )
        )
    )
    # claimed_atlas = driver.find_element(
    #     By.XPATH, "/html/body/div/div/div[1]/div/div[1]/section[1]/div[2]/div/p"
    # ).text

    claimed_atlas_raw = driver.find_element(
        By.XPATH, "//p[contains(text(),'ATLAS')]").text
    claimed_atlas = float((claimed_atlas_raw.split()[1]))

    print(f'{claimed_atlas} ATLAS claimed!')

    # Wait Accept button.
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "html/body/div/div/div[1]/div/div[2]/div/button[2]",
            )
        )
    )
    approve = driver.find_element(
        By.XPATH, "html/body/div/div/div[1]/div/div[2]/div/button[2]"
    )
    driver.execute_script("arguments[0].click();", approve)

    # # Wait new window close and go old window.
    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(driver.window_handles[0])

    return claimed_atlas

def phantom_approve_resupply_transaction():
    """Re-supply all transaction accept."""

    # Wait until new window(phantombwallet) open and go new window.
    WebDriverWait(driver, 20).until(
        EC.new_window_is_opened(driver.window_handles))
    driver.switch_to.window(driver.window_handles[1])

    # Show quantitiy of resources that fleet needs.

    # Wait Accept button.
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "html/body/div/div/div[1]/div/div[2]/div/button[2]",
            )
        )
    )

    approve = driver.find_element(
        By.XPATH, "html/body/div/div/div[1]/div/div[2]/div/button[2]"
    )
    driver.execute_script("arguments[0].click();", approve)

    # Wait new window close and go old window.
    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(driver.window_handles[0])

def phantom_popup():
    """
    This is main screen of Phantom wallet.
    """
    phantom_link = (
        "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html"
    )
    driver.get(phantom_link)

    time.sleep(4)
    total_atlas = driver.find_element(
        By.XPATH, "//p[contains(text(),'ATLAS')]").text

    print(total_atlas)
    total_atlas = float((total_atlas.split()[0].replace(',', '')))
    print(total_atlas)

    return total_atlas

def first_login_check():
    """ It checks if it is your first login."""
    if 'Local Extension Settings' in os.listdir(f"C:\\Users\\{username}\AppData\Local\\Google\\Chrome\\User Data\\A-Selenium\\automate-staratlas"):
        print('Not the first time!')
        pass
    else:
        print('First Login!')
        driver.quit()
        copy_files_folders()
        chrome_driver()

def claim_rewards(total_claimed_atlas=0):
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "/html[1]/body[1]/div[1]/div[1]/div[2]/main[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[2]/div",
            )
        )
    )
    claim_buttons_number = len(driver.find_elements(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[2]/main[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[2]/div",
    ))
    print(f'Claimed fleet number: {claim_buttons_number}')
    time.sleep(3)
    for i in range(1, claim_buttons_number + 1):
        claim_button = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[2]/main/div/main/div[2]/div/div/div[2]/div[" +
            str(i)+"]/div/div[3]/div[1]/div[2]/button",
        )
        # print(claim_button)
        driver.execute_script("arguments[0].click();", claim_button)
        claimed_atlas = phantom_approve_claim_transaction()
        total_claimed_atlas += claimed_atlas

    print(f'TOTAL CLAIMED ATLAS: {total_claimed_atlas:.5f}')

def resupply_all():
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/main/div/main/div[2]/div/div/div[2]/div",
            )
        )
    )
    manage_fleet_number = len(driver.find_elements(
        By.XPATH,
        "/html/body/div[1]/div/div[2]/main/div/main/div[2]/div/div/div[2]/div",
    ))
    print(f'Resupplyed Fleet number: {manage_fleet_number}')

    for i in range(1, manage_fleet_number + 1):
        manage_fleet_btn = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[2]/main/div/main/div[2]/div/div/div[2]/div[" +
            str(i)+"]/div/div[3]/div[2]/button",
        )
        driver.execute_script("arguments[0].click();", manage_fleet_btn)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//span[contains(text(),'Re-supply All')]",
                )
            )
        )
        resupply_all_btn = driver.find_element(
            By.XPATH, "//span[contains(text(),'Re-supply All')]"

        )
        driver.execute_script("arguments[0].click();", resupply_all_btn)
        
        phantom_approve_resupply_transaction()

        close = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div[10]/div/div/div/div/div/div[2]/div[1]/div/span"
    )
        driver.execute_script("arguments[0].click();", close)
        time.sleep(3)


if __name__ == "__main__":
    chrome_driver()
    first_login_check()
    phantom_lock_on()
    total_atlas = phantom_popup()
    enter_fleet()
    claim_rewards(total_claimed_atlas=0)
    resupply_all()
