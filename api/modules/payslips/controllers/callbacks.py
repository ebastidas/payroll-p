from flask import current_app as app
from flask import request, jsonify
from bson.tz_util import FixedOffset
from datetime import datetime
from ....shared.helpers import get_date_range

# ########################
# PAYSLIP HELPERS - START


def calculate_tax_deduction(gross, tax_rate):
    return round((gross * (tax_rate / 100)), 2)


def calculate_net(gross, national_insurance_deduction, tax_deduction):
    return round((gross - national_insurance_deduction - tax_deduction), 2)

# PAYSLIP HELPERS - END
# ########################


def filterByYearAndMonth(request, lookup):
    """ Filter docs on year and month when these parameters are present in the URL
    """
    year = request.args.get('year')
    month = request.args.get('month')

    if year is not None and month is not None:
        start_date, end_date = get_date_range(year, month, '')
        lookup["date"] = {'$gte': start_date, '$lte': end_date}
    else:
        return True


def calculate_amounts_on_update(updates, original):
    """ recalculate the 'net', 'tax_deduction' amounts when 'tax_rate' is present in the PATCH request body
    """
    if('tax_rate' in updates):
        updates['tax_deduction'] = calculate_tax_deduction(
            original['gross'], updates['tax_rate'])
        updates['net'] = calculate_net(
            original['gross'], original['national_insurance_deduction'], updates['tax_deduction'])

    else:
        return True


def calculate_amounts_on_replace(item, original):
    """ calculate the 'net', 'tax_deduction' amounts when 'tax_rate' is present in the PUT request body
    """
    if('tax_rate' in item):
        # calulate new 'tax_deduction' and 'net'
        new_tax_rate = item['tax_rate']
        item['tax_deduction'] = calculate_tax_deduction(
            original['gross'], new_tax_rate)

        item['net'] = calculate_net(
            original['gross'], original['national_insurance_deduction'], item['tax_deduction'])

        # copy from orignal
        item['external_id'] = original['external_id']
        item['vat'] = original['vat']
        item['date'] = original['date']
        item['gross'] = original['gross']
        item['national_insurance_rate'] = original['national_insurance_rate']
        item['national_insurance_deduction'] = original['national_insurance_deduction']
    else:
        return True


def perform_update_all_payslips():
    """ recalculate the 'net', 'tax_deduction' amounts when 'tax_rate', 'year' and 'month' are present in the POST request
    """
    if 'tax_rate' and 'year' and 'month' in request.json:
        new_tax_rate = request.json['tax_rate']
        year = request.json['year']
        month = request.json['month']

        start_date, end_date = get_date_range(str(year), str(month), '-')

        # find all payslips in between the date range
        payslips_collection = app.data.driver.db['payslips']
        payslips_docs = payslips_collection.find({
            'date': {
                '$gte': datetime.strptime(start_date + ' 01:00:00.000000', '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=FixedOffset(60, '+0100')),
                '$lte': datetime.strptime(end_date + ' 01:00:00.000000', '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=FixedOffset(60, '+0100'))
            }
        })

        # iterate in all docs found and update the amounts
        for payslip_doc in payslips_docs:

            new_tax_deduction = calculate_tax_deduction(
                payslip_doc['gross'], new_tax_rate)
            new_net = calculate_net(
                payslip_doc['gross'], payslip_doc['national_insurance_deduction'], new_tax_deduction)

            updates = {
                'tax_rate': new_tax_rate,
                'tax_deduction': new_tax_deduction,
                'net': new_net,
            }
            payslips_collection.update(
                {'_id': payslip_doc['_id']}, {"$set": updates})

        response = jsonify(_status='OK', message='Payslips updated')
        response.status_code = 200
        return response
    else:
        response = jsonify(error='Provide the fields: tax_rate, year, month')
        response.status_code = 401
        return response
