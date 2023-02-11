import argparse
import datetime
import os
import sys
import time

from client import AkamaiClient
from config import AkamaiConfig
from tree import FolderTree

################################################################
## A function to call the Akamai hostname API for a list of 
## hostnames in Akamai configuration for collection for an 
## understanding on public domains already configured.
################################################################
def discover_hostnames(client, session, properties):
  hostnames = []
  for p in properties:
    items = p['properties']['items']
    for i in items:
      params = {
        'propertyId': i['propertyId'],
        'propertyVersion': i['latestVersion'],
        'contractId': i['contractId'],
        'groupId': i['groupId']
      }
      hostnames.append(client.hostnames(session, params))
  return hostnames

################################################################
## A function to call the Akamai hostname API for a list of 
## property groups and properties setup in the organization
## of Akamai. This is necessary to understand the organization
## and folder structure currently setup, and may be used
## as input for other API calls.
################################################################
def discover_properties(client, session):
  propertyGroups = client.property_group(session)
  properties = []
  for group in propertyGroups['groups']['items']:
    for contract in group['contractIds']:
      params = {
        'groupId': group['groupId'],
        'contractId': contract
      }
      result = client.properties(session, params)
      result['requestGroupId'] = group.get('groupId')
      result['requestContractId'] = contract
      properties.append(result)
  return propertyGroups, properties

##############################################################################
## A function to mirror the Akamai Control Panel's organization / property
## structure via a local folder structure. 
##
## If we are to use Infrastructure-As-Code (IaC), the configuration will fall
## within each of the property folder structure.
##############################################################################
def generate_folder_path(propertyGroups, properties):
  f = FolderTree(propertyGroups['groups']['items'])
  folders = []
  folders += f.get_structure_property_groups_items(propertyGroups['groups']['items'])
  folders += f.get_structure_properties(properties)
  sortedFolders = sorted(folders, key=lambda l: (len(l), l))
  # from pprint import pprint
  # pprint(sortedFolders)

  foldersOrg = []
  for f in sortedFolders:
    dirpath = '/'.join(f)
    foldersOrg.append(dirpath)
  return foldersOrg

def make_folders(outputPath, folders):
  for f in folders:
    dirpath = os.path.abspath(os.path.join(outputPath, f))
    os.makedirs(dirpath, exist_ok=True)

def handle_arguments():
  DEFAULT_OUTPUT_PATH="./prod/org/"
  parser = argparse.ArgumentParser(description='import the existing hostname organization structure')
  parser.add_argument(
    '-d', '--dryrun', required=False, help='simulate a dry run of the folder structure', action='store_true')
  parser.add_argument(
    '-o', '--output', required=False, type=str, help='location of the output path', default=DEFAULT_OUTPUT_PATH)
  args = parser.parse_args()

  return args.dryrun, args.output

def main():
  now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
  print(now)

  ## verify the akamai configuration and fail immediately if environment
  ## variables aren't set. Read the README.md for more information.
  errors, isVerified = AkamaiConfig().verify()
  if errors or not isVerified:
    print(f'Exiting due to bad credentials in configuration: {errors}')
    sys.exit()

  isDryrun, outputPath = handle_arguments()
  outputPath = os.path.abspath(outputPath)
  print(f'Running dryrun is {isDryrun}, outputPath = {outputPath}')

  ## pull the Akamai configurations for property groups, properties, and hostnames
  ## in order to create a folder structure that mimics the Akamai organization
  ## structure within the Akamai Control Panel - https://control.akamai.com
  c = AkamaiClient()
  s, contact_ids = c.connect(AkamaiConfig().credentials())
  if s == None or contact_ids == None or not contact_ids:
    print('Exiting: failed to get connection or contract IDs from Akamai.')
    sys.exit()

  property_groups, properties = discover_properties(c, s)
  hostnames = discover_hostnames(c, s, properties)

  ## Print all the hostnames and create a csv grouping for anybody who wants
  ## to track hostnames and their organization
  print("List of hostnames and their groupings")
  headers = ['hostname','propertyName','groupId','contractId']
  headers = ','.join(headers)
  print(headers)
  for h in hostnames:
    for hostname in h.get('hostnames', None).get('items', None):
      line = [hostname.get('cnameFrom', None), 
        h.get('propertyName'), 
        h.get('groupId', None), 
        h.get('contractId')]
      line = ','.join(line)
      print(line)

  ## Create a folder structure and print it out for anybody who needs
  ## to understand how Akamai organization structure is stood up
  foldersOrg = generate_folder_path(property_groups, properties)
  print('Folder structure to mirror Akamai folder organization: ')
  for f in foldersOrg:
    print(f)

  if not isDryrun:
    make_folders(outputPath, foldersOrg)
    print('completing folder creation')
  else:
    print('simulated folder creation structure')

if __name__ == "__main__":
  main()