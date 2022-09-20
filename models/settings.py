from datetime import datetime


def init():
    global deja_fait
    deja_fait = []
    global skip_0
    skip_0 = 0
    global skip_1
    skip_1 = 0
    global num
    num = -1
    global ref
    ref = -1
    global validate

    def validate(date_text):
        try:
            datetime.strptime(date_text, '%d-%m-%Y')
            return True
        except ValueError:
            return False
