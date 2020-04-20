import decimal
from faker import Faker
from dataclasses import dataclass

"""
model of sensor array read
"""
@dataclass
class SensorDataModel:
    outside_temp: float
    outside_humidity: float
    inside_temp: float
    inside_humidity: float

    def toJson(self):
        return self.__dict__

    def toCsv(self):
        return [self.__dict__[key] for key in self.__dict__.keys()]

    def headers(self):
        return [key for key in self.__dict__.keys()]

    def __repr__(self):
        return self.toJson()

"""
model for taking and saving sensor readings
adds metadata to SensorDataModel
"""
@dataclass
class SensorReading(SensorDataModel):
    username: str
    date: str
    time: str

    def toJson(self):
        dc = super().toJson()
        return dc

    def toCsv(self):
        dc = super().toCsv()
        return dc

    def headers(self):
        return super().headers()

    def __repr__(self):
        return self.toJson()


"""
The base sensor class takes the units and range
of possible valuess and exposes one method, read
"""
class Sensor():
    def __init__(self, vmin, vmax, unit):
        self.vmin = vmin
        self.vmax = vmax
        self.unit = unit

    def read(self, limit):
        F = Faker()
        offset = F.random_int(min=0, max=10)

        smin = self.vmin if not limit else limit - offset
        smax = self.vmax if not limit else limit

        result = float(decimal.Decimal(
            F.random.randint(
                smin*10,
                smax*10)
        )/10)

        return result

""" A sensor for measuring temperature """
class TemperatureSensor(Sensor):
    def __init__(self, m=70, x=95):
        super().__init__(m, x, "F")

""" A sensor for measuring relative humidity """
class HumiditySensor(Sensor):
    def __init__(self, m=50, x=95):
        super().__init__(m, x, "%")

"""
The sensor array is made up of four sensors
two each for temperature and humidity
"""
class SensorArray():
    def __init__(self):
        self.outsideTemperature = TemperatureSensor()
        self.insideTemperature = TemperatureSensor()
        self.outsideHumidity = HumiditySensor()
        self.insideHumidity = HumiditySensor()

    def sample(self):
        o_tmp =self.outsideTemperature.read(None)
        i_tmp =self.insideTemperature.read(o_tmp)
        o_hum =self.outsideHumidity.read(None)
        i_hum =self.insideHumidity.read(o_hum)

        return SensorDataModel(
            o_tmp, o_hum, i_tmp, i_hum
        )
