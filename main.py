import requests
import json
import csv
import json

NUM_PAGES=3
AUTHORIZATION_TOKEN='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjozMzMxODEsImV4cCI6MTcwODc3Mzg5NywiaXNzdWVkX2F0IjoxNzA4NzcwMjk3fQ.94pxLXZgSeRPEfUX9zNcGt0ytFE_WCoSxJc2lS5DJOMkR_-FEuDvf96tJSILdRdq3Y1QsWK9e-BjiFZITK2mLg'

def process_contacts(contacts):
    processed_contacts = []

    for contact_id, contact_info in contacts.items():
        processed_contact = {
            'id': contact_id,
            'firstName': contact_info.get('firstName', ''),
            'lastName': contact_info.get('lastName', ''),
            'email': contact_info.get('email', ''),
            'phone': contact_info.get('phone', ''),
            'companyPhone': contact_info.get('companyPhone', ''),
            'sources': json.dumps(contact_info.get('sources', {}))  # Convert sources to JSON string
        }
        processed_contacts.append(processed_contact)

    return processed_contacts

def write_to_csv(processed_contacts, filename='contacts.csv'):
    if processed_contacts:
        keys = processed_contacts[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(processed_contacts)
        print(f"Contacts written to {filename} successfully.")
    else:
        print("No contacts to write.")

def fetch_contacts(authorization_token, num_pages):
    base_url = 'https://app.dealfront.com/t/backend/results-contacts'
    headers = {
        'authority': 'app.dealfront.com',
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {authorization_token}',
        'content-type': 'application/json',
        # Add other headers as needed
    }

    all_contacts = {}

    for page in range(1, num_pages + 1):
        data = {
            'filters': {
                'JobTitleFilter': {
                    'tokens': [
                        {'type': 'cluster', 'mode': 'include', 'value': 'Head of HR'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Leiterin Human Resources'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Leiter Personal'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Personalleiter'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Director of Human Resources'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Director Human Resources'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'HR Director'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Human Resources Manager'},
                        {'type': 'match', 'mode': 'include', 'value': 'Head of people and culture'},
                        {'type': 'match', 'mode': 'include', 'value': '"Head of people and culture"'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'CPO'},
                        {'type': 'cluster', 'mode': 'include', 'value': 'Chief Human Resources Officer'}
                    ]
                },
                'EBIndustryFilter': {
                    'codes': [{'code': 'it', 'mode': 'include'},
                              {'code': 'software', 'mode': 'include'},
                              {'code': 'media', 'mode': 'include'}]
                },
                'RegionalFilter': {
                    'countries': ['DE', 'AT', 'CH'],
                    'regions': []
                },
                'CompanySizeFilter': {
                    'range': {'from': 20, 'to': 800},
                    'uncategorized': False
                }
            },
            'contactIds': [],  # To be filled later
            'isGrouped': False,
            'lang': 'de'
        }

        contact_ids, contacts_infos = fetch_contact_ids(authorization_token, page)
        data['contactIds'] = contact_ids

        response = requests.post(base_url, headers=headers, json=data)
        if response.status_code == 200:
            contacts = response.json()
            # all_contacts.update(contacts)
            for contact_id, contact_info in zip(contact_ids, contacts_infos):
                contact_data = contacts.get(contact_id, {})
                contact_data.update(contact_info)
                all_contacts[contact_id] = contact_data
            print(f"{page} of {num_pages} fetched successfully", end="\r")
        else:
            print(f"Error fetching contacts for page {page}: {response.text}")

    return all_contacts

def fetch_contact_ids(authorization_token, page):
    base_url = 'https://app.dealfront.com/t/backend/search'
    headers = {
        'authority': 'app.dealfront.com',
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {authorization_token}',
        'content-type': 'application/json',
        # Add other headers as needed
    }

    data = {
        'debug': False,
        'filters': {
            'CompanySizeFilter': {
                'range': {'from': 20, 'to': 800},
                'uncategorized': False
            },
            'EBIndustryFilter': {
                'codes': [{'code': 'it', 'mode': 'include'},
                          {'code': 'software', 'mode': 'include'},
                          {'code': 'media', 'mode': 'include'}]
            },
            'JobTitleFilter': {
                'tokens': [
                    {'mode': 'include', 'type': 'cluster', 'value': 'Head of HR'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Leiterin Human Resources'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Leiter Personal'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Personalleiter'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Director of Human Resources'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Director Human Resources'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'HR Director'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Human Resources Manager'},
                    {'mode': 'include', 'type': 'match', 'value': 'Head of people and culture'},
                    {'mode': 'include', 'type': 'match', 'value': '"Head of people and culture"'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'CPO'},
                    {'mode': 'include', 'type': 'cluster', 'value': 'Chief Human Resources Officer'}
                ]
            },
            'RegionalFilter': {
                'countries': ['AT', 'CH', 'DE'],
                'regions': []
            }
        },
        'interests': [{
            'count': 100,
            'deduplicate': False,
            'include': 'companies',
            'numFound': True,
            'offset': page * 100,
            'sorting': 'score desc',
            'type': 'contacts'
        }],
        'profileId': ''
    }

    response = requests.post(base_url, headers=headers, json=data)
    contact_ids = []
    contacts_infos = []
    if response.status_code == 200:
        results = response.json().get('contacts', {}).get('results', [])
        for result in results:
            contact_ids.append(result.get('id'))
            contacts_infos.append({
                "firstName": result.get('firstName'),
                "lastName": result.get('lastName'),
                "jobTitle": result.get('jobTitle')
            })
    else:
        print(f"Error fetching contacts for page {page}: {response.text}")

    return contact_ids, contacts_infos


# Prompt user for authorization token
authorization_token = input("Enter your authorization token: ")

# Prompt user for the number of pages
num_pages = int(input("Enter the number of pages: "))

# Fetch contacts
contacts = fetch_contacts(authorization_token, num_pages)
processed_contacts = process_contacts(contacts)
write_to_csv(processed_contacts, 'contacts.csv')
