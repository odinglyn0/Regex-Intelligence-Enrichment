import re
from typing import List

class SSNValidator:
    

    @staticmethod
    def is_valid_area_number(area: str) -> bool:
        
        area_int = int(area)
        return 1 <= area_int <= 899 and area_int not in [0, 666] and not (900 <= area_int <= 999)

    @staticmethod
    def is_valid_group_number(group: str) -> bool:
        
        group_int = int(group)
        return 1 <= group_int <= 99

    @staticmethod
    def is_valid_serial_number(serial: str) -> bool:
        
        serial_int = int(serial)
        return 1 <= serial_int <= 9999

class SSNExtractor:
    

    def __init__(self):
        
        self.pattern = re.compile(
            r'\b(\d{3})-(\d{2})-(\d{4})\b'
        )

    def extract_ssns(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            area, group, serial = match
            if self._validate_ssn(area, group, serial):
                validated.append(f"{area}-{group}-{serial}")
        return validated

    def _validate_ssn(self, area: str, group: str, serial: str) -> bool:
        
        try:
            if not SSNValidator.is_valid_area_number(area):
                return False
            if not SSNValidator.is_valid_group_number(group):
                return False
            if not SSNValidator.is_valid_serial_number(serial):
                return False

            
            
            full_ssn = f"{area}{group}{serial}"
            if full_ssn in ['078051120', '219099999', '457555462']:  
                return False

            
            if full_ssn == ''.join(str(i % 10) for i in range(len(full_ssn))):
                return False

            return True
        except ValueError:
            return False

    def extract_ssns_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            area, group, serial = match.groups()
            if self._validate_ssn(area, group, serial):
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end]
                results.append({
                    'ssn': f"{area}-{group}-{serial}",
                    'context': context
                })
        return results