import datetime
import pandas

# with open("example_data/direct_big_unsub_payments.csv") as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         print(row)

def read_data(name):
    data = pandas.read_csv(
        name,
        parse_dates=["Effective Date"],
        converters={
            'Balance': lambda s: float(s.replace('$', '').replace(',', '')),
            'Interest': lambda s: float(s.replace('$', '').replace(',', '')),
        }
    )
    return data

