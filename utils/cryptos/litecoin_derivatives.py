import re
from typing import List

class Base58Validator:
    
    ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    @staticmethod
    def is_valid_base58(s: str) -> bool:
        if not s or s[0] in '0OIl':
            return False
        return all(c in Base58Validator.ALPHABET for c in s)

class Bech32Validator:
    
    CHARSET = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'

    @staticmethod
    def is_valid_bech32(s: str, hrp: str) -> bool:
        if not s.startswith(hrp + '1'):
            return False
        data = s[len(hrp) + 1:]
        if len(data) < 6 or not all(c in Bech32Validator.CHARSET for c in data):
            return False
        return len(data) <= 90

class LitecoinExtractor:
    

    def __init__(self):
        self.legacy_pattern = re.compile(r'\bL[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.segwit_pattern = re.compile(r'\bM[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.bech32_pattern = re.compile(r'\bltc1[a-z0-9]{20,40}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_legacy(text))
        addresses.update(self.extract_segwit(text))
        addresses.update(self.extract_bech32(text))
        return list(addresses)

    def extract_legacy(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_segwit(self, text: str) -> List[str]:
        matches = self.segwit_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_bech32(self, text: str) -> List[str]:
        matches = self.bech32_pattern.findall(text)
        return [m for m in matches if Bech32Validator.is_valid_bech32(m, 'ltc')]

class DogecoinExtractor:
    

    def __init__(self):
        self.legacy_pattern = re.compile(r'\bD[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.segwit_pattern = re.compile(r'\bA[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.bech32_pattern = re.compile(r'\bdoge1[a-z0-9]{20,40}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_legacy(text))
        addresses.update(self.extract_segwit(text))
        addresses.update(self.extract_bech32(text))
        return list(addresses)

    def extract_legacy(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_segwit(self, text: str) -> List[str]:
        matches = self.segwit_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_bech32(self, text: str) -> List[str]:
        matches = self.bech32_pattern.findall(text)
        return [m for m in matches if Bech32Validator.is_valid_bech32(m, 'doge')]

class DigiByteExtractor:
    

    def __init__(self):
        self.legacy_pattern = re.compile(r'\bD[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.segwit_pattern = re.compile(r'\bS[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_legacy(text))
        addresses.update(self.extract_segwit(text))
        return list(addresses)

    def extract_legacy(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_segwit(self, text: str) -> List[str]:
        matches = self.segwit_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

class FeathercoinExtractor:
    

    def __init__(self):
        self.legacy_pattern = re.compile(r'\b[67][1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]