import re


def price_units(price_string):
    pattern = re.search(r'(.*) (LB\.|EA\.)(.*)', price_string)
    if pattern:
        return dict(bool=True, units=pattern.group(2), price=pattern.group(1) + pattern.group(3))
    else:
        return dict(bool=False, price=price_string)


def get_plus_card(price_string):
    pattern = re.search(r'(.+) (?i)with price plus card', price_string)
    if pattern:
        return dict(bool=True, price=pattern.group(1))
    else:
        return dict(bool=False, price=price_string)


#  call flat_price last
def flat_price(price_string):
    pattern = re.search(r'^\$([\d,\.]+)$', price_string)
    if pattern:
        return dict(bool=True, price="{0:.2f}".format(float(pattern.group(1))))
    else:
        return dict(bool=False, price=price_string)


def flat_reduction(price_string):
    pattern = re.search(r'.*\$([\d,\.]+)[\s]+(?i)off.*', price_string)
    if pattern:
        print "Pattern: " + pattern.group(1)
        return dict(bool=True, price=pattern.group(1))
    else:
        return dict(bool=False, price=price_string)


def conditional(price_string):
    pattern = re.search(r'.*(?i)buy (\d+).+(?i)get (\d)+(.*)', price_string)
    if pattern:
        return dict(bool=True, buy=pattern.group(1), get=pattern.group(2), end=pattern.group(3))
    else:
        return dict(bool=False, price=price_string)


def x_for_y(price_string):
    pattern = re.search(r'([\d]+) (?i)for \$?([\d,\.]+)', price_string)
    if pattern:
        return dict(bool=True, price="{0:.2f}".format(float(pattern.group(2))), count=pattern.group(1),
                    eff_price="{0:.2f}".format(float(pattern.group(2))/float(pattern.group(1))))
    else:
        return dict(bool=False, price=price_string)


def fractional_reduction(price_string):
    pattern = re.search(r'.*((\d)/(\d))[\s]+(?i)price.*', price_string)
    if pattern:
        return dict(bool=True, fractional_reduction=pattern.group(1), price="{0:.0f}".format(100*(1-(float(pattern.group(2))/float(pattern.group(3))))))
    else:
        pattern = re.search(r'.*((\d)/(\d))[\s]+(?i)off.*', price_string)
        if pattern:
            return dict(bool=True, fractional_reduction=pattern.group(1), price="{0:.0f}".format(100*(float(pattern.group(2))/float(pattern.group(3)))))
        else:
            return dict(bool=False, price=price_string)


def percent_reduction(price_string):
    pattern = re.search(r'(.+)%[\s]+(?i)price', price_string)
    if pattern:
        return dict(bool=True, price="{0:.0f}".format(100 - float(pattern.group(1))))
    else:
        pattern = re.search(r'(.+)%[\s]+(?i)off', price_string)
        if pattern:
            return dict(bool=True, price=pattern.group(1))
        else:
            return dict(bool=False, price=price_string)


def price_range(price_string):
    pattern = re.search(r'.*\$([\d,\.]+) (?i)to \$([\d,\.]+).*', price_string)
    if pattern:
        return dict(bool=True, price=("{0:.2f}".format(
            float(pattern.group(1))), "{0:.2f}".format(float(pattern.group(2)))))
    else:
        return dict(bool=False, price=price_string)