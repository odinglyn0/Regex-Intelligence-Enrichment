import re
from typing import List

class MACValidator:
    

    @staticmethod
    def is_valid_hex(s: str) -> bool:
        
        return all(c in '0123456789abcdefABCDEF' for c in s)

    @staticmethod
    def normalize_mac(mac: str) -> str:
        
        
        clean = re.sub(r'[:\-\.]', '', mac)
        if len(clean) != 12:
            return mac
        
        return ':'.join(clean[i:i+2] for i in range(0, 12, 2)).upper()

class MACExtractor:
    

    def __init__(self):
        
        self.colon_pattern = re.compile(r'\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b')  
        self.dash_pattern = re.compile(r'\b(?:[0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}\b')   

    def extract_macs(self, text: str) -> List[str]:
        
        macs = set()

        
        macs.update(self._extract_from_pattern(text, self.colon_pattern))
        macs.update(self._extract_from_pattern(text, self.dash_pattern))

        return list(macs)

    def _extract_from_pattern(self, text: str, pattern: re.Pattern) -> List[str]:
        
        matches = pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_mac(match):
                normalized = MACValidator.normalize_mac(match)
                validated.append(normalized)
        return validated

    def _validate_mac(self, candidate: str) -> bool:
        
        
        clean = re.sub(r'[:\-\.]', '', candidate)

        if len(clean) != 12:
            return False

        if not MACValidator.is_valid_hex(clean):
            return False

        
        
        if clean.upper() == 'FFFFFFFFFFFF':
            return True  

        
        first_byte = int(clean[:2], 16)
        if first_byte & 0x01:
            pass  

        
        if first_byte & 0x02:
            pass  

        return True

    def extract_macs_with_context(self, text: str) -> List[dict]:
        
        results = []
        all_patterns = [self.colon_pattern, self.dash_pattern, self.dot_pattern, self.no_sep_pattern]

        for pattern in all_patterns:
            for match in pattern.finditer(text):
                mac = match.group()
                if self._validate_mac(mac):
                    start = max(0, match.start() - 40)
                    end = min(len(text), match.end() + 40)
                    context = text[start:end]
                    results.append({
                        'mac': MACValidator.normalize_mac(mac),
                        'context': context
                    })

        
        seen = set()
        unique_results = []
        for result in results:
            if result['mac'] not in seen:
                seen.add(result['mac'])
                unique_results.append(result)

        return unique_results