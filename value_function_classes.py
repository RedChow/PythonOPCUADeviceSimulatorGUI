"""
random.sample(range(1, 7), k=random.randint(6, 17), counts=[10, 2, 2, 2, 2, 2])
"""
import math
import random
import time
from collections import deque


class ValueFunction:
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        """
        :param device:
        """
        self.device = device
        self.path = path
        self.y_min = y_min
        self.y_max = y_max
        self.period = period
        self.random = isinstance(random, str)
        self.repeat = repeat
        self.start = time.time()
        self.timer_initialized = False
        self.timeout_in_milliseconds = 0
        self.random_timeout = False
        self.timeout_min = -1
        self.timeout_max = -1
        self.historize = historize
        if self.device is not None:
            if self.device.name in self.path:
                self.path = self.path[self.path.index('/')+1:]

    def get_full_path(self):
        if self.device is not None:
            return self.device.name + '/' + self.path
        return ''

    def evaluate(self):
        raise NotImplementedError

    def set_timeout(self, random_timeout, timeout_min, timeout_max, timeout_in_milliseconds):
        self.random_timeout = random_timeout
        self.timeout_min = timeout_min
        self.timeout_max = timeout_max
        self.timeout_in_milliseconds = timeout_in_milliseconds

    def get_timeout_value(self):
        if self.random_timeout:
            return random.randint(self.timeout_min, self.timeout_max)
        return self.timeout_in_milliseconds

    def timer_has_been_initialized(self):
        return self.timer_initialized

    def initialize_timer(self):
        self.timer_initialized = True

    def random_timer(self):
        return self.random_timeout

    @staticmethod
    def get_function_list(function_type):
        if function_type == 'valuelist':
            return {
                'func_arg_1': 'values',
                'func_arg_2': 'period',
                'func_arg_3': 'repeat',
                'func_arg_4': 'historize'
            }
        elif function_type == 'weightedlist':
            return {
                'func_arg_1': 'values',
                'func_arg_2': 'weights',
                'func_arg_3': 'period',
                'func_arg_4': 'repeat',
                'func_arg_5': 'historize'
            }
        elif function_type == 'rampstep':
            return {
                'func_arg_1': 'min',
                'func_arg_2': 'max',
                'func_arg_3': 'step',
                'func_arg_4': 'repeat',
                'func_arg_5': 'historize'
            }
        elif function_type in ['triangle', 'rampperiodic', 'square', 'randomsquare', 'sin', 'cos']:
            return {
                'func_arg_1': 'min',
                'func_arg_2': 'max',
                'func_arg_3': 'period',
                'func_arg_4': 'repeat',
                'func_arg_5': 'historize'
            }
        else:
            return {}

    @staticmethod
    def functions():
        return sorted(['valuelist', 'weightedlist', 'rampstep', 'triangle', 'rampperiodic', 'square', 'randomsquare',
                       'sin', 'cos'])


class ValueList(ValueFunction):
    """
    period > 0 = number of times to repeat
    """
    def __init__(self, device, path, y_min, y_max, period, values, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)
        self.values = values
        self.repeated_times = 0
        try:
            self.deque = deque(values)
        except TypeError:
            self.deque = deque()
            self.values = []

    def evaluate(self):
        if len(self.deque) > 0:
            v = self.deque.popleft()
            self.device.set_value(self.path, v)
        # if we've taken the last one and are set to repeat, set up the deque for the next call
        if len(self.deque) == 0:
            if self.repeat or self.repeated_times < self.period:
                self.deque = deque(self.values)
                self.repeated_times += 1
                if self.repeated_times >= self.period:
                    self.repeated_times = 0


class Triangle(ValueFunction):
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)

    def evaluate(self):
        t = (time.time() - self.start)*1000
        if t >= self.period:
            if not self.repeat:
                return
            self.start = time.time()

        t = 2 * (self.y_max - self.y_min) * abs(t/self.period - math.floor(t/self.period + .5)) + self.y_min
        self.device.set_value(self.path, t)


