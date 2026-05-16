import time


class EnvironmentState:

    def __init__(self):

        self.humidity = 92
        self.co2 = 800
        self.temperature = 21.5
        self.pressure = 0

        self.fan_on = False
        self.mister_on = False

        self.auto_mode = True

        self.target_humidity = 92
        self.target_co2 = 1300

        self.alarm_active = False
        self.alarm_message = ""

        self.sensor_fault = False
        self.sensor_fault_message = ""

        self.system_start_time = time.time()

        self.total_fan_seconds = 0
        self.total_mister_seconds = 0
        
        self.light_on = False


state = EnvironmentState()