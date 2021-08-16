from app.models import *

class Seeder:
    def __init__(self):
        pass

    def seed(self):
        print("Im Seeding")

        station = Station()
        station.name = 'Lahore'
        station.save()

        college = College()
        college.station = station
        college.name = 'LBC1'
        college.save()


# This run() function is automatically called by the script runner
def run():
    seeder = Seeder()
    seeder.seed()
