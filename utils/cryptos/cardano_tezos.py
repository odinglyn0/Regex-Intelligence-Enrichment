import re
from typing import List

class Base58Validator:
    
    ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    @staticmethod
    def is_valid_base58(s: str) -> bool:
        if not s or s[0] in '0OIl':
            return False
        return all(c in Base58Validator.ALPHABET for c in s)

class CardanoExtractor:
    

    def __init__(self):
        self.mainnet_pattern = re.compile(r'\baddr1[a-z0-9]{98}\b')
        self.testnet_pattern = re.compile(r'\baddr_test1[a-z0-9]{98}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_mainnet(text))
        addresses.update(self.extract_testnet(text))
        return list(addresses)

    def extract_mainnet(self, text: str) -> List[str]:
        matches = self.mainnet_pattern.findall(text)
        return [m for m in matches if len(m) == 103]  

    def extract_testnet(self, text: str) -> List[str]:
        matches = self.testnet_pattern.findall(text)
        return [m for m in matches if len(m) == 109]  

class TezosExtractor:
    

    def __init__(self):
        self.tz1_pattern = re.compile(r'\btz1[1-9A-HJ-NP-Za-km-z]{33}\b')
        self.tz2_pattern = re.compile(r'\btz2[1-9A-HJ-NP-Za-km-z]{33}\b')
        self.tz3_pattern = re.compile(r'\btz3[1-9A-HJ-NP-Za-km-z]{33}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_tz1(text))
        addresses.update(self.extract_tz2(text))
        addresses.update(self.extract_tz3(text))
        return list(addresses)

    def extract_tz1(self, text: str) -> List[str]:
        matches = self.tz1_pattern.findall(text)
        return [m for m in matches if len(m) == 36 and Base58Validator.is_valid_base58(m)]

    def extract_tz2(self, text: str) -> List[str]:
        matches = self.tz2_pattern.findall(text)
        return [m for m in matches if len(m) == 36 and Base58Validator.is_valid_base58(m)]

    def extract_tz3(self, text: str) -> List[str]:
        matches = self.tz3_pattern.findall(text)
        return [m for m in matches if len(m) == 36 and Base58Validator.is_valid_base58(m)]