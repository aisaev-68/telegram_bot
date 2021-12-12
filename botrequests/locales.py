# -*- coding: utf-8 -*-


loctxt = {'ru_RU':
              ['Ищем...', 'Выберите дату *заезда*:',
               'Такой город не найден. Повторите поиск.', 'В каком городе будем искать?',
               'Выберите дату *выезда*:', 'Укажите количество отелей, которые необходимо вывести (не более 25).',
               'Показать фотографии отелей?', 'Выберите количество фото для загрузки:',
               'Гостиницы не найдены. Повторите поиск.', 'Дата заезда выбрана.', 'Дата выезда выбрана.',
               'Дата выезда должна быть больше даты въезда.Повторите ввод.', 'Последняя гостиница.', 'Первая гостиница.',
               'Последнее фото.', 'Первое фото.', 'История запросов:\n', 'Ваша история пуста.',
               'Команда:', 'Дата запросов:', 'Город должен содержать только буквы, повторите ввод.',
               'Пожалуйста, уточните город', 'Поиск завершен. Найдены {} гостиниц'
               ],
          'en_US':
              ['Are looking for...', 'Select *check-in date*:',
               'No such city has been found. Repeat the search. ', ' In which city are we looking? ',
               'Select *check-out date*:', 'Specify the number of hotels to be displayed (no more than 25).',
               'Show photos of hotels?', 'Select the number of photos to upload:',
               'No hotels found. Search again. ', ' Check-in date selected. ', ' Check-out date selected.',
               'The check-out date must be greater than the check-in date. Please re-enter.',
               'Last hotel.', 'First hotel.', 'Last photo.', 'First photo.', 'Request history:\n',
               'Your story is empty.', 'Command:', 'Date of requests:', 'City must contain only letters, please re-enter.',
               'Please specify the city', 'Found {} hotels'
               ]
          }

loc_txt = {'ru_RU':
               ['Рейтинг: ', 'Отель: ', 'Адрес: ', 'От центра города:', 'Дата заезда-выезда: ',
                'Цена за сутки (в руб): ', 'Цена за {} сутки (в руб): ', 'Ссылка на страницу: '
                ],
           'en_US':
               ['Rating: ', 'Hotel: ', 'Address: ', 'From the city center: ', 'Check-in (check-out) date: ',
                'Price per day (USD): ', 'Price for {} day (USD): ', 'link to the page: '
                ]
           }

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

hotel_kbd = {'ru_RU':
             ['Меню выбора', 'Дешевые', 'Дорогие', 'Лучшие', 'История', 'Да', 'Нет', 'Найти отель', 'Помощь'],
             'en_US':
             ['Choice menu', 'Cheap', 'Expensive', 'Best', 'History', 'Yes', 'No', 'Find a hotel', 'Help']
             }


commands_bot = {
    "ru_RU": {
        "start": "Запустить бота", "lowprice": "Поиск дешевых отелей",
        "highprice": "Поиск отелей класса люкс", "bestdeal": "Поиск лучших отелей",
        "history": "Показать историю запросов", "help": "Помощь", "cancel": "Отмена"},
    "en_US": {
        "start": "to start bot", "lowprice": "Search for cheap hotels",
        "highprice": "Search for luxury hotels", "bestdeal": "Search for the best hotels",
        "history": "Show request history", "help": "Help", "cancel": "Cancel"}}
