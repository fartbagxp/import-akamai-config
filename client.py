#############################################################################
## This is a simple Akamai client based on a limited number of Akamai's APIs
## used to pull a number of our configurations.
##
## Akamai Tech Docs for APIs: https://techdocs.akamai.com/home/page/products-tools-a-z?sort=api
## Akamai Property Manager API: https://techdocs.akamai.com/property-mgr/reference/api-summary 
## 
#############################################################################
import requests
import json
from akamai.edgegrid import EdgeGridAuth
from urllib.parse import urljoin

class AkamaiClient:

  def __init__(self):
    self.API_MAPPING = {
      'contract_identifier': '/contract-api/v1/contracts/identifiers',
      'property_groups': '/papi/v1/groups',
      'properties': '/papi/v1/properties'
    }

  def connect(self, credentials):
    self.baseurl = credentials['baseurl']
    s = requests.Session()
    s.auth = EdgeGridAuth(
      client_token=credentials['client_token'],
      client_secret=credentials['client_secret'],
      access_token=credentials['access_token']
    )
    headers = {"accept": "application/json"}
    result = s.get(urljoin(self.baseurl, self.API_MAPPING['contract_identifier']), headers=headers)
    if result.status_code == 200:
      contract_ids = result.json()
      return s, contract_ids
    elif result.status_code == 401:
      print(f'Failed to get a proper connection due to invalid credentials: status code is {result.status_code}')
      return None, None
    else:
      print(f'Failed to get a proper connection: status code is: {result.status_code}')
      return None, None
    return None, None
  
  def property_group(self, s):
    baseurl = self.baseurl
    headers = {"accept": "application/json"}
    result = s.get(urljoin(baseurl, self.API_MAPPING['property_groups']), headers=headers)
    property_group = result.json()
    if result.status_code == 200:
      return property_group
    else:
      print(f"Failed to call {self.API_MAPPING['property_groups']}, status code is: {result.status_code}")

  def properties(self, s, params=None):
    baseurl = self.baseurl
    headers = {"accept": "application/json"}
    result = s.get(urljoin(baseurl, self.API_MAPPING['properties']), headers=headers, params=params)
    properties = result.json()
    if result.status_code == 200:
      return properties
    else:
      print(f"Failed to call {self.API_MAPPING['properties']}, status code is: {result.status_code}")

  ###########################################################################
  ## This looks to be an undocumented API as the published documentation
  ## is missing /versions/<property version> in its path.
  ## 
  ## The published API can be found here and will throw status code 400.
  ## https://techdocs.akamai.com/property-mgr/reference/get-hostnames
  ##
  ## The Akamai CLI includes a version of this API and can be found here:
  ## https://github.com/akamai/cli-property-manager/blob/729a31bc10889074804c9e7922fa8f2ef181c412/src/papi.js#L180
  ###########################################################################
  def hostnames(self, s, params=None):
    baseurl = self.baseurl
    headers = {"accept": "application/json"}
    url = f"{self.API_MAPPING['properties']}/{params['propertyId']}/versions/{params['propertyVersion']}/hostnames?contractId={params['contractId']}&groupId={params['groupId']}"
    result = s.get(urljoin(baseurl, url), headers=headers)
    hostnames = result.json()
    if result.status_code == 200:
      return hostnames
    else:
      print(f"Failed to call {url}, status code is: {result.status_code}, {result.content}")