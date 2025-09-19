import re
from typing import List, Set

class EmailExtractor:
    

    def __init__(self):
        
        
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            re.IGNORECASE
        )

        
        self.backup_patterns = [
            re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b'),
            re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b'),
        ]

    def extract_emails(self, text: str) -> List[str]:
        
        emails = set()

        
        primary_matches = self.email_pattern.findall(text)
        emails.update(primary_matches)

        
        for pattern in self.backup_patterns:
            backup_matches = pattern.findall(text)
            emails.update(backup_matches)

        
        validated_emails = [email for email in emails if self._validate_email(email)]

        return list(validated_emails)

    def _validate_email(self, email: str) -> bool:
        
        
        if len(email) > 254 or len(email) < 3:
            return False

        
        if email.count('@') != 1:
            return False

        
        local, domain = email.split('@')

        
        if not local or len(local) > 64:
            return False

        
        if not domain or '.' not in domain:
            return False

        
        if '..' in email:
            return False

        return True

    def extract_emails_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.email_pattern.finditer(text):
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            context = text[start:end]
            results.append({
                'email': match.group(),
                'context': context
            })
        return results