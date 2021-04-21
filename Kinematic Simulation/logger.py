import csv

class Logger():

    def __init__(self):
        # w+ mode truncates (clears) the file
        log = open('logs/data.csv', 'w+', newline='')
        self.logger = csv.writer(log, dialect = 'excel')

    def log_to_file(self, x, y):
        self.logger.writerow([x, y])


