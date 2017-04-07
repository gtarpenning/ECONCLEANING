import csv
import lib
import numpy as np

# inputs
# Pick an indicator from this list:
"""
Region
Country
Nra_covt
nra_cov_i
nra_cov_o
nra_cov_dms
nra_cov_bms
nra_bms_covm
nra_bms_covx
nra_bms_covh
nra_covh
nra_covm
nra_covx
nra_ncm
nra_ncx
nra_nch
nra_nct
nps
nra_totm
nra_totx
nra_toth
Rra
Er_econ
vop_covt
vop_covh
vop_covm
Vop_covx
cte_covh
cte_covm
cte_covx
cte_covt
voc_covh
voc_covm
voc_covx
voc_covt
ssr
shrimp
shrexp
ac_prod
R_and_D
pop_agreconact
pop_agric
pop_nonagric
pop_rural
pop_total
pop_urban
pop_toteconact
gdppcp00
gdpdeflator
gse
gse_constant
cte_dollar
Cte_dollar_constant

nra
nra_o
nra_i
nra_bms
nra_bms_x
nra_bms_m
nra_dms
er_prod
officialERproduct
q
pd
pd_us
Bp
vop_prod
cte
voc_prod
"""

INDICATOR = 'nra'
COUNTRIES = ['nigeria', 'us', 'greece', 'turkey']


class hash(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class Controls(object):

    def num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def get_data(self):
        data = hash()
        r = csv.DictReader(open('./data/controls.csv', 'r'))
        for row in r:
            data[row['country']][row['year']] = row

        return data

    def return_good_data(self, c, ind, d):
        digestible_data = {}
        found_countries = []
        for country in c:
            c_bin = d[country]
            for year, data in c_bin.items():
                if data[ind]:
                    if country not in found_countries:
                        found_countries.append(country)
                    try:
                        digestible_data[country].append([year, self.num(data[ind])])
                    except Exception as e:
                        print e
                        digestible_data[country] = [[year, self.num(data[ind])]]
        return found_countries, digestible_data

    def main(self, target_countries, target_indicators, display):
        d = self.get_data()
        used_c, digest_d = self.return_good_data(target_countries, target_indicators, d)
        l = lib.lib()
        if display:
            l.display(used_c, digest_d)
        return used_c, digest_d


if __name__ == "__main__":
    welk = Controls()
    welk.main(COUNTRIES, INDICATOR, True)
