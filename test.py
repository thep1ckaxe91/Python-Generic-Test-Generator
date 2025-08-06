from faker import Faker

fake = Faker()
for __ in range(1234):
    print(len([ x for x in [len(fake.name()) for _ in range(10000)] if x > 50]))