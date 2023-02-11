import os

####################################################################
## Akamai CLI and API clients uses environment variables 
## as credentials for programmatic access. 
## 
## This class can read those environment variables, verify 
## they exist, and return them.
####################################################################

class AkamaiConfig:
  def credentials(self):
    return {
      'baseurl': os.environ.get('AKAMAI_PAPI_HOST', ''),
      'access_token': os.environ.get('AKAMAI_PAPI_ACCESS_TOKEN', ''),
      'client_secret': os.environ.get('AKAMAI_PAPI_CLIENT_SECRET', ''),
      'client_token': os.environ.get('AKAMAI_PAPI_CLIENT_TOKEN', '')
    }

  def verify(self):
    errors = ''
    if os.environ.get('AKAMAI_PAPI_HOST', '') == '':
      errors += 'host'
    if os.environ.get('AKAMAI_PAPI_ACCESS_TOKEN', '') == '':
      if errors != '':
        errors += ', '
      errors += 'access token'
    if os.environ.get('AKAMAI_PAPI_CLIENT_SECRET', '') == '':
      if errors != '':
        errors += ', '
      errors += 'client secret'
    if os.environ.get('AKAMAI_PAPI_CLIENT_TOKEN', '') == '':
      if errors != '':
        errors += ', '
      errors += 'client token'
    if errors != '':
      errors += " is not set."
      return errors, False
    return errors, True
