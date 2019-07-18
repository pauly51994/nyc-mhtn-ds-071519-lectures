import math
import operator

class Dsc_Stats:
    
    @staticmethod
    def calc_mean(data):
        return sum(data)/len(data)
    
    @staticmethod
    def calc_med(data):
        mid = len(data)/2
        if len(data)%2 == 0:
            return (data[int(mid + .5)] + data[int(mid - .5)])/2
        else: return data[int(mid - .5)]
    
    @staticmethod
    def calc_mode(data):
       values = {item:0 for item in data}
       for item in data:
           values[item] += 1
       return max(values.items(), key=operator.itemgetter(1))[0]
   
    @staticmethod
    def variance(data):
        mean = Dsc_Stats.calc_mean(data)
        return sum(list(map(lambda num: (num - mean)**2, data)))/(len(data)-1)

    @staticmethod
    def std_dev(data):
        return math.sqrt(Dsc_Stats.variance(data))