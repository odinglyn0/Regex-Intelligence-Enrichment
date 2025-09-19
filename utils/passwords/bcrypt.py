import re
from typing import List

class BcryptValidator:
    

    BASE64_CHARS = './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    @staticmethod
    def is_valid_base64_bcrypt(s: str) -> bool:
        
        return all(c in BcryptValidator.BASE64_CHARS for c in s)

    @staticmethod
    def is_valid_cost(cost: str) -> bool:
        
        try:
            cost_int = int(cost)
            return 4 <= cost_int <= 31  
        except ValueError:
            return False

class BcryptExtractor:
    

    def __init__(self):
        
        
        self.pattern = re.compile(r'\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}')

    def extract_hashes(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_bcrypt(match):
                validated.append(match)
        return validated

    def _validate_bcrypt(self, candidate: str) -> bool:
        
        if not candidate.startswith(('$2a$', '$2b$', '$2y$')):
            return False

        parts = candidate.split('$')
        if len(parts) != 4:
            return False

        version, cost, salt_and_hash = parts[1], parts[2], parts[3]

        if not BcryptValidator.is_valid_cost(cost):
            return False

        if len(salt_and_hash) != 53:
            return False

        salt = salt_and_hash[:22]
        hash_part = salt_and_hash[22:]

        if len(salt) != 22 or len(hash_part) != 31:
            return False

        if not BcryptValidator.is_valid_base64_bcrypt(salt):
            return False

        if not BcryptValidator.is_valid_base64_bcrypt(hash_part):
            return False

        
        
        if candidate in ['$2a$10$abcdefghijklmnopqrsABCDEFGHIJ', '$2b$10$abcdefghijklmnopqrsABCDEFGHIJ']:
            return False

        return True

    def extract_hashes_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            hash_str = match.group()
            if self._validate_bcrypt(hash_str):
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end]
                results.append({
                    'hash': hash_str,
                    'context': context
                })
        return results