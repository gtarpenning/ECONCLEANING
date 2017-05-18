import csv
import lib
import json


class Dep_Var(object):

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_data(self):
        print 'Loading from the dep var sheet'
        data = {}
        with open('./data/dep_var.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = unicode(row['country'].lower(), errors='replace')
                var = row['var']

                try:
                    data[country]
                except:
                    data[country] = {}

                row.pop('country', None)
                row.pop('var', None)
                rd = row
                for y, d in rd.items():
                    if len(d) < 1:
                        d = 'NaN'
                    if len(y) > 4:
                        fy = y[:4]
                        rd.pop(y, None)
                        rd[fy] = float(d)
                data[country][var] = rd

        return data


if __name__ == "__main__":
    print "Displaying just the Food Price Data"
    sheet = Dep_Var()
    d = sheet.get_data()
    print json.dumps(d, sort_keys=True, indent=8)
