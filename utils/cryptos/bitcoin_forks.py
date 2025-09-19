import re
from typing import List, Set

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

class BitcoinExtractor:
    

    def __init__(self):
        self.p2pkh_pattern = re.compile(r'\b1[1-9A-HJ-NP-Za-km-z]{25,34}\b')
        self.p2sh_pattern = re.compile(r'\b3[1-9A-HJ-NP-Za-km-z]{25,34}\b')
        self.bech32_pattern = re.compile(r'\bbc1[a-z0-9]{20,40}\b')
        self.taproot_pattern = re.compile(r'\bbc1p[a-z0-9]{58}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_p2pkh(text))
        addresses.update(self.extract_p2sh(text))
        addresses.update(self.extract_bech32(text))
        addresses.update(self.extract_taproot(text))
        return list(addresses)

    def extract_p2pkh(self, text: str) -> List[str]:
        matches = self.p2pkh_pattern.findall(text)
        return [m for m in matches if self._validate_p2pkh(m)]

    def extract_p2sh(self, text: str) -> List[str]:
        matches = self.p2sh_pattern.findall(text)
        return [m for m in matches if self._validate_p2sh(m)]

    def extract_bech32(self, text: str) -> List[str]:
        matches = self.bech32_pattern.findall(text)
        return [m for m in matches if Bech32Validator.is_valid_bech32(m, 'bc')]

    def extract_taproot(self, text: str) -> List[str]:
        matches = self.taproot_pattern.findall(text)
        return [m for m in matches if Bech32Validator.is_valid_bech32(m, 'bc') and m.startswith('bc1p')]

    def _validate_p2pkh(self, addr: str) -> bool:
        return len(addr) >= 26 and len(addr) <= 35 and Base58Validator.is_valid_base58(addr)

    def _validate_p2sh(self, addr: str) -> bool:
        return len(addr) >= 26 and len(addr) <= 35 and Base58Validator.is_valid_base58(addr)

class BitcoinCashExtractor:
    

    def __init__(self):
        
        self.cashaddr_pattern = re.compile(r'\b(bitcoincash:)?[qp][a-z0-9]{41}\b', re.IGNORECASE)
        self.legacy_pattern = re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_cashaddr(text))
        addresses.update(self.extract_legacy(text))
        return list(addresses)

    def extract_cashaddr(self, text: str) -> List[str]:
        matches = self.cashaddr_pattern.findall(text)
        return [m for m in matches if self._validate_cashaddr(m)]

    def extract_legacy(self, text: str) -> List[str]:
        matches = self.legacy_pattern.findall(text)
        return [m for m in matches if self._validate_legacy(m)]

    def _validate_cashaddr(self, addr: str) -> bool:
        
        return len(addr) > 10 and ':' in addr or addr.startswith(('q', 'p'))

    def _validate_legacy(self, addr: str) -> bool:
        return len(addr) >= 26 and len(addr) <= 35 and Base58Validator.is_valid_base58(addr)

class BitcoinSVExtractor:
    

    def __init__(self):
        self.p2pkh_pattern = re.compile(r'\b1[1-9A-HJ-NP-Za-km-z]{25,34}\b')
        self.p2sh_pattern = re.compile(r'\b3[1-9A-HJ-NP-Za-km-z]{25,34}\b')
        self.bech32_pattern = re.compile(r'\bbc1[a-z0-9]{20,40}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_p2pkh(text))
        addresses.update(self.extract_p2sh(text))
        addresses.update(self.extract_bech32(text))
        return list(addresses)

    def extract_p2pkh(self, text: str) -> List[str]:
        matches = self.p2pkh_pattern.findall(text)
        return [m for m in matches if len(m) >= 26 and len(m) <= 35 and Base58Validator.is_valid_base58(m)]

    def extract_p2sh(self, text: str) -> List[str]:
        matches = self.p2sh_pattern.findall(text)
        return [m for m in matches if len(m) >= 26 and len(m) <= 35 and Base58Validator.is_valid_base58(m)]

    def extract_bech32(self, text: str) -> List[str]:
        matches = self.bech32_pattern.findall(text)
        return [m for m in matches if Bech32Validator.is_valid_bech32(m, 'bc')]

class BitcoinGoldExtractor:
    

    def __init__(self):
        self.p2pkh_pattern = re.compile(r'\b[AG][1-9A-HJ-NP-Za-km-z]{25,34}\b')  
        self.p2sh_pattern = re.compile(r'\b[8][1-9A-HJ-NP-Za-km-z]{25,34}\b')

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_p2pkh(text))
        addresses.update(self.extract_p2sh(text))
        return list(addresses)

    def extract_p2pkh(self, text: str) -> List[str]:
        matches = self.p2pkh_pattern.findall(text)
        return [m for m in matches if len(m) >= 26 and len(m) <= 35 and Base58Validator.is_valid_base58(m)]

    def extract_p2sh(self, text: str) -> List[str]:
        matches = self.p2sh_pattern.findall(text)
        return [m for m in matches if len(m) >= 26 and len(m) <= 35 and Base58Validator.is_valid_base58(m)]

class NamecoinExtractor:
    

    def __init__(self):
        self.p2pkh_pattern = re.compile(r'\b[NM][1-9A-HJ-NP-Za-km-z]{25,34}\b')  
        self.namecoin_specific_pattern = re.compile(r'\bid-[a-z0-9]+\b', re.IGNORECASE)  

    def extract_addresses(self, text: str) -> List[str]:
        addresses = set()
        addresses.update(self.extract_p2pkh(text))
        addresses.update(self.extract_namecoin_ids(text))
        return list(addresses)

    def extract_p2pkh(self, text: str) -> List[str]:
        matches = self.p2pkh_pattern.findall(text)
        return [m for m in matches if len(m) >= 26 and len(m) <= 35 and Base58Validator.is_valid_base58(m)]

    def extract_namecoin_ids(self, text: str) -> List[str]:
        matches = self.namecoin_specific_pattern.findall(text)
        return [m for m in matches if self._validate_namecoin_id(m)]

    def _validate_namecoin_id(self, addr: str) -> bool:
        return addr.startswith('id-') and len(addr) > 3