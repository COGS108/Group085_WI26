import requests

def clean_address_chipotle(address, city):
    '''
    Function to clean an address in the 2020 Chipotle dataset for use with the Census Geolocator API

    :param address: An address field for a Chipotle address
    :param city: City to act as a way to find where to split the string
    '''

    # splitting address on first occurrence of city going backwards from end
    address_parts = address.lower().rsplit(" " + city.lower(), 1)
    return (address_parts[0] + ", " + city.lower() + address_parts[1][:-3])

def find_tract(address):
    '''
    Function to find the census tract of a single address with the Census Geolocator API
    
    :param address: one-line address of a single census tract
    '''

    params_find_address = {
        "address": address,
        "benchmark": "Public_AR_Current",
        "vintage": "Census2010_Current",
        "format": "json"
    }

    response_find_address = requests.get("https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress", params=params_find_address)

    data_find_address = response_find_address.json()
    try:
        return data_find_address["result"]["addressMatches"][0]["geographies"]["Census Tracts"][0]["GEOID"]
    except Exception:
        return "00000000000"
    
def find_tract_batch(csv_file):
    '''
    Function to find the census tract of a batch of addresses using the Census Geolocator API

    :param csv_file: file of batched addresses
    '''
    url = "https://geocoding.geo.census.gov/geocoder/geographies/addressbatch"

    params = {
        "benchmark": "Public_AR_Current",
        "vintage": "Census2010_Current",
    }

    files = {
        "addressFile": open(csv_file, "rb")
    }

    response = requests.post(url, params=params, files=files)

    with open(f"{csv_file}_output.csv", "wb") as f:
        f.write(response.content)