import csv
import os

output_file = os.path.join('app/static/output/result.csv')
input_file = os.path.join('app/static/csv/input.csv')

def write_result(data):
    """Write new scrapped data to final result file"""

    headers = ['Hkid', 'Facility']
    with open(output_file, 'a', newline='') as file:
        file_is_empty = os.stat(output_file).st_size == 0
        csv_writer = csv.writer(file, delimiter=',')
        if file_is_empty:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)


# def write_orgin(data):
#     """Write new scrapped data to final result file"""
#
#     keys = data[0].keys()
#
#     with open(input_file, 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(data)