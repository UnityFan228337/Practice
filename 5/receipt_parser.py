#connecting REGex libreary
import re
import json

with open(r"5\raw.txt", "r", encoding="utf-8") as x:
    lines = x.readlines()

prices = []
names = []
payments = []
dates = []
totals = 0

products = []
current_item = None

for line in lines:
    line = line.strip()
    if re.match(r'^\d+\.$', line): #типа 1. 2. 3.
        if current_item:
            products.append(current_item)
        current_item = {}
    elif current_item is not None:
        if 'x' in line:
            # quantity x price
            match = re.search(r'(\d+(?:,\d+)?) x (\d{1,3}(?: \d{3})*,\d{2})', line)
            if match:
                current_item['quantity'] = match.group(1)
                current_item['unit_price'] = match.group(2)
        elif re.match(r'^\d{1,3}(?: \d{3})*,\d{2}$', line):
            current_item['total_price'] = line
        elif not current_item.get('name'):
            current_item['name'] = line

if current_item:
    products.append(current_item)

#Extract total, date, payment
for line in lines:
    line = line.strip()
    if 'ИТОГО:' in line:
        match = re.search(r'(\d{1,3}(?: \d{3})*,\d{2})', line)
        if match:
            totals = match.group(1)
    if 'Время:' in line:
        match = re.search(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})', line)
        if match:
            dates.append(match.group(1))
    if 'Банковская карта:' in line:
        match = re.search(r'(\d{1,3}(?: \d{3})*,\d{2})', line)
        if match:
            payments.append({'method': 'Банковская карта', 'amount': match.group(1)})

#All prices
content = '\n'.join(lines)
all_prices = re.findall(r'\b\d{1,3}(?: \d{3})*,\d{2}\b', content)
prices = all_prices

#Product names
names = [p['name'] for p in products if 'name' in p]

#Structured output
output = {
    'product_names': names,
    'all_prices': prices,
    'total_amount': totals,
    'date_time': dates[0] if dates else None,
    'payment': payments[0] if payments else None,
    'products': products
}

print(json.dumps(output, ensure_ascii=False, indent=4)) 
