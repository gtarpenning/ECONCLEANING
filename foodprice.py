import csv
import lib


class FoodPrice(object):

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_data(self):
        data = {}
        with open('./data/foodprice.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            data['Maize'] = {}
            data['Barley'] = {}
            data['Wheat'] = {}
            for row in reader:
                data['Maize'][row['Year']] = self.num(row['Maize'])
                data['Barley'][row['Year']] = self.num(row['Barley'])
                data['Wheat'][row['Year']] = self.num(row['Wheat US HRW'])

        return data


if __name__ == "__main__":
    print "Displaying just the Food Price Data"
    food = FoodPrice()
    d = food.get_data()
    print d
