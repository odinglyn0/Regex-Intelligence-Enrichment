import re
from typing import List, Dict, Set

class CountryCodeValidator:
    

    
    VALID_COUNTRY_CODES: Set[str] = {
        '1', '7', '20', '27', '30', '31', '32', '33', '34', '36', '39', '40', '41', '43', '44', '45', '46', '47', '48', '49',
        '51', '52', '53', '54', '55', '56', '57', '58', '60', '61', '62', '63', '64', '65', '66', '81', '82', '84', '86', '90',
        '91', '92', '93', '94', '95', '98', '212', '213', '216', '218', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229',
        '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249',
        '250', '251', '252', '253', '254', '255', '256', '257', '258', '260', '261', '262', '263', '264', '265', '266', '267', '268', '269',
        '290', '291', '297', '298', '299', '350', '351', '352', '353', '354', '355', '356', '357', '358', '359', '370', '371', '372', '373', '374',
        '375', '376', '377', '378', '380', '381', '382', '383', '385', '386', '387', '389', '420', '421', '423', '500', '501', '502', '503', '504', '505', '506', '507', '508', '509',
        '590', '591', '592', '593', '594', '595', '596', '597', '598', '599', '670', '672', '673', '674', '675', '676', '677', '678', '679', '680',
        '681', '682', '683', '684', '685', '686', '687', '688', '689', '690', '691', '692', '850', '852', '853', '855', '856', '880', '886', '960', '961', '962', '963', '964', '965', '966', '967', '968', '970', '971', '972', '973', '974', '975', '976', '977', '992', '993', '994', '995', '996', '998',
        
        '1', '1242', '1246', '1264', '1268', '1284', '1340', '1345', '1441', '1473', '1649', '1664', '1670', '1671', '1684', '1721', '1758', '1767', '1784', '1787', '1809', '1829', '1849', '1868', '1869', '1876', '1939', '441481', '441534', '441624', '441639', '473', '649', '671', '684', '689', '767', '809', '829', '849', '868', '869', '876', '939', '970', '971', '972', '973', '974', '975', '976', '977', '992', '993', '994', '995', '996', '998'
    }

    @staticmethod
    def is_valid_country_code(code: str) -> bool:
        return code in CountryCodeValidator.VALID_COUNTRY_CODES

class PhoneExtractor:
    

    def __init__(self):
        
        
        self.pattern = re.compile(
            r'\+\s*(\d{1,4})\s*[\(\)\-\.\s/]*'  
            r'(\d[\(\)\-\.\s/\d]*\d)'  
            r'(?:\s*[\(\)\-\.\s/]*\d[\(\)\-\.\s/\d]*)*',  
            re.VERBOSE
        )

    def extract_phones(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            country_code, number_part = match
            full_number = f"+{country_code}{number_part}"
            if self._validate_phone(full_number):
                standardized = self._standardize_phone(full_number)
                validated.append(standardized)
        return validated

    def _validate_phone(self, candidate: str) -> bool:
        
        
        cleaned = re.sub(r'[^\d+]', '', candidate)
        if not cleaned.startswith('+'):
            return False

        digits_only = cleaned[1:]  

        
        country_code = digits_only[:4] if len(digits_only) >= 4 else digits_only
        for i in range(1, len(country_code) + 1):
            if CountryCodeValidator.is_valid_country_code(digits_only[:i]):
                country_code = digits_only[:i]
                break
        else:
            return False  

        if not CountryCodeValidator.is_valid_country_code(country_code):
            return False

        
        total_digits = len(digits_only)
        if total_digits < 7 or total_digits > 15:  
            return False

        
        if re.search(r'(\d)\1{5,}', cleaned):  
            return False

        return True

    def _standardize_phone(self, phone: str) -> str:
        
        
        return re.sub(r'[^\d+]', '', phone)

    def extract_phones_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            country_code, number_part = match.groups()
            full_number = f"+{country_code}{number_part}"
            if self._validate_phone(full_number):
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                results.append({
                    'phone': self._standardize_phone(full_number),
                    'context': context
                })
        return results