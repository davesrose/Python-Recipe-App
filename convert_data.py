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
            text = text.replace(key, fraction_codes[key])
        """
            Converts a Unicode string with accented characters to its ASCII equivalent.
            Accents are removed, and characters not representable in ASCII are ignored.
            """
        # Normalize the string to NFD (Canonical Decomposition) form,
        # which separates base characters from diacritical marks.
        normalized_text = unicodedata.normalize('NFD', text)

        # Encode to ASCII, ignoring characters that cannot be encoded.
        # This effectively removes the diacritical marks and other non-ASCII characters.
        ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')

        return ascii_text