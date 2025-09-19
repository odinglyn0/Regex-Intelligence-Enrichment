import re
from typing import List

class HexValidator:
    
    HEX_CHARS = set('0123456789abcdefABCDEF')

    @staticmethod
    def is_valid_hex(s: str) -> bool:
        return all(c in HexValidator.HEX_CHARS for c in s)

    @staticmethod
    def is_potential_hash(s: str, expected_length: int) -> bool:
        return len(s) == expected_length and HexValidator.is_valid_hex(s)

class BLAKE2sExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\b[a-fA-F0-9]{32}\b')
        self.expected_length = 32

    def extract_hashes(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_blake2s(match):
                validated.append(match.lower())  
        return validated

    def _validate_blake2s(self, candidate: str) -> bool:
        
        if not HexValidator.is_potential_hash(candidate, self.expected_length):
            return False

        
        if candidate == '0' * self.expected_length:
            return False
        if len(set(candidate.lower())) == 1:
            return False

        
        return True

    def _calculate_entropy(self, s: str) -> float:
        
        from collections import Counter
        import math

        if not s:
            return 0.0

        char_counts = Counter(s.lower())
        length = len(s)
        entropy = 0.0

        for count in char_counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return entropy

    def extract_hashes_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            context = text[start:end]
            results.append({
                'hash': match.group().lower(),
                'context': context
            })
        return results