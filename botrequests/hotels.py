from keyboards import PhotoYesNo, InlKbShow, HotelKbd, PhotoNumbKbd, InlKbShowNoPhoto, StartKbd, types


class Hotel:
    def __init__(self):
        self.__all_hotels: dict = dict()
        self._get_hotel_kbd: types.InlineKeyboardMarkup = HotelKbd().get_hotel_kbd()
        self.__get_photo_yes_no: types.InlineKeyboardMarkup = PhotoYesNo().get_photo_yes_no()
        self.__get_kbd_photo_numb: types.InlineKeyboardMarkup = PhotoNumbKbd().get_kbd_photo_numb()
        self.__get_show_kbd: types.InlineKeyboardMarkup = InlKbShow().get_show_kbd()
        self.__get_show_no_photo_kbd: types.InlineKeyboardMarkup = InlKbShowNoPhoto().get_show_kbd()
        self.__start_keyboard = StartKbd().get_start_kbd()
        self.__start_index_hotel: int = -1
        self.__start_index_photo: int = -1
        self.__hotel_forward_triger: bool = True
        self.__hotel_backward_triger: bool = False
        self.__photo_backward_triger: bool = False
        self.__photo_forward_triger: bool = True
        self.__photo_list: list = []

    def getAllhotels(self) -> dict:
        return self.__all_hotels

    def setAllhotels(self, hotel_dict: dict) -> None:
        self.__all_hotels = hotel_dict

    all_hotels = property(getAllhotels, setAllhotels)

    def getHotel_kbd(self) -> types.InlineKeyboardMarkup:
        return self._get_hotel_kbd

    def getPhoto_yes_no(self) -> types.InlineKeyboardMarkup:
        return self.__get_photo_yes_no

    def getKbd_photo_numb(self) -> types.InlineKeyboardMarkup:
        return self.__get_kbd_photo_numb

    def getShow_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__get_show_kbd

    def getShowNoPhoto_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__get_show_no_photo_kbd

    def getStart_kbd(self):
        return self.__start_keyboard

    def getHotel_forward_triger(self):
        return self.__hotel_forward_triger

    def getHotel_backward_triger(self):
        return self.__hotel_backward_triger

    def getPhoto_forward_triger(self):
        return self.__photo_forward_triger

    def setPhoto_forward_triger(self, trig):
        self.__photo_forward_triger = trig

    photo_forward_triger = property(getPhoto_forward_triger, setPhoto_forward_triger)

    def getPhoto_backward_triger(self):
        return self.__photo_backward_triger

    def setPhoto_backward_triger(self, trig):
        self.__photo_backward_triger = trig

    photo_backward_triger = property(getPhoto_backward_triger, setPhoto_backward_triger)


    def hotel_forward(self):
        """
        Функция возвращает отель по индексу

        """
        self.__start_index_photo = -1
        self.__photo_backward_triger = False
        self.__photo_forward_triger = True
        if self.__start_index_hotel < len(list(self.__all_hotels)):
            self.__start_index_hotel += 1
            if self.__start_index_hotel > 0:
                self.__hotel_backward_triger = True
        else:
            self.__start_index_hotel = len(list(self.__all_hotels)) - 1
            self.__hotel_forward_triger = False
        if self.__start_index_hotel == len(list(self.__all_hotels)) - 1:
            self.__hotel_forward_triger = False
        hotel = list(self.__all_hotels)[self.__start_index_hotel]
        self.__photo_list = self.__all_hotels[hotel]
        print('Вперед', self.__start_index_hotel)

        return hotel


    def hotel_backward(self):
        """
        Функция возвращает отель по индексу

        """
        self.__start_index_photo = -1
        self.__photo_backward_triger = False
        self.__photo_forward_triger = True
        if self.__start_index_hotel > 0:
            self.__start_index_hotel -= 1
            self.__hotel_forward_triger = True
        else:
            self.__start_index_hotel = 0
            self.__hotel_backward_triger = False
        if self.__start_index_hotel == 0:
            self.__hotel_backward_triger = False

        hotel = list(self.__all_hotels)[self.__start_index_hotel]
        self.__photo_list = self.__all_hotels[hotel]

        print('Назад', self.__start_index_hotel)

        return hotel

    def photo_forward(self):
        """
        Функция возвращает следующее фото отеля по индексу

        """
        if self.__start_index_photo < len(self.__photo_list):
            self.__start_index_photo += 1
            if self.__start_index_photo > 0:
                self.__photo_backward_triger = True
        else:
            self.__start_index_photo = len(self.__photo_list) - 1
            self.__photo_forward_triger = False
        if self.__start_index_photo == len(self.__photo_list) - 1:
            self.__photo_forward_triger = False

        return self.__photo_list[self.__start_index_photo]

    def photo_backward(self):
        """
        Функция возвращает предыдущее фото отеля по индексу

        """
        if self.__start_index_photo > 0:
            self.__start_index_photo -= 1
            self.__photo_forward_triger = True
        else:
            self.__start_index_photo = 0
            self.__photo_backward_triger = False
        if self.__start_index_photo == 0:
            self.__photo_backward_triger = False

        return self.__photo_list[self.__start_index_photo]

    def clearCache(self):
        self.__all_hotels: dict = dict()
        self.__start_index_hotel: int = -1
        self.__start_index_photo: int = -1
        self.__hotel_forward_triger: bool = True
        self.__hotel_backward_triger: bool = False
        self.__photo_backward_triger: bool = False
        self.__photo_forward_triger: bool = True
        self.__photo_list: list = []
