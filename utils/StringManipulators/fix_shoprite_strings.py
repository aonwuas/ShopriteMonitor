import re


def get_plus_card(entry):
    card = re.search(r'(.+) (?i)with price plus card', entry['price'])
    if card:
        return {'bool': True, 'price': card.group(1)}
    else:
        return {'bool': False}


def cents_to_dollars(entry):
    price_check = re.search(r'([^0-9]*)([\d]+)\xa2(.*)', entry['price'])
    if price_check:
        return price_check.group(1) + "$0." + price_check.group(2) + price_check.group(3)


def get_units(entry):
    units = re.search(r'(.+) (LB\.|EA\.)', entry['price'])
    if units:
        return {'bool': True, 'units': units.group(2), 'price': units.group(1)}
    else:
        return {'bool': False}


def remove_extra_periods(entry):
    p = re.sub(r'\.{2,}', '', entry['price'])
    n = re.sub(r'\.{2,}', '', entry['name'])
    return {'price': p, 'name': n}


def remove_extra_text(entry):
    global price
    price = entry['price']
    your_choice = re.search(r'(.*)(?i)your choice!?\s?(.*)', price)
    if your_choice:
        price = your_choice.group(1) + your_choice.group(2)

    wow = re.search(r'(.*)(?i)wow!?\s?(.*)', price)
    if wow:
        price = wow.group(1) + wow.group(2)

    mix_match = re.search(r'(.*)(?i)mix .+ match!?\s?(.*)', price)
    if mix_match:
        price = mix_match.group(1) + mix_match.group(2)

    final_cost = re.search(r'(.*)(?i)final cost\s?(.*)', price)
    if final_cost:
        price = final_cost.group(1) + final_cost.group(2)
    return price