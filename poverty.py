import csv
import lib


class PovertyData(object):

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_data(self):
        data = {}
        dirty = open('./data/poverty.csv', 'rU')
        r = csv.DictReader(dirty)
        # dirty.close()
        for row in r:
            if row['name'] and row['ind'] == 'SI.POV.2DAY':
                data[row['name']] = []
                for year, d in row.items():
                    try:
                        int(year)
                        d = self.num(d)
                        inputs = [year, d]
                        data[row['name']].append(inputs)
                    except Exception as e:
                        print e
                        pass
        return data


if __name__ == "__main__":
    print "Displaying Poverty Data"
    poverty = PovertyData()
    l = lib.lib()
    d = poverty.get_data()
    print d
    c = l.choose_countries(d)
    l.display(c, d)
