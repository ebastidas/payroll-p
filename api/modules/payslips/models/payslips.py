payslips = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'external_id'
    },
    'schema': {
        'external_id': {
            'type': 'string',
        },
        'vat': {
            'type': 'string'
        },
        'date': {
            'type': 'datetime'
        },
        'gross': {
            'type': 'number'
        },
        'national_insurance_rate': {
            'type': 'number',
            'min': 0,
            'max': 100
        },
        'national_insurance_deduction': {
            'type': 'number'
        },
        'tax_rate': {
            'type': 'number',
            'min': 0,
            'max': 100
        },
        'tax_deduction': {
            'type': 'number'
        },
        'net': {
            'type': 'number'
        }
    }
}
