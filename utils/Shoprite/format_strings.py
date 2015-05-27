import re


def cents_to_dollars(price_string):
    pattern = re.search(r'([^0-9]*)([\d]+)\xa2(.*)', price_string)
    if pattern:
        return "{0}$0.{1}{2}".format(pattern.group(1), pattern.group(2), pattern.group(3))


def remove_extra_periods(string):
    pattern = re.sub(r'\.{2,}', '', string)
    return pattern


def remove_extra_text(price_string):
    pattern = price_string
    your_choice = re.search(r'(.*)(?i)your choice!?\s?(.*)', pattern)
    if your_choice:
        pattern = "{0}{1}".format(your_choice.group(1), your_choice.group(2))

    wow = re.search(r'(.*)(?i)wow!?\s?(.*)', pattern)
    if wow:
        pattern = "{0}{1}".format(wow.group(1), wow.group(2))

    mix_match = re.search(r'(.*)(?i)mix .+ match!?\s?(.*)', pattern)
    if mix_match:
        pattern = "{0}{1}".format(mix_match.group(1), mix_match.group(2))

    final_cost = re.search(r'(.*)(?i)final cost\s?(.*)', pattern)
    if final_cost:
        pattern = "{0}{1}".format(final_cost.group(1), final_cost.group(2))
    return pattern