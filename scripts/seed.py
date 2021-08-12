from app.models import *
from app.core.admissions import Level


class Seeder:
    def __init__(self):
        pass

    def add_disc(self, name, level):
        ds = Discipline()
        ds.name = name
        ds.level = level
        ds.save()
        return ds

    def make_slab(self, structure, name, index, marks, amount):
        slab = FeeSlab()
        slab.parent_fee_structure = structure
        slab.name = name
        slab.index = index
        slab.marks = marks
        slab.amount = amount
        slab.save()

    def seed(self):
        print("Im Seeding")

        station = Station()
        station.name = 'Lahore'
        station.save()

        college = College()
        college.station = station
        college.name = 'LBC1'
        college.save()

        medical = self.add_disc('F.Sc Pre-Medical', Level.INTER)
        engg = self.add_disc('F.Sc Pre-Engg', Level.INTER)
        ics = self.add_disc('I.C.S', Level.INTER)
        self.add_disc('I.Com', Level.INTER)

        self.add_disc('Computer', Level.BS)
        self.add_disc('English', Level.BS)
        self.add_disc('Zoology', Level.BS)

        st = FeeStructure()
        st.discipline = medical
        st.full_fee = 115000
        st.save()

        self.make_slab(st, "95% and above", 0, 1045, 1000)
        self.make_slab(st, "94% and above", 1, 1034, 25000)
        self.make_slab(st, "93% and above", 2, 1023, 35000)
        self.make_slab(st, "92% and above", 3, 1012, 47000)
        self.make_slab(st, "91% and above", 4, 1001, 53850)
        self.make_slab(st, "89% and above", 5, 979, 64125)
        self.make_slab(st, "88% and above", 6, 968, 81250)
        self.make_slab(st, "86% and above", 7, 946, 98375)
        self.make_slab(st, "80% and above", 8, 880, 108650)

        st = FeeStructure()
        st.discipline = ics
        st.full_fee = 108800
        st.save()

        self.make_slab(st, "94% and above", 0, 1034, 1000)
        self.make_slab(st, "93% and above", 1, 1023, 25000)
        self.make_slab(st, "92% and above", 2, 1012, 35000)
        self.make_slab(st, "91% and above", 3, 1001, 45000)
        self.make_slab(st, "89% and above", 4, 979, 51380)
        self.make_slab(st, "88% and above", 5, 968, 60950)
        self.make_slab(st, "86% and above", 6, 946, 76900)
        self.make_slab(st, "80% and above", 7, 880, 92850)
        self.make_slab(st, "75% and above", 8, 825, 102420)

        st = FeeStructure()
        st.discipline = engg
        st.full_fee = 115000
        st.save()

        self.make_slab(st, "95% and above", 0, 1045, 1000)
        self.make_slab(st, "94% and above", 1, 1034, 25000)
        self.make_slab(st, "93% and above", 2, 1023, 35000)
        self.make_slab(st, "92% and above", 3, 1012, 47000)
        self.make_slab(st, "91% and above", 4, 1001, 53850)
        self.make_slab(st, "89% and above", 5, 979, 64125)
        self.make_slab(st, "88% and above", 6, 968, 81250)
        self.make_slab(st, "86% and above", 7, 946, 98375)
        self.make_slab(st, "80% and above", 8, 880, 108650)


# This run() function is automatically called by the script runner
def run():
    seeder = Seeder()
    seeder.seed()
