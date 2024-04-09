import csv
import requests

# Calling the API on a while loop for pagination
# Passing in the next_page as a URL param to get all results. 
def get_user_ids(token):
    user_data = []
    headers = {"Authorization": f"Bearer {token}"}
    api_url = "https://api.metronome.com/v1/customers"
    next_page = None

    while True:
        url_with_params = api_url + f"?next_page={next_page}" if next_page else api_url

        try:
            response = requests.get(url_with_params, headers=headers)

            data = response.json()
            for user in data.get('data', []):
                user_data.append({'id': user.get('id'), 'name': user.get('name')})

            next_page = data.get('next_page')
            if not next_page:
                break

        # Standard exception handling + print since running locally.
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            break

    return user_data

# Similar method here - just passing in each user id and capturing the invoices for each. 
def get_invoices_for_user(user_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"https://api.metronome.com/v1/customers/{user_id}/invoices"

    try:
        response = requests.get(api_url, headers=headers)

        data = response.json()
        invoices = data.get('data', [])
        return invoices

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return []

# Passing in each user_id similar to invoices. 
# I wanted to add a field for the grant amount in dollars for easier reading.
def get_credit_grants_for_user(user_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = "https://api.metronome.com/v1/credits/listGrants"
    payload = {
        "customer_ids": [user_id],
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()
        grants = data.get('data', [])
        for grant in grants:
            grant_amount_dollars = grant.get('grant_amount', {}).get('amount', 0) / 100
            grant['grant_amount_dollars'] = grant_amount_dollars

        return grants

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return []

# Split this file into a couple different methods
# Not the absolute most granular but I think good for this exercise & timeline.
def main():
    token = '' # Your Token Here
    if not token:
        print("Please provide a valid token")
        return

    # First just getting IDs, then using the customer IDs to get invoices, subtotals, and credit grants
    user_ids = get_user_ids(token)
    for user in user_ids:
        invoices = get_invoices_for_user(user.get('id'), token)
        # Wanted to makes rue we are only getting draft here for both count and total
        draft_invoices_count = sum(1 for invoice in invoices if invoice.get('status') == 'DRAFT')
        draft_invoices_subtotal = sum(invoice.get('total', 0) for invoice in invoices if invoice.get('status') == 'DRAFT')

        grants = get_credit_grants_for_user(user.get('id'), token)
        credit_grants_count = len(grants)
        total_credit_grants = sum(grant.get('grant_amount_dollars', 0) for grant in grants)

        # Setting user fields here for later writing
        user.update({
            'draft_invoices_count': draft_invoices_count,
            'draft_invoices_subtotal': draft_invoices_subtotal,
            'credit_grants_count': credit_grants_count,
            'total_credit_grants': total_credit_grants
        })

    # I wanted to sort by subtotal since many of the fields had a zero subtotal.
    user_ids_sorted = sorted(user_ids, key=lambda x: x.get('draft_invoices_subtotal', 0), reverse=True)

    # Pretty boilerplate CSV writing. 
    with open('metronome_invoices.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Customer Name', 'Customer ID', 'Draft Invoice Count', 'Subtotal ($)', 'Credit Grant Count', 'Total Credit Grants ($)'])
        writer.writeheader()

        for user in user_ids_sorted:
            writer.writerow({
                'Customer Name': user.get('name'),
                'Customer ID': user.get('id'),
                'Draft Invoice Count': user.get('draft_invoices_count', 0),
                'Subtotal ($)': '{:.2f}'.format(user.get('draft_invoices_subtotal', 0)),
                'Credit Grant Count': user.get('credit_grants_count', 0),
                'Total Credit Grants ($)': '{:.2f}'.format(user.get('total_credit_grants', 0))
            })

if __name__ == '__main__':
    main()
