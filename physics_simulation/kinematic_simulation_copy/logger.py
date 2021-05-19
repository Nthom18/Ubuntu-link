import csv

class Logger():

    def __init__(self):
        # w+ mode truncates (clears) the file
        log = open('logs/data.csv', 'w+', newline='')
        self.logger = csv.writer(log, dialect = 'excel')

        self.i = 0

    # def log_to_file(self, x, y, z):
    #     self.logger.writerow([x, y, z])

    def log_to_file(self, x, *y):
        row = [x]
        row.extend(y)

        self.logger.writerow(row)
