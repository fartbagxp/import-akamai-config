#!/usr/bin/env bash

set -e

######################################################################
## This function utilizes the Akamai command line tool (CLI) to import
## terraform configurations into each of the property folders.
##
## The folder structure mirrors the Akamai control panel, and the
## properties are imported as an effort to provide infrastructure as 
## code (IaC) to provide a glimpse into the Akamai configuration
## settings between projects/programs/domains.
##
## NOTE: this function is best effort only, there may be failures in 
## fetching domains or properties that do not exist, and while they 
## will be printed out, it won't fail the run.
######################################################################
create_akamai_configuration() {
  echo "Creating property configurations from the following folders: "
  local DOMAIN=${1}
  shift 1
  local FOLDERS=("$@")

  ## Quoting the folders parameters will force only the first item to be 
  ## fetched, when this should act as an array.
  # shellcheck disable=SC2048
  for folder in ${FOLDERS[*]}; do
    name="$(basename "${folder}")"
    if [[ ${name} == *"${DOMAIN}" ]]; then
      echo "Folder: ${folder}"
      echo "Domain: ${name}"
      # akamai terraform export-domain --tfworkpath "${folder}" "${name}" || true ## best effort, could fail.
      # akamai terraform export-appsec --tfworkpath "${folder}" "${name}" || true ## best effort, could fail.
      akamai terraform export-property --tfworkpath "${folder}" "${name}" || true ## best effort, could fail.
    fi
  done
}

#######################################################################
## This functions involves deletion of files and should be modified
## carefully. All deletions should be explicit to particular files and
## folders by name, to avoid deletion of the wrong file/folder.
#######################################################################
delete_akamai_configuration() {
  echo "Deleting property configurations from the following folders: "
  local DOMAIN=${1}
  shift 1
  local FOLDERS=("$@")

  ## Quoting the folders parameters will force only the first item to be 
  ## fetched, when this should act as an array.
  # shellcheck disable=SC2048
  for folder in ${FOLDERS[*]}; do
    IMPORT_FILE_TO_DELETE="${folder}/import.sh"
    PROPERTY_FILE_TO_DELETE="${folder}/property.tf"
    VARIABLE_FILE_TO_DELETE="${folder}/variables.tf"
    PROPERTY_SNIPPETS_FOLDER_TO_DELETE="${folder}/property-snippets"
    MODULES_FOLDER_TO_DELETE="${folder}/modules"
    name="$(basename "${folder}")"
    if [[ ${name} == *"${DOMAIN}" ]]; then
      echo "${name}"
      if test -f "${IMPORT_FILE_TO_DELETE}"; then 
        rm -rf "${IMPORT_FILE_TO_DELETE}" 
      fi
      if test -f "${PROPERTY_FILE_TO_DELETE}"; then 
        rm -rf "${PROPERTY_FILE_TO_DELETE}" 
      fi
      if test -f "${VARIABLE_FILE_TO_DELETE}"; then 
        rm -rf "${VARIABLE_FILE_TO_DELETE}" 
      fi
      if test -d "${PROPERTY_SNIPPETS_FOLDER_TO_DELETE}"; then 
        rm -rf "${PROPERTY_SNIPPETS_FOLDER_TO_DELETE}" 
      fi
      if test -d "${MODULES_FOLDER_TO_DELETE}"; then 
        rm -rf "${MODULES_FOLDER_TO_DELETE}" 
      fi
    fi
  done
}

## These are parameters to change based on the type of domains in Akamai 
## configuration and the folder to target this script to.
DOMAIN=".gov"
FOLDER_TO_SCAN="../prod/"

folders="$(find "${FOLDER_TO_SCAN}" -type d)"
create_akamai_configuration ${DOMAIN} "${folders[@]}"
# delete_akamai_configuration ${DOMAIN} "${folders[@]}"