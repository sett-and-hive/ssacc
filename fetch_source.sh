#!/bin/bash

# fetch_source.sh - download source data for mapping ZIP codes
#  to SSA County Codes may mapping through FIPS Country Codes
# Adapted from https://github.com/bgruber/zip2fips/blob/master/fetch_source

# SSA county code to ZIP code
curl --create-dirs "https://wonder.cdc.gov/wonder/sci_data/datasets/zipctyA.zip" -o "data/source/compressed/zipctyA.zip"
curl --create-dirs "https://wonder.cdc.gov/wonder/sci_data/datasets/zipctyB.zip" -o "data/source/compressed/zipctyB.zip"

unzip data/source/compressed/zipctyA.zip -d data/source
unzip data/source/compressed/zipctyB.zip -d data/source

# SSA county code to FIP county code in CSV
curl --create-dirs "https://data.nber.org/ratebook/2018/countyrate2018.csv" -o "data/source/countyrate.csv"

# State postal code to FIPS state code
curl --create-dirs "https://raw.githubusercontent.com/bgruber/zip2fips/master/state_fips.json" -o "data/source/state_fips.json"

# FIPS county code to ZIP
curl --create-dirs "https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/Downloads/msabea.zip" -o "data/source/compressed/msabea.zip"
unzip data/source/compressed/msabea.zip -d data/source

# Get a list of all ZIP codes to test our mapping file for completeness
curl --create-dirs "http://federalgovernmentzipcodes.us/free-zipcode-database-Primary.csv" -o "data/source/zipcodes.csv"
