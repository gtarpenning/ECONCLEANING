import csv
import lib


class InfantMortalityData(object):

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_data(self, countries):
        data = {}
        with open('./data/infantmortality.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print row['name'], row
                # print '\n\n'
                if row['name'] and row['name'].lower() in countries:
                    data[row['name']] = []
                    for year, d in row.items():
                        try:
                            int(year)
                            d = self.num(d)
                            inputs = [year, d]
                            data[row['name']].append(inputs)
                        except:
                            pass
        return data


if __name__ == "__main__":
    print "Displaying just the Infant Mortality Data"
    mortality = InfantMortalityData()
    l = lib.lib()
    d = mortality.get_data(['france', 'germany'])
    c = l.choose_countries(d)
    l.display(c, d)
