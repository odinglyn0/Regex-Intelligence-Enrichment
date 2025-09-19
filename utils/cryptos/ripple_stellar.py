import re
from typing import List

class Base58Validator:
    
    ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    @staticmethod
    def is_valid_base58(s: str) -> bool:
        if not s or s[0] in '0OIl':
            return False
        return all(c in Base58Validator.ALPHABET for c in s)

class Base32Validator:
    
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'

    @staticmethod
    def is_valid_base32(s: str) -> bool:
        return all(c in Base32Validator.ALPHABET for c in s)

class RippleExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\br[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 34 and Base58Validator.is_valid_base58(m)]

class StellarExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bG[A-Z2-7]{55}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 56 and Base32Validator.is_valid_base32(m[1:])]