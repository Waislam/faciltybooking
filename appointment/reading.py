import csv
import os

# filepath = 'input.csv'


filepath = os.path.join('app/static/csv/w2leisureinput.csv')

class ReadWrite:
    data_list = []
    def __init__(self):
        pass

    def read_data(self):
        """ Read data csv file """

        with open(filepath) as csvfile:
            thereader = csv.DictReader(csvfile)
            for item in thereader:
                hkid = item['HKID']
                hkiddigit = item['HKIDDIGIT']
                telephone = item['TELEPHONE']
                date = item['Date']
                facility = item['Facility']
                type = item['Type']
                time = item['Time']
                area = item['Area']
                venu1 = item['Venu1']
                location1 = item['Location1']
                venu2 = item['Venu2']
                location2 = item['Location2']
                venu3 = item['Venu3']
                location3 = item['Location3']
                concession = item['Concession']
                name = item['Name']
                email = item['Email']
                account = item['Account']
                pin = item['Pin']
                leisurelinkn = item['Leisureln']
                password = item['Password']





                self.data_list.append({'HKID': hkid,
                                       'HKIDDIGIT': hkiddigit,
                                       'TELEPHONE': telephone,
                                       'Date': date,

                                       'Facility': facility,
                                       'Type': type,
                                       'Time': time,
                                       'Area': area,
                                       'Venu1': venu1,
                                       'Location1': location1,
                                       'Venu2': venu2,
                                       'Location2': location2,
                                       'Venu3': venu3,
                                       'Location3': location3,
                                       'Concession': concession,
                                       'Name': name,
                                       'Email': email,
                                       'Account': account,
                                       'Pin': pin,
                                       'Leisurelinkn': leisurelinkn,
                                       'Password': password

                                       })



# if __name__ == "__main__":
#     bot = ReadWrite()
#     bot.read_data()
