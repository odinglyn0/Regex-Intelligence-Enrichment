import re
from typing import List

class LuhnValidator:
    

    @staticmethod
    def is_valid_luhn(card_num: str) -> bool:
        
        if not card_num.isdigit():
            return False

        digits = [int(d) for d in card_num[::-1]]  

        for i in range(1, len(digits), 2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

        return sum(digits) % 10 == 0

class CardExtractor:
    

    def __init__(self):
        
        self.single_word_pattern = re.compile(r'\b\d{13,19}\b')  
        self.dash_pattern = re.compile(r'\b\d{4}(?:-\d{4}){3}\b')  
        self.space_pattern = re.compile(r'\b\d{4}(?: \d{4}){3}\b')  

    def extract_cards(self, text: str) -> List[str]:
        
        cards = set()

        
        cards.update(self._extract_from_pattern(text, self.single_word_pattern))
        cards.update(self._extract_from_pattern(text, self.dash_pattern))
        cards.update(self._extract_from_pattern(text, self.space_pattern))

        return list(cards)

    def _extract_from_pattern(self, text: str, pattern: re.Pattern) -> List[str]:
        
        matches = pattern.findall(text)
        validated = []
        for match in matches:
            clean_card = self._clean_card_number(match)
            if self._validate_card(clean_card):
                validated.append(clean_card)
        return validated

    def _clean_card_number(self, card: str) -> str:
        
        return re.sub(r'[^\d]', '', card)

    def _validate_card(self, card: str) -> bool:
        
        if not card.isdigit():
            return False

        length = len(card)
        if length < 13 or length > 19:
            return False

        
        if not LuhnValidator.is_valid_luhn(card):
            return False

        
        
        if card in ['4111111111111111', '5555555555554444', '378282246310005']:
            return False  

        
        if card == ''.join(str(i % 10) for i in range(length)):
            return False

        
        if len(set(card)) == 1:
            return False

        
        bin_code = card[:6]
        if not self._is_valid_bin(bin_code):
            return False

        return True

    def _is_valid_bin(self, bin_code: str) -> bool:
        
        
        
        
        
        
        
        
        

        if bin_code.startswith('4'):
            return True  
        if bin_code.startswith('5') and bin_code[1] in '12345':
            return True  
        if bin_code.startswith('3') and bin_code[1] in '47':
            return True  
        if bin_code.startswith('6') and bin_code[1] in '0245':
            return True  
        if bin_code.startswith('3') and bin_code[1] in '068':
            return True  
        if bin_code.startswith('35'):
            return True  

        
        return True

    def extract_cards_with_context(self, text: str) -> List[dict]:
        
        results = []
        all_patterns = [self.single_word_pattern, self.dash_pattern, self.space_pattern]

        for pattern in all_patterns:
            for match in pattern.finditer(text):
                card = match.group()
                clean_card = self._clean_card_number(card)
                if self._validate_card(clean_card):
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    results.append({
                        'card': clean_card,
                        'context': context
                    })

        
        seen = set()
        unique_results = []
        for result in unique_results:
            if result['card'] not in seen:
                seen.add(result['card'])
                unique_results.append(result)

        return unique_results