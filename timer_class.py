from typing import Optional
import PySide6
from PySide6.QtCore import (QTimer)
from random import randint
from logging import config
import logging


config.fileConfig("log_conf.conf")
logger = logging.getLogger('main')


class OPCTimer(QTimer):
    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = ...):
        super().__init__(parent)
        self.name = None
        self.timer_type = None
        self.functions = []
        self.is_random = False
        self.min = 0
        self.max = 0
        self.interval_milliseconds = 500

    def set_name(self, name):
        self.name = name

    def set_interval(self, milliseconds):
        self.interval_milliseconds = milliseconds

    def set_timer_type(self, timer_type):
        self.timer_type = timer_type
        if timer_type == 'random':
            self.is_random = True

    def set_min_max(self, min_seconds, max_seconds):
        self.min = 1000*int(min_seconds)
        self.max = 1000*int(max_seconds)

    def set_random_timeout(self):
        if self.is_random and (self.min > 0 and self.max > 0):
            return randint(self.min, self.max)

    def add_function(self, function):
        self.functions.append(function)

    def evaluate_functions(self):
        # [x.evaluate() for x in self.functions]
        removal_functions = []
        for x in self.functions:
            try:
                x.evaluate()
            except Exception as e:
                logger.info(f"Removing function due to not being able to evaluate. Error info: {e}.")
                removal_functions.append(x)
        for x in removal_functions:
            self.functions.remove(x)

    def __eq__(self, other):
        return self.name == other
