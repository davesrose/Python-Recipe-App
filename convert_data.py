import unicodedata

class ConvertData:
    def convert_unicode_ascii(self, text):
        # vulgar fraction unicode to first convert
        fraction_codes = {
            "\u00bc": "1/4",
            "\u00bd": "1/2",
            "\u00be": "3/4",
            "\u2150": "1/7",
            "\u2151": "1/9",
            "\u2152": "1/10",
            "\u2153": "1/3",
            "\u2154": "2/3",
            "\u2155": "1/5",
            "\u2156": "2/5",
            "\u2157": "3/5",
            "\u2158": "4/5",
            "\u2159": "1/6",
            "\u215a": "5/6",
            "\u215b": "1/8",
            "\u215c": "3/8",
            "\u215d": "5/8",
            "\u215e": "7/8",
            "\u215f": "1/",
            "\u2189": "0/3",
        }
        for key in fraction_codes:
            if key == text[1] or key == text[2]:
                text = text.replace(key, " " + fraction_codes[key])
            else:
                text = text.replace(key, fraction_codes[key])

        return text
