from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scraper():
    # Install the ChromeDriver and get its path
    chromedriver_path = "C:\\Users\\tanho\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"     
    print(f"The path of the ChromeDriver is: {chromedriver_path}")

    # Create a new Service instance and specify the path to the Chromedriver executable
    service = ChromeService(executable_path=chromedriver_path)

    # Create ChromeOptions object
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--log-level=3")

    # Create a new Chrome webdriver instance, passing in the Service and options objects
    driver = webdriver.Chrome(options=options, service=service)

    try:
        # Navigate to the first webpage
        driver.get('https://cde.nus.edu.sg/ece/undergraduate/electrical-engineering/ee-curriculum-structure-ay2022-23/')
        
        # EE
        common_curr = ['Singapore Studies', 'Cultures and Connections', 'Communities and Engagement']

        # Wait for the page to load and find the tbody element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        tbody = driver.find_element(By.TAG_NAME, "tbody")
        output = tbody.find_elements(By.TAG_NAME, 'a')
        for i in output:
            common_curr.append(i.text)

        ##
        """
        Choose 24 units
        """

        # Navigate to the second webpage
        driver.get('https://cde.nus.edu.sg/ece/second-major-in-computing-design-and-engineering/')

        second_common_curr = ['CS1010E', ['EE2211', 'CDE2212'], 'CS2030', 'CS2040', 'CS2100', 'CS2103']

        # Choose 16 units
        second_elec_curr = []

        # Wait for the table rows to be present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        output = driver.find_elements(By.TAG_NAME, 'tr')
        a_tag = output[5].find_elements(By.TAG_NAME, 'a')
        for i in a_tag:
            second_elec_curr.append(i.text)

    finally:
        driver.quit()

    return common_curr, second_common_curr, second_elec_curr

if __name__ == "__main__":
    common_curr, second_common_curr, second_elec_curr = scraper()
    print("Common Curriculum:", common_curr)
    print("Second Major Common Curriculum:", second_common_curr)
    print("Second Major Elective Curriculum:", second_elec_curr)
