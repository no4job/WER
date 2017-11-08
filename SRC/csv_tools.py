__author__ = 'mdu'
import csv
import os

class dialect_tab(csv.excel):
    delimiter = '\t'

class dialect_semicolon(csv.excel):
    delimiter = ';'

class csvLog:
    def __init__(self,filename, append = 0,save_intial = 0,encoding='utf-8'):
        if save_intial == 1:
            if os.path.exists(filename):
                with open(filename,"r",encoding=encoding) as self.outFile:
                    self.outCsvDictReader = csv.DictReader(self.outFile, dialect=dialect_tab)
                    self.initialCSV = []
                    for row in self.outCsvDictReader:
                        self.initialCSV.append(row)
                    self.initialCSV = tuple(self.initialCSV)
            else:
                self.initialCSV = ()
        if append == 1:
            self.outFile = open(filename, 'a+', newline='',encoding=encoding)
        else:
            if os.path.exists(filename):
                os.remove(filename)
            self.outFile = open(filename, 'w+', newline='', encoding=encoding)
        self.outCsvWriter = csv.writer(self.outFile, delimiter='\t',quoting=csv.QUOTE_MINIMAL)
    def close(self):
        self.outFile.close()
    def __dell__(self):
        self.close()
    def add_row(self,row):
        # print(row)
        self.outCsvWriter.writerow(row)
        self.outFile.flush()
    def add_rows(self,rows):
        self.outCsvWriter.writerows(rows)
        self.outFile.flush()
    def getInitialCSV(self):
        return self.initialCSV
