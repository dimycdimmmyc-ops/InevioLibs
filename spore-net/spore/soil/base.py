"""Интерфейс почвы. Любой транспорт реализует 5 методов."""


class Почва:
    def тип(self):
        """'ethernet' / 'wifi' / 'cellular' / 'internet' / 'bluetooth'
        / 'wifi_direct' / 'wifi_aware' / '5g_redcap' / 'rfid' / 'nfc' / 'lora'."""
        raise NotImplementedError

    def пористость(self):
        """0.0 – 1.0. 1 = легко встроиться, 0 = невозможно."""
        raise NotImplementedError

    def питательность(self):
        """0.0 – 1.0. Насколько быстро растёт грибница на этой почве."""
        raise NotImplementedError

    def отправить(self, кому, данные):
        """Отправить байты соседу."""
        raise NotImplementedError

    def получить(self):
        """Получить байты. Возвращает (от_кого, данные) или None."""
        raise NotImplementedError

    def соседи(self):
        """Список известных соседей прямо сейчас."""
        raise NotImplementedError