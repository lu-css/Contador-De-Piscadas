import os

class BlinkCheck:
    def __init__(self, close_on, open_on, save_file = False, file_path = 'out') -> None:
        self.eyes_close_on = close_on
        self.eyes_open_on = open_on
        self.eyes_closed = False
        self.save_file = save_file
        self.path = file_path
        self.file_path = f'{file_path}/piscadas.txt'
        self.blink_count = 0
        self._config()

    def _config(self):
        self._config_blink()
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _config_blink(self):
        if not self.save_file:
            self.blink_count = 0
            return

        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, 'r') as file:
            for line in file:
                if line.isdigit():
                    self.blink_count = int(line)
                    return

        self.blink_count = 0


    def _blink_updated(self):
        if not self.save_file:
            return

        with open(self.file_path, 'w') as file:
            content = str(self.blink_count)
            file.write(content)
            print("File writed")

    def inc_blinks(self):
        self.blink_count += 1
        self._blink_updated()

    def dec_blinks(self):
        if self.blink_count > 0:
            self.blink_count -= 1

        self._blink_updated()

    def reset_blinks(self):
        self.blink_count = 0
        self._blink_updated()

    def blink(self, ratio):
        if not self.eyes_closed and ratio < self.eyes_close_on:
            self.inc_blinks()
            self.eyes_closed = True
            return True

        if self.eyes_closed and ratio >= self.eyes_open_on:
            self.eyes_closed = False

        return False
