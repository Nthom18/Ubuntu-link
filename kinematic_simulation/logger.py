import csv

class Logger():

    def __init__(self, case_id, test_id):
        file_name = 'logs/data_' + case_id + '_' + str(test_id) +'.csv'
        log = open(file_name, 'w+', newline='')  # w+ mode truncates (clears) the file        
        
        self.logger = csv.writer(log, dialect = 'excel')


    def log_to_file(self, t, *data):
        row = [t]
        row.extend(data)

        self.logger.writerow(row)


    # def combine_files(self, nr_of_files):
    #     for i in range(nr_of_files):


