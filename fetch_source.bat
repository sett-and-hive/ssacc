@echo off
rem fetch_source.bat - download source data for mapping ZIP codes
rem  to SSA County Codes may mapping through FIPS Country Codes
rem Adapted from https://github.com/bgruber/zip2fips/blob/master/fetch_source

rem SSA country code to FIP county code in CSV
curl --create-dirs "https://data.nber.org/ratebook/2018/countyrate2018.csv" -o "data/source/countyrate.csv"

rem FIPS county code to ZIP
curl --create-dirs "https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/Downloads/msabea.zip" -o "data/source/compressed/msabea.zip"
powershell Expand-Archive data\source\compressed\msabea.zip -DestinationPath %CD%\data\source

rem Get a list of all ZIP codes to test our mapping file for completeness
curl --create-dirs "http://federalgovernmentzipcodes.us/free-zipcode-database-Primary.csv" -o "data/source/zipcodes.csv"