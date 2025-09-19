import re
from typing import List

class Base58Validator:
    
    ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    @staticmethod
    def is_valid_base58(s: str) -> bool:
        if not s or s[0] in '0OIl':
            return False
        return all(c in Base58Validator.ALPHABET for c in s)

class MonacoinExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bM[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

class VertcoinExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bV[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

class SyscoinExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bS[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

class PeercoinExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bP[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

class PrimecoinExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bA[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

class NexusExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\bN[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]