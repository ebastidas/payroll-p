### Core Python packages ###
from api.modules.payslips.controllers.callbacks import filterByYearAndMonth, calculate_amounts_on_update, calculate_amounts_on_replace, perform_update_all_payslips
from flask_cors import CORS
from eve import Eve
import os
from pathlib import Path
from dotenv import load_dotenv

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
if 'PORT' in os.environ:
    env_path = Path('.') / '.env-production'
else:
    # Uncomment to run app locally, and connect to local MongoDB
    env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

# Environment Variable 'EVE_SETTINGS' is automatically being load as a parameter -> Eve(settings=EVE_SETTINGS...)
os.environ['EVE_SETTINGS'] = os.environ.get(
    'PERS_PAYROLL_BACKEND_EVE_SETTINGS')


# #################################
# #################################
# Flask-Eve App and Routes - START
app = Eve()


@app.route('/health')
def health():
    return 'Personio Payroll up and running!'


# #################################
# Endpoint: payslips  -  START


app.on_pre_GET_payslips += filterByYearAndMonth

app.on_update_payslips += calculate_amounts_on_update

app.on_replace_payslips += calculate_amounts_on_replace


@app.route('/api/v1/payslips/update_all', methods=['POST'])
def update_all_payslips():
    return perform_update_all_payslips()
# Endpoint: payslips  -  END
# #################################


# Flask-Eve App and Routes - END
# #################################
# #################################


# On IBM Cloud, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))

# Needed for non-Eve Flask endpoints accessed via browser in another host
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
