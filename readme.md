#This telegram bot allows you to search hotels

## Description.
    The Telegram bot is designed to search hotels on the Hotels.com website according to the criteria
    set by users. The open API Hotels is used, which is located on website rapidapi.com. The user using 
    special bot commands can perform the following actions (get the following information):

         1. Find out the top of the cheapest hotels in the city (command / lowprice).
         2. Find out the top most expensive hotels in the city (command / highprice).
         3. Find out the top hotels, the most suitable for the price and location from the center
         (cheapest and closest to the center) (command / bestdeal)
         4. Find out the history of hotel search (command / history)
         5. Get help for the bot (command / help) 

### Requirements:

    Python 3.9+
    Sqllite3

### Libraries:

    beautifulsoup4
    certifi==2021.10.8
    charset-normalizer==2.0.7
    emoji==1.6.1
    frozenlist==1.2.0
    idna==3.3
    pyTelegramBotAPI==4.2.2
    python-dateutil==2.8.2
    python-decouple==3.5
    python-telegram-bot-calendar @ git+https://github.com/artembakhanov/python-telegram-bot-calendar.git@00cb20d566565d7bd1602e006eb300b27279c112
    requests==2.26.0
    six==1.16.0
    soupsieve==2.3.1
    typing_extensions==4.0.1
    urllib3==1.26.7

### To install locally:

   1. Download this repository
   2. Create a file *.env* in the downloaded directory
   3. Find Bot-Father in telegram. Register a new bot and copy his *token*
   4. Add this strings to the *.env* file and save it:
        """
        TELEGRAM_API_TOKEN=*your token*
        URL="https://hotels4.p.rapidapi.com/locations/search"
        URL_LOW="https://hotels4.p.rapidapi.com/properties/list"
        URL_PHOTOS="https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        """

### Create and activate a virtual environment:

    Install dependencies in env / virtual environment:   
    pip install -r requirements.txt

### How to run:

     python main.py

### Available functions:

     ● /start - bot launch
     ● /help — help with bot commands
     ● /lowprice — listing of the cheapest hotels in the city
     ● /highprice — conclusion of the most expensive hotels in the city
     ● /bestdeal — conclusion of hotels that are most suitable in terms of price and location from the center
     ● /history - hotel search history display

