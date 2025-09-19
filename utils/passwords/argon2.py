import re
import base64
from typing import List

class Argon2Validator:
    

    @staticmethod
    def is_valid_base64(s: str) -> bool:

        try:
            base64.b64decode(s, validate=True)
            return True
        except Exception:
            # Try adding padding
            for pad in ['', '=', '==']:
                try:
                    base64.b64decode(s + pad, validate=True)
                    return True
                except Exception:
                    pass
            return False

    @staticmethod
    def is_valid_version(version: str) -> bool:
        
        return version == '19'  

    @staticmethod
    def is_valid_memory(memory: str) -> bool:

        try:
            mem = int(memory)
            return 1 <= mem <= 2**32
        except ValueError:
            return False

    @staticmethod
    def is_valid_iterations(iterations: str) -> bool:
        
        try:
            it = int(iterations)
            return 1 <= it <= 2**32
        except ValueError:
            return False

    @staticmethod
    def is_valid_parallelism(parallelism: str) -> bool:
        
        try:
            par = int(parallelism)
            return 1 <= par <= 2**24
        except ValueError:
            return False

class Argon2Extractor:
    

    def __init__(self):
        
        self.pattern = re.compile(r'\$argon2(?:id|d|i)?\$.*')

    def extract_hashes(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_argon2(match):
                validated.append(match)
        return validated

    def _validate_argon2(self, candidate: str) -> bool:

        if not candidate.startswith(('$argon2i$', '$argon2d$', '$argon2id$')):
            return False

        parts = candidate.split('$')
        if len(parts) < 6:
            return False

        variant = parts[1]

        
        params = {}
        i = 2
        while i < len(parts) and '=' in parts[i]:
            for sub in parts[i].split(','):
                if '=' in sub:
                    key, value = sub.split('=', 1)
                    params[key] = value
            i += 1

        
        if i >= len(parts):
            return False
        salt_b64 = parts[i]
        i += 1

        
        if i >= len(parts):
            return False
        hash_b64 = parts[i]

        version = params.get('v')
        memory = params.get('m')
        iterations = params.get('t')
        parallelism = params.get('p')

        if not Argon2Validator.is_valid_version(version):
            return False

        if not Argon2Validator.is_valid_memory(memory):
            return False

        if not Argon2Validator.is_valid_iterations(iterations):
            return False

        if not Argon2Validator.is_valid_parallelism(parallelism):
            return False


        if not Argon2Validator.is_valid_base64(salt_b64):
            return False

        if not Argon2Validator.is_valid_base64(hash_b64):
            return False



        if len(salt_b64) != 22:
            return False


        if len(hash_b64) < 40:
            return False

        return True

    def extract_hashes_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            hash_str = match.group()
            if self._validate_argon2(hash_str):
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end]
                results.append({
                    'hash': hash_str,
                    'context': context
                })
        return results