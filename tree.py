##############################################################################
## This class builds a simple directory structure based on Akamai property
## information provided by Akamai API in order to mimic our folder structure
## to our organization structure within Akamai Control Panel.
##
## The Akamai API provides an organizational structure viewable in 
## the Akamai Control Panel - https://control.akamai.com.
##############################################################################

class FolderTree:
  def __init__(self, items):
    self.id_to_name_map = dict((i['groupId'], i['groupName']) for i in items)
    self.id_to_parent_map = dict((i['groupId'], i.get('parentGroupId', None)) for i in items)

  def get_structure_property_groups_items(self, items):
    groups = []
    for i in items:
      group = self.find_parent(i['groupId'])
      group = [p.strip() for p in group.split(',')]        ## split the list of parents, remove whitespace
      group = list(filter(None, group))                    ## filter empty strings
      group.reverse()                                      ## reverse the list so the top level parent shows up first
      group.append(self.id_to_name_map.get(i['groupId']))  ## add current property into folder structure
      group = [p.lower().replace(' ', '-') for p in group] ## consistent naming with lowercase and - in place of spaces
      groups.append(group)

    # ## sort the groups into shortest lengths first
    # ## the shortest lengths group are top level directory structures
    sorted_groups = sorted(groups, key=lambda l: (len(l), l))
    return sorted_groups

  def get_structure_properties(self, properties):
    groups = []
    for p in properties:
      items = p['properties']['items']
      for i in items:
        group = self.find_parent(i['groupId'])
        group = [p.strip() for p in group.split(',')] ## split the list of parents, remove whitespace
        group = list(filter(None, group))             ## filter empty strings
        group.reverse()                               ## reverse the list so the top level parent shows up first
        group.append(self.id_to_name_map.get(i['groupId']))  ## add the property's parent property name into folder structure
        group.append(i['propertyName'])                      ## add current property into folder structure
        group = [p.lower().replace(' ', '-') for p in group] ## consistent naming with lowercase and - in place of spaces
        groups.append(group)

    # ## sort the groups into shortest lengths first
    # ## the shortest lengths group are top level directory structures
    sorted_groups = sorted(groups, key=lambda l: (len(l), l))
    return sorted_groups

  def get_id_to_name_map(self):
    return self.id_to_name_map

  def get_id_to_parent_id_map(self):
    return self.id_to_parent_map

  def find_parent(self, x):
    value = self.id_to_parent_map.get(x, None)
    if value is None:
      return ""
    else:
      # For IDs without name
      if self.id_to_name_map.get(value, None) is None:
        return self.find_parent(value)
      return self.id_to_name_map.get(value) + ", " + self.find_parent(value)
      # return value + ", " + self.find_parent(value)