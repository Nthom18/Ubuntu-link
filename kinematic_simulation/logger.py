"""
Logging passed information to csv files format.

Author: Nicoline Louise Thomsen
"""

import csv
import numpy as np

class Logger():

    def __init__(self, case_id, test_id, flock_size):

        if case_id == 'c':
            file_name = 'logs/data_' + case_id + '_' + str(flock_size) + '.csv'
            
            if test_id == 0 or test_id == 'main':
                log = open(file_name, 'w+', newline='') # w+ mode truncates (clears) the file
            else:
                log = open(file_name, 'a', newline='')  # Append to existing file 


        elif case_id == 'd':
            file_name = 'logs/data_' + case_id + '_' + str(test_id) +'.csv'
            log = open(file_name, 'w+', newline='')  # w+ mode truncates (clears) the file (new file for every test)   
        
        self.logger = csv.writer(log, dialect = 'excel')


    def log_to_file(self, t, *data):

        row = [t]
        row.extend(data)

        self.logger.writerow(row)


    def combine_files(self, prefix, nr_of_files, frame_duration):
        
        t = list(range(frame_duration))
        dst0 = np.zeros(frame_duration)
        dst1 = np.zeros(frame_duration)
        dst2 = np.zeros(frame_duration)
        dst3 = np.zeros(frame_duration)
        dst4 = np.zeros(frame_duration)


        for i in range(nr_of_files):
            with open('logs/' + prefix + '_' + str(i) + '.csv','r') as csvfileQuick:
                plots = csv.reader(csvfileQuick, delimiter=',')
                
                for frame, row in enumerate(plots):
                    
                    dst0[frame] += float(row[1])
                    dst1[frame] += float(row[2])
                    dst2[frame] += float(row[3])
                    dst3[frame] += float(row[4])
                    dst4[frame] += float(row[5])

        for i in range(len(t)):
            self.log_to_file(t[i], dst0[i]/nr_of_files, dst1[i]/nr_of_files, dst2[i]/nr_of_files, dst3[i]/nr_of_files, dst4[i]/nr_of_files)


