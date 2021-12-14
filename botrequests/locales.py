l_text = {'ru_RU': ['В каком городе будем искать?', 'Будет выведена информация о трех последних запросах',
                    'Извините, данная команда мне неизвестна.\n'],
          'en_US': ['What city are we looking for?', 'Information about the last three requests will be displayed',
                    'Sorry, this command is unknown to me.\n']}

info_help = {'ru_RU':
                 'Привет , я БОТ по поиску отелей. Подобрать для Вас отель? 🏨✅\n'
                 '● /help — помощь по командам бота\n● /lowprice — вывод самых дешёвых отелей в городе\n'
                 '● /highprice — вывод самых дорогих отелей в городе\n'
                 '● /bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                 '● /history - вывод истории поиска отелей',
             'en_US':
                 "Hi, I'm a hotel search BOT. Find a hotel for you? 🏨✅\n"
                 '● /help — help with bot commands\n● /lowprice — listing of the cheapest hotels in the city\n'
                 '● /highprice — conclusion of the most expensive hotels in the city\n'
                 '● /bestdeal — conclusion of hotels that are most suitable in terms of price and location '
                 'from the center\n'
                 '● /history - hotel search history display'
             }


loctxt = {'ru_RU':
              ['Ищем...', 'Такой город не найден. Повторите поиск.', 'В каком городе будем искать?',
               'Выберите дату *заезда*:', 'Выберите дату *выезда*:',
               'Укажите количество отелей, которые необходимо вывести (не более 25).',
               'Показать фотографии отелей?', 'Выберите количество фото для загрузки:',
               'Дата заезда выбрана.', 'Дата выезда выбрана.',
               'Дата выезда должна быть больше даты въезда.Повторите ввод.', 'История запросов:\n',
               'Ваша история пуста.',
               'Команда:', 'Дата запросов:', 'Команда выполнена.', 'Вы отменили данную операцию'
               ],
          'en_US':
              ['Are looking for...', 'No such city has been found. Repeat the search.',
               ' In which city are we looking?',
               'Select *check-in date*:', 'Select *check-out date*:',
               'Specify the number of hotels to be displayed (no more than 25).',
               'Show photos of hotels?', 'Select the number of photos to upload:',
               ' Check-in date selected. ', ' Check-out date selected.',
               'The check-out date must be greater than the check-in date. Please re-enter.',
               'Request history:\n', 'Your story is empty.', 'Command:', 'Date of requests:',
               'Command completed.', 'You canceled this operation'
               ]
          }
commands = ["/lowprice", "/highprice", "/bestdeal"]

loc_txt = {'ru_RU':
               ['Рейтинг: ', 'Отель: ', 'Адрес: ', 'От центра города:', 'Дата заезда-выезда: ',
                'Цена за сутки (в руб): ', 'Цена за {} сутки (в руб): ', 'Ссылка на страницу: ',
                'Найдено {} отелей', 'Нет данных об адресе.', 'Нет данных о расценках.'],
           'en_US':
               ['Rating: ', 'Hotel: ', 'Address: ', 'From the city center: ', 'Check-in (check-out) date: ',
                'Price per day (USD): ', 'Price for {} day (USD): ', 'link to the page: ',
                'Found {} hotels', 'No address data.', 'No price data.']
           }

server_error = {"ru_RU": {"ertime": "Время ожидания запроса истекло. Попробуйте позже.",
                              "erjson": "Получен некорректный ответ от сервиса. Попробуйте позже.",
                              "ercon": "Нет, соединения с сервисом. Попробуйте позже.",
                              "erhttp": "Что-то пошло не так. Повторите позже."},
                    "en_US": {"ertime": "The request timed out. Please try again later.",
                              "erjson": "Received an invalid response from the service. Please try again later.",
                              "ercon": "No, connecting to the service. Please try again later.",
                              "erhttp": "Something went wrong. Please try again later."}}

loc = {'ru_RU':
               ['Отмена', 'Пожалуйста, уточните город', 'Превышена ежемесячная квота для запросов по плану BASIC.'],
           'en_US':
               ['Cancel', 'Please specify city', 'Monthly quota exceeded for BASIC plan requests.']
           }

hotel_kbd = {'ru_RU': ['Да', 'Нет'], 'en_US': ['Yes', 'No']}

commands_bot = {
    "ru_RU": {
        "lowprice": "Поиск дешевых отелей",
        "highprice": "Поиск отелей класса люкс", "bestdeal": "Поиск лучших отелей",
        "history": "Показать историю запросов", "help": "Помощь"},
    "en_US": {
        "lowprice": "Search for cheap hotels",
        "highprice": "Search for luxury hotels", "bestdeal": "Search for the best hotels",
        "history": "Show request history", "help": "Help"}}