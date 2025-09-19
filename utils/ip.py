import re
import ipaddress
from typing import List, Union

class IPv4Extractor:
    

    def __init__(self):
        
        self.pattern = re.compile(
            r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'   
        )
        
        self.cidr_pattern = re.compile(
            r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'  
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/'   
            r'(?:[1-9]|[1-2][0-9]|3[0-2])\b'  
        )

    def extract_ips(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_ipv4(match):
                validated.append(match)
        return validated

    def extract_cidrs(self, text: str) -> List[str]:
        
        matches = self.cidr_pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_ipv4_cidr(match):
                validated.append(match)
        return validated

    def _validate_ipv4(self, candidate: str) -> bool:
        
        try:
            
            ipaddress.IPv4Address(candidate)
            return True
        except ipaddress.AddressValueError:
            return False

    def _validate_ipv4_cidr(self, candidate: str) -> bool:
        
        try:
            ipaddress.IPv4Network(candidate, strict=False)
            return True
        except (ipaddress.AddressValueError, ValueError):
            return False

    def extract_ips_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end]
            if self._validate_ipv4(match.group()):
                results.append({
                    'ip': match.group(),
                    'context': context
                })
        return results

class IPv6Extractor:
    

    def __init__(self):
        
        self.pattern = re.compile(
            r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|'  
            r'\b(?:[0-9a-fA-F]{1,4}:){1,7}:\b|'                
            r'\b(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}\b|' 
            r'\b::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}\b|'
            r'\b[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}\b|'
            r'\b[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}\b|'
            r'\b(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}\b|'
            r'\b(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}\b|'
            r'\b(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4}\b|'
            r'\b(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}::[0-9a-fA-F]{1,4}\b|'
            r'\b(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}::\b'
        )
        
        self.cidr_pattern = re.compile(
            r'\b(?:(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|'  
            r'(?:[0-9a-fA-F]{1,4}:){1,7}:|'                
            r'(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
            r'::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}|'
            r'[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}|'
            r'[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}|'
            r'(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}|'
            r'(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}|'
            r'(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4}|'
            r'(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}::[0-9a-fA-F]{1,4}|'
            r'(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}::)/'
            r'(?:[1-9]|[1-9][0-9]|1[0-1][0-9]|12[0-8])\b'  
        )

    def extract_ips(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_ipv6(match):
                validated.append(match.lower())
        return validated

    def extract_cidrs(self, text: str) -> List[str]:
        
        matches = self.cidr_pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_ipv6_cidr(match):
                validated.append(match.lower())
        return validated

    def _validate_ipv6(self, candidate: str) -> bool:
        
        try:
            ipaddress.IPv6Address(candidate)
            return True
        except ipaddress.AddressValueError:
            return False

    def _validate_ipv6_cidr(self, candidate: str) -> bool:
        
        try:
            ipaddress.IPv6Network(candidate, strict=False)
            return True
        except (ipaddress.AddressValueError, ValueError):
            return False

    def extract_ips_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end]
            if self._validate_ipv6(match.group()):
                results.append({
                    'ip': match.group().lower(),
                    'context': context
                })
        return results

class IPExtractor:
    

    def __init__(self):
        self.ipv4_extractor = IPv4Extractor()
        self.ipv6_extractor = IPv6Extractor()

    def extract_ips(self, text: str) -> dict:
        
        return {
            'ipv4': self.ipv4_extractor.extract_ips(text),
            'ipv6': self.ipv6_extractor.extract_ips(text),
            'cidr4': self.ipv4_extractor.extract_cidrs(text),
            'cidr6': self.ipv6_extractor.extract_cidrs(text)
        }

    def extract_all_ips(self, text: str) -> List[str]:
        
        ipv4 = self.ipv4_extractor.extract_ips(text)
        ipv6 = self.ipv6_extractor.extract_ips(text)
        cidr4 = self.ipv4_extractor.extract_cidrs(text)
        cidr6 = self.ipv6_extractor.extract_cidrs(text)
        return ipv4 + ipv6 + cidr4 + cidr6