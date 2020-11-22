from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

url = "https://www.investing.com/equities/tata-consultancy-services-historical-data"
starting_date = "04/01/2016"
ending_date = datetime.strftime(datetime.today(), "%m/%d/%Y")
path_to_adblocker = "./adblock_plus_3.10_0"

chOps = webdriver.ChromeOptions()
chOps.add_argument("load_extension=" + path_to_adblocker)
driver = webdriver.Chrome("./chromedriver", chrome_options=chOps)
driver.create_options()
# driver = webdriver.Firefox(executable_path="./geckodriver")
driver.get(url)

dateWidget = driver.find_element_by_xpath('//*[@id="widgetFieldDateRange"]')
dateWidget.click()

setStartDate = driver.find_element_by_xpath('//*[@id="startDate"]')
setStartDate.clear()
setStartDate.send_keys(starting_date)
setEndDate = driver.find_element_by_xpath('//*[@id="endDate"]')
setEndDate.clear()
setEndDate.send_keys(ending_date)
ApplyButton = driver.find_element_by_xpath('//*[@id="applyBtn"]').click()
time.sleep(3)


table = driver.find_element_by_xpath('//*[@id="curr_table"]/tbody').text.split("\n")

# creating db and inserting into it
import psycopg2

# connecting to db
connection = psycopg2.connect(
    database="test", user="saurabh", password="admin", host="127.0.0.1", port="5432"
)
print("Database successfully opened.")

cursor = connection.cursor()

"""
cursor.execute("CREATE TABLE test (id SERIAL PRIMARY KEY NOT NULL, date DATE NOT NULL, price real NOT NULL);")
print("Table successfully created.")
"""

pid_counter = 1
for row in table:
    temp = row.split()
    # date = datetime.strptime(temp[0] + "-" + temp[1][0:2] + "-" + temp[2], "%b-%d-%Y")
    date = temp[1] + " " + temp[0] + " " + temp[2]
    price = float(temp[3].replace(",", ""))
    cursor.execute(
        """INSERT INTO test (id, date, price) VALUES (%s, to_date(%s, 'DD Mon YYYY'), %s);""",
        (pid_counter, date, price),
    )
    pid_counter += 1
print("Records successfully inserted.")

# commiting to db
connection.commit()

# reading from db
cursor.execute(f"""SELECT * FROM test;""")
rows = cursor.fetchall()
for row in rows:
    print("Date = ", row[1], end="\t")
    print("Price = ", row[2])
print("Database successfully read.")

# closing db connection
connection.close()

# closing webdriver.
driver.close()
