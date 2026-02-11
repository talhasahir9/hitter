from faker import Faker
import random

fake = Faker(['en_US', 'en_GB', 'en_CA'])

def generate_random_person():
    country_options = ['US', 'GB', 'CA']
    country = random.choice(country_options)
    
    if country == 'US':
        state = fake.state_abbr()
        city = fake.city()
        zipcode = fake.zipcode()
    elif country == 'GB':
        state = ""
        city = fake.city()
        zipcode = fake.postcode()
    else:  # CA
        state = fake.province_abbr()
        city = fake.city()
        zipcode = fake.postalcode()
    
    name = fake.name()
    email = fake.free_email()
    address1 = fake.street_address()
    address2 = random.choice(["", f"Apt {random.randint(1, 99)}", f"Unit {random.randint(10, 999)}"])
    
    return {
        "name": name,
        "email": email,
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "zip": zipcode,
        "country": country
    }
