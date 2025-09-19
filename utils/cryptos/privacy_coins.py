import re
from typing import List

class Base58Validator:
    
    ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    @staticmethod
    def is_valid_base58(s: str) -> bool:
        if not s or s[0] in '0OIl':
            return False
        return all(c in Base58Validator.ALPHABET for c in s)

class MoneroExtractor:
    

    def __init__(self):
        self.stealth_pattern = re.compile(r'\b[48][0-9A-Za-z]{94}\b')

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.stealth_pattern.findall(text)
        return [m for m in matches if self._validate_stealth(m)]

    def _validate_stealth(self, addr: str) -> bool:
        return len(addr) == 95 and Base58Validator.is_valid_base58(addr)

class ZcashExtractor:
    

    def __init__(self):
        self.shielded_pattern = re.compile(r'\bz[ct][0-9A-Za-z]{93}\b')  
        self.transparent_pattern = re.compile(r'\bt1[0-9A-Za-z]{33}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_shielded(text))
        addresses.update(self.extract_transparent(text))
        return list(addresses)

    def extract_shielded(self, text: str) -> List[str]:
        matches = self.shielded_pattern.findall(text)
        return [m for m in matches if self._validate_shielded(m)]

    def extract_transparent(self, text: str) -> List[str]:
        matches = self.transparent_pattern.findall(text)
        return [m for m in matches if self._validate_transparent(m)]

    def _validate_shielded(self, addr: str) -> bool:
        return len(addr) == 95 and addr.startswith(('zc', 'zt')) and Base58Validator.is_valid_base58(addr)

    def _validate_transparent(self, addr: str) -> bool:
        return len(addr) == 35 and addr.startswith('t1') and Base58Validator.is_valid_base58(addr)

class DashExtractor:
    

    def __init__(self):
        self.legacy_pattern = re.compile(r'\bX[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.privatesend_pattern = re.compile(r'\bX[1-9A-HJ-NP-Za-km-z]{33}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_legacy(text))
        addresses.update(self.extract_privatesend(text))
        return list(addresses)

    def extract_legacy(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_privatesend(self, text: str) -> List[str]:
        
        matches = self.privatesend_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m) and self._is_privatesend(m)]

    def _is_privatesend(self, addr: str) -> bool:
        
        return True

class VergeExtractor:
    

    def __init__(self):
        self.legacy_pattern = re.compile(r'\bD[1-9A-HJ-NP-Za-km-z]{33}\b')  
        self.wraith_pattern = re.compile(r'\b[48][0-9A-Za-z]{94}\b')  

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_legacy(text))
        addresses.update(self.extract_wraith(text))
        return list(addresses)

    def extract_legacy(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if len(m) == 35 and Base58Validator.is_valid_base58(m)]

    def extract_wraith(self, text: str) -> List[str]:
        matches = self.wraith_pattern.findall(text)
        return [m for m in matches if len(m) == 95 and Base58Validator.is_valid_base58(m)]