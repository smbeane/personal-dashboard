from datetime import datetime

class DateTimeUser():
    def __init__(self) -> None:
        self.update_data()

    def update_data(self) -> None:
        now = datetime.now()
    
        day_and_date = now.strftime("%a %b%d")
        year = now.strftime("     %Y")
        curr_time = now.strftime(" %I:%M%p ")
        seconds = now.second

        self.time = curr_time
        self.day_and_date = day_and_date
        self.year = year
        self.seconds = seconds
