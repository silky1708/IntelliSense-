import sqlite3
from typing import List

class Parameter():
    def __init__(self, paramName, paramType, paramDescription):
        self.paramName = paramName
        self.paramType = paramType
        self.paramDesc = paramDescription

    def print(self):
        print(f"{self.paramName}: {self.paramType}\n{self.paramDesc}")


class DataPoint():
    def __init__(self, methodName, library, parameters):
        self.methodName = methodName
        self.library = library
        self.parameters = parameters

    def print(self,):
        print(f"{self.library}.{self.methodName}")
        for param in self.parameters:
            param.print()


if __name__=="__main__":
    p1 = Parameter("start", "int", "the start point of the interval")
    p2 = Parameter("end", "int", "the end point of the interval")
    
    linspace = DataPoint('linspace', 'numpy', [p1,p2])
    # datapoint.print()

    # building the database
    data = sqlite3.connect('data.sqlite')
    cursor = data.cursor()
    cursor.execute('DROP TABLE IF EXISTS methods')
    cursor.execute('CREATE TABLE methods (id INTEGER, datapoint DataPoint, PRIMARY KEY (id))')
    cursor.execute('INSERT INTO methods (datapoint) VALUES (?)', (linspace))
    cursor.execute('SELECT * FROM methods WHERE id=1')
    
    data.commit()
    d = cursor.fetchone()
    print(d)

    data.close()
