import csv
import lib
import numpy as np
import json

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



nra
nra_o
nra_i
vop_prod
cte
voc_prod



"""

INDICATOR = 'nra'
COUNTRIES = ['france']


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
            data[row['country']][row['prod2']][row['year']] = row

        return data

    def return_good_data(self, c, ind, d):
        digestible_data = {}
        found_countries = []
        for country in c:
            country = country.lower()
            digestible_data[country] = {}
            c_bin = d[country]
            for product in c_bin:
                print product
                if product.lower() == 'general':
                    p_bin = c_bin[product]
                    for year, data in p_bin.items():
                        if data[ind]:
                            if country not in found_countries:
                                found_countries.append(country)
                            try:
                                digestible_data[country][year] = self.num(data[ind])
                            except:
                                digestible_data[country] = {year: self.num(data[ind])}
                elif c_bin[product]['2000'][ind] and product.lower() in ['wheat', 'barley', 'maize']:
                    print 'in the elif: ' + product
                    p_bin = c_bin[product]
                    digestible_data[country][ind + '-' + product.lower()] = {}
                    for year, data in p_bin.items():
                        if data[ind]:
                            if country not in found_countries:
                                found_countries.append(country)
                            digestible_data[country][ind + '-' + product.lower()][year] = self.num(data[ind])

        return found_countries, digestible_data

    def main(self, target_countries, target_indicators, display):
        d = self.get_data()
        used_c, digest_d = self.return_good_data(target_countries, target_indicators, d)
        l = lib.lib()
        if display:
            l.display(used_c, digest_d)
        print json.dumps(digest_d, sort_keys=True, indent=8)
        return used_c, digest_d


if __name__ == "__main__":
    welk = Controls()
    welk.main(COUNTRIES, INDICATOR, False)
