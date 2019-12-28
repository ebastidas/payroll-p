# -*- coding: utf-8 -*-

"""
    init-db
    ~~~~~~~~~~~~~~~
    1) delete all items in the 'payslips' collections
    2) read the file and 'payslips.201812.txt' and parse each line to a valid JSON object
    3) Insert this JSON obejct as docs in the 'payslips' collections
"""
import json
import requests

# CONSTANTS - START
# APP_HOST = 'http://localhost:8080/api/v1/'  # localhost
APP_HOST = 'https://pers-payr.eu-de.cf.appdomain.cloud/api/v1/'  # IBM Cloud


payslip_line_structure = {
    'external_id': {
        'start': 0,
        'end': 12
    },
    'vat': {
        'start': 12,
        'end': 21
    },
    'date': {
        'start': 21,
        'end': 29
    },
    'gross': {
        'start': 29,
        'decimal_separator': 35,
        'end': 37
    },
    'national_insurance_rate': {
        'start': 37,
        'decimal_separator': 39,
        'end': 41
    },
    'national_insurance_deduction': {
        'start': 41,
        'decimal_separator': 47,
        'end': 49
    },
    'tax_rate': {
        'start': 49,
        'decimal_separator': 51,
        'end': 53
    },
    'tax_deduction': {
        'start': 53,
        'decimal_separator': 59,
        'end': 61
    },
    'net': {
        'start': 61,
        'decimal_separator': 67,
        'end': 69
    },

}
# CONSTANTS - END


def post_payslips():

    payslips = []

    # Read file 'payslips.201812.txt' line by line and parse each line to a JSON format
    filepath = 'payslips.201812.txt'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            payslips.append(
                {
                    'external_id': line[payslip_line_structure['external_id']['start']: payslip_line_structure['external_id']['end']],
                    'vat': line[payslip_line_structure['vat']['start']: payslip_line_structure['vat']['end']],
                    'date': line[payslip_line_structure['date']['start']: payslip_line_structure['date']['end']],
                    'gross': float(line[payslip_line_structure['gross']['start']: payslip_line_structure['gross']['decimal_separator']] + '.' + line[payslip_line_structure['gross']['decimal_separator']: payslip_line_structure['gross']['end']]),
                    'national_insurance_rate': float(line[payslip_line_structure['national_insurance_rate']['start']: payslip_line_structure['national_insurance_rate']['decimal_separator']] + '.' + line[payslip_line_structure['national_insurance_rate']['decimal_separator']: payslip_line_structure['national_insurance_rate']['end']]),
                    'national_insurance_deduction': float(line[payslip_line_structure['national_insurance_deduction']['start']: payslip_line_structure['national_insurance_deduction']['decimal_separator']] + '.' + line[payslip_line_structure['national_insurance_deduction']['decimal_separator']: payslip_line_structure['national_insurance_deduction']['end']]),
                    'tax_rate': float(line[payslip_line_structure['tax_rate']['start']: payslip_line_structure['tax_rate']['decimal_separator']] + '.' + line[payslip_line_structure['tax_rate']['decimal_separator']: payslip_line_structure['tax_rate']['end']]),
                    'tax_deduction': float(line[payslip_line_structure['tax_deduction']['start']: payslip_line_structure['tax_deduction']['decimal_separator']] + '.' + line[payslip_line_structure['tax_deduction']['decimal_separator']: payslip_line_structure['tax_deduction']['end']]),
                    'net': float(line[payslip_line_structure['net']['start']: payslip_line_structure['net']['decimal_separator']] + '.' + line[payslip_line_structure['net']['decimal_separator']: payslip_line_structure['net']['end']])
                }
            )

            line = fp.readline()
            cnt += 1

    # Insert json object created to database
    HTTP_HEADERS = {'Content-Type': 'application/json'}
    r = requests.post(APP_HOST + 'payslips',
                      json.dumps(payslips), headers=HTTP_HEADERS)
    print("'payslips' posted", r.status_code)


def delete_all_payslips():
    r = requests.delete(APP_HOST + 'payslips')
    print("'payslips' deleted", r.status_code)


def reset_database():
    # delete database
    delete_all_payslips()

    # populate_ database
    post_payslips()


if __name__ == '__main__':
    reset_database()
