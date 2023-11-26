import datetime as dt
from typing import Optional


class Record:
    # Record class that allows to collect the records for the calculators
    # In the form of (amount, comment, date(optional))
    # If the date is optional, then the date will be set to today's date
    date_format = '%d.%m.%Y'

    def __init__(self, amount: int, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date,self.date_format).date()


class Calculator:
    # Base calculator class that allows for inheritance of the Cash and Calories calculators
    # It is initialized with the amount of limit.
    # It has methods that allow to add the record using Record object.
    # It allows to get today (current date) stats.
    # It is able to count weekly stats.
    def __init__(self, limit):
        # Value check for the limit.
        if limit >= 0:
            self.limit = limit
        else:
            raise ValueError("Только положительные числа")
        self.records = []
        self.daily_spent_amount = 0

    def add_record(self, record):
        # Adds the record to the record pool of the calculator.
        self.records.append(record)
        if record.date == dt.datetime.now().date():
            # If the entered date is today, it will add the spent amount to the daily limit.
            self.daily_spent_amount += record.amount

    def get_today_stats(self):
        # Returns the daily spent amount that was accumulated by the variable.
        return self.daily_spent_amount

    def get_week_stats(self):
        # Returns the weekly spent amount by iterating over the records list and
        # checking if the date of the record object is in the period from today and
        # 7 days ago.
        today = dt.datetime.now().date()
        last_week = today - dt.timedelta(days=7)
        weekly_spent = 0
        for record in self.records:
            if last_week <= record.date <= today:
                weekly_spent += record.amount
        return weekly_spent


class CashCalculator(Calculator):
    # Cash calculator child class inherited from the Calculator class.
    # Inherits all the methods from the parent
    # Has the method to count the cash remained for today
    USD_RATE = 87.98
    EURO_RATE = 96.29
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        # This method allows to count the remained cash for today.
        # It checks the currency entered and returns the message with the remained money.
        # In the currency entered.
        remained_cash = self.limit - self.daily_spent_amount
        postfix_dict = {
            "rub": ("руб", self.RUB_RATE),
            "usd": ("USD", self.USD_RATE),
            "eur": ("Euro", self.EURO_RATE),
        }
        if currency in postfix_dict:
            remained_cash_in_currency = round(remained_cash/postfix_dict[currency][1],2)
            postfix = postfix_dict[currency][0]
        else:
            raise ValueError("Такой валюты нет")

        if remained_cash_in_currency == 0:
            return "Денег нет, держись"

        if remained_cash_in_currency > 0:
            return f"На сегодня осталось {remained_cash_in_currency} {postfix}"

        if remained_cash_in_currency < 0:
            return f"Денег нет, держись: твой долг - {abs(remained_cash_in_currency)} {postfix}"


class CaloriesCalculator(Calculator):
    # Child class that inherits from the Calculator class for
    # calories counting.
    def get_calories_remained(self):
        # Counts the calories remaining and returns the message based on the value.
        remainder = self.limit - self.daily_spent_amount
        if remainder >= 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remainder} кКал"
        if remainder < 0:
            return "Хватит есть!"


# Basic usage scenario
cash_calculator = CashCalculator(1000)  # Inits the object with the limit value of 1000.
cash_calculator.add_record(Record(amount=145, comment="кофе"))  # Adds the record to instanced calculator object.
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained("rub"))  # Writes the today cash remained according to the records.
