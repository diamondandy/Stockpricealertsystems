#Stock price alert system by Diamond Andy

#This program checks stock prices in real-time and sends an email alert when the price crosses a set threshold.

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Alpha Vantage API configuration
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
STOCK_SYMBOL = 'AAPL'  # Example: Apple stock
ALERT_PRICE = 150  # Set your desired target alert price

# Email configuration
SENDER_EMAIL = 'youremail@gmail.com'
SENDER_PASSWORD = 'yourpassword'
RECEIVER_EMAIL = 'receiveremail@gmail.com'

# Function to fetch stock price
def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Extract the latest closing price from the data
    latest_time = list(data['Time Series (5min)'])[0]
    latest_price = float(data['Time Series (5min)'][latest_time]['4. close'])
    
    return latest_price

# Function to send email alert
def send_email_alert(price):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f'Stock Alert: {STOCK_SYMBOL}'
    
    body = f'The stock price of {STOCK_SYMBOL} is now {price}, which crossed your alert price of {ALERT_PRICE}.'
    msg.attach(MIMEText(body, 'plain'))
    
    # Setting up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    # Send email
    text = msg.as_string()
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
    server.quit()
    
    print(f'Email alert sent for {STOCK_SYMBOL} at price {price}.')

# Main function to monitor stock price and send alert
def check_stock_price():
    current_price = get_stock_price(STOCK_SYMBOL)
    print(f'Current price of {STOCK_SYMBOL}: {current_price}')
    
    if current_price >= ALERT_PRICE:
        send_email_alert(current_price)

# Run the stock checker
if __name__ == "__main__":
    check_stock_price()



