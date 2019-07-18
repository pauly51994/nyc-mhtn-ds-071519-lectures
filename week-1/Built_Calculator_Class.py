from Calculator_funcs import Dsc_Stats


class Calculator:    
    def __init__(self, data):
        # check from beginning if all elements in data are numbers
        assert all(isinstance(x, (int, float)) for x in data), 'list can only contain numbers'
        
        # at creation, bind data to instance
        self.data = data
        # update the statistics
        self.update_data()
        
    def update_data(self):
        # statistics of data
        self.length = len(self.data)
        self.mean = Dsc_Stats.calc_mean(self.data)
        self.median = Dsc_Stats.calc_med(self.data)
        self.variance = Dsc_Stats.variance(self.data)
        self.standev = Dsc_Stats.std_dev(self.data)
        self.mode = Dsc_Stats.calc_mode(self.data)
        
    def add_data(self, val):
        # if val is a list, extend the current dataset
        if isinstance(val, list):
            self.data.extend(val)
        # otherwise, just append val to end of current dataset
        else: self.data.append(val)
        # update all statistics with the updated dataset
        self.update_data()
    
    def remove_data(self, pos):
        # choose a position in current dataset to remove that piece of data
        del self.data[pos]
        # update all statistics with new dataset
        self.update_data()

