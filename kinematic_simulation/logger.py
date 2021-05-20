import csv

class Logger():

    def __init__(self):
        # w+ mode truncates (clears) the file
        log = open('logs/data.csv', 'w+', newline='')
        self.logger = csv.writer(log, dialect = 'excel')


    # def log_to_file(self, x, y, z):
    #     self.logger.writerow([x, y, z])

    def log_to_file(self, t, *data):
        row = [t]
        row.extend(data)

        self.logger.writerow(row)
