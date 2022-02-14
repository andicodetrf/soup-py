import os
import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

url = "https://www.amazon.com/dp/B013I40R8E/ref=sbl_dpx_kitchen-electric-cookware_B08GC6PL3D_0"
header = {
	"User-Agent": os.getenv("USER_AGENT"),
	"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price = soup.find(class_="a-offscreen").getText()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()

BUY_PRICE = 300
EMAIL = os.getenv("EMAIL")
PW = os.getenv("PW")

if price_as_float < BUY_PRICE:
	body_message = f"{title} is now {price}"
	message = 'To: {}\nSubject: {}\n\n{}'.format(EMAIL, "Amazon Price Alert!", body_message)
	print(message)
	with smtplib.SMTP('smtp.gmail.com') as connection:
		connection.starttls()
		connection.login(user=EMAIL, password=PW)
		connection.sendmail(EMAIL, EMAIL, message)
