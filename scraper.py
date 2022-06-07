#imports
import requests
from bs4 import BeautifulSoup
import smtplib

#The URL of the product we are tracing
URL             = 'https://www.amazon.de/EliteDisplay-E233-58-42-inch-Monitor/dp/B079347GWN/ref=sr_1_1_sspa?crid=3A0EZ9R1VA4U7&dchild=1&keywords=monitor+27+zoll&qid=1624376227&sprefix=monitor%2Caps%2C199&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyMVVJNlExM0pZMUNJJmVuY3J5cHRlZElkPUEwODE0Njg2M1FYTE5XR05VVVBQJmVuY3J5cHRlZEFkSWQ9QTEwMjQzNzMxNUJCWDJLWlZFWFkyJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

#The headers of the web browsers
headers         = {
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

#In this variable you put the Gmail adress from which you want to send the mail
fromMailAdress  = ''
#Password
mailPassword    = ''

#In this variable you put the mail adress to which you want to send the mail
toMailAdress    = ''

#The target price you want
targetPrice     = 300

#function for checking the price of the product
def checkPrice():
    page    = requests.get(URL, headers = headers)
    soup    = BeautifulSoup(page.content, 'html.parser')

    title   = soup.find(id="productTitle").get_text()
    price   = soup.find(id="priceblock_ourprice").get_text()

    #eliminates the comma and the Euro sign and converts the price to float type
    convertedPrice = float(price[:-5]) 

    #check if the price reached the targeted price
    if convertedPrice < targetPrice:
        sendMail()



#the function to send e-mail using the smtp library
def sendMail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()

    server.starttls()
    server.ehlo()

    server.login(fromMailAdress, mailPassword)

    subject = 'Price fell down!'
    body    = f"Check the amazon link: {URL}"
    msg     = f"Subject: {subject} \n\n {body}"

    server.sendmail(
        fromMailAdress,
        toMailAdress,
        msg
    )

    print("EMAIL SENT!")

    server.quit()


#Call the function
checkPrice()