from datetime import datetime, timedelta
from .UserFactory import UserFactory
from .SensorArray import SensorArray, SensorReading
import pandas as pd

class DataLoader():
    def __init__(self, num_users, num_samples):
        self.nusers: int = num_users
        self.nsamples: int = num_samples
        self.users: [UserFactory] = []
        self.data: [[SensorReading]] = []
        self.dates = []
        self.times = []
        self.loaded = False
        self.df = None

    def toJson(self):
        return {
            "users": [x.toJson() for x in self.users],
            "data": [[y.toJson() for y in x] for x in self.data]
        }

    def toCsv(self):
        return [y.toCsv() for x in self.data for y in x]

    def headers(self):
        if not self.data[0]: return []
        return self.data[0][0].headers()

    def fromCsv(self, filename):
        data = pd.read_csv(filename)
        df = pd.DataFrame(data)
        self.df = df
        self.loaded = True

    def toDf(self):
        if self.loaded: return self.df

        data = [y.toJson() for x in self.data for y in x]
        df = pd.DataFrame(data=data, columns=self.headers())
        self.df = df
        self.loaded = True
        return df

    def genUsers(self):
        self.users =  []
        cnt = 0
        yield (0, 0)
        self.getTimeArray()
        yield (0, 0)
        for _ in range(self.nusers):
            user = UserFactory()
            self.users.append(user)

            for d in self.getUserReadings(user.username) :
                yield (cnt, d)

            yield (cnt, self.nsamples)
            cnt += 1

    def getTimeArray(self):
        timestamp = datetime(2015, 1, 1)
        for _ in range(self.nsamples):
            self.dates.append(timestamp.strftime("%y-%m-%d"))
            self.times.append(timestamp.strftime("%H"))
            timestamp = timestamp + timedelta(hours=6)


    def getUserReadings(self, username):
        sensors = SensorArray()
        cnt = 0
        samples = []
        for _ in range(self.nsamples):
            sample = sensors.sample()
            record = SensorReading(
                sample.outside_temp,
                sample.outside_humidity,
                sample.inside_temp,
                sample.inside_humidity,
                username,
                self.dates[cnt],
                self.times[cnt]
            )
            samples.append(record)
            cnt += 1
            if(cnt %50 == 0): yield cnt
        self.data.append(samples)