class WeightedList(ValueFunction):
    def __init__(self, device, path, y_min, y_max, period, value_list, weight_list, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)
        self.values = value_list
        self.weights = weight_list
        self.choice_list = []
        self.times_evaluated = 0
        self.create_choice_list()

    def create_choice_list(self):
        for pair in zip(self.values, self.weights):
            self.choice_list = [pair[0]]*pair[1] + self.choice_list

    def evaluate(self):
        self.times_evaluated += 1
        if self.times_evaluated > self.period:
            if not self.repeat:
                return
            self.times_evaluated = 0
        self.device.set_value(self.path, random.choice(self.choice_list))


class RampStep(ValueFunction):
    """
    NOTES: period acts as the step value
    """
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)
        # print(self.path, self.device)

    def evaluate(self):
        v = self.device.get_value(self.path)
        if v + self.period > self.y_max:
            if not self.repeat:
                return
            self.device.set_value(self.path, self.y_min)
            return

        self.device.set_value(self.path, v + self.period)


class RampPeriodic(ValueFunction):
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)
        # print(self.path, self.device)

    def evaluate(self):
        if self.period == 0:
            return
        t = (time.time() - self.start)*1000
        if t > self.period:
            if not self.repeat:
                return
            t = 0
            self.start = time.time()
        v = t * (self.y_max - self.y_min)/self.period + self.y_min
        self.device.set_value(self.path, v)


class Square(ValueFunction):
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)

    def evaluate(self):
        value = (time.time() - self.start)*1000
        if value > self.period:
            if not self.repeat:
                return
            self.start = time.time()
            value = 0
        v = self.y_max if math.copysign(1, math.sin(2 * math.pi * value / self.period)) > 0 else self.y_min
        self.device.set_value(self.path, v)


class RandomSquare(ValueFunction):
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)

    def evaluate(self):
        t = (time.time() - self.start)*1000
        if t >= self.period:
            if not self.repeat:
                return
        v = self.y_max if random.random() > .5 else self.y_min
        self.device.set_value(self.path, v)


class Sin(ValueFunction):
    """
    NOTES:
        * Division is an expensive operation, so we compute amplitude and period when the function is initialized
        * Try to make it easy on the user: e.g., "I want a sin function that goes between 1 and 20."
            We compute the amplitude and vertical shift to accommodate
        * Default to 2 minutes
    """
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)
        self.amplitude = (self.y_max - self.y_min)/2
        if self.period != 0:
            self.trig_period = 2*math.pi/self.period
        else:
            self.trig_period = 2*math.pi/(2*60*1000)

    def evaluate(self):
        t = (time.time() - self.start)*1000
        if t >= self.period:
            if not self.repeat:
                return
            self.start = time.time()
        v = self.amplitude*math.sin(self.trig_period*t) + self.amplitude + self.y_min
        self.device.set_value(self.path, v)


class Cos(ValueFunction):
    """
    NOTES:
        * Division is an expensive operation, so we compute amplitude and period when the function is initialized
        * Try to make it easy on the user: e.g., "I want a sin function that goes between 1 and 20."
            We compute the amplitude and vertical shift to accommodate
        * Default to 2 minutes
    """
    def __init__(self, device, path, y_min, y_max, period, repeat=True, historize=False):
        super().__init__(device, path, y_min, y_max, period, repeat, historize)
        self.amplitude = (self.y_max - self.y_min)/2
        if self.period != 0:
            self.trig_period = 2*math.pi/self.period
        else:
            self.trig_period = 2*math.pi/(2*60*1000)

    def evaluate(self):
        t = (time.time() - self.start)*1000
        if t >= self.period:
            if not self.repeat:
                return
            self.start = time.time()
        v = self.amplitude*math.cos(self.trig_period*t) + self.amplitude + self.y_min
        self.device.set_value(self.path, v)


