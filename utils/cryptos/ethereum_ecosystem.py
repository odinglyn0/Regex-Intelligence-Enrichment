import re
import hashlib
from typing import List

class EthereumBaseExtractor:
    

    def __init__(self):
        self.pattern = re.compile(r'\b0x[a-fA-F0-9]{40}\b')

    def extract_addresses(self, text: str) -> List[str]:
        matches = self.pattern.findall(text)
        return [m for m in matches if self._validate_address(m)]

    def _validate_address(self, addr: str) -> bool:
        
        if not addr.startswith('0x') or len(addr) != 42:
            return False
        addr_lower = addr.lower()
        addr_hash = hashlib.sha3_256(addr_lower[2:].encode()).hexdigest()
        for i in range(40):
            expected_case = addr_hash[i] in '89abcdef'
            actual_upper = addr[i+2].isupper()
            if expected_case != actual_upper:
                return False
        return True

class EthereumExtractor(EthereumBaseExtractor):
    
    pass  

class EthereumClassicExtractor(EthereumBaseExtractor):
    
    pass  

class ArbitrumExtractor(EthereumBaseExtractor):
    
    pass

class AvalancheExtractor(EthereumBaseExtractor):
    
    pass

class PolygonExtractor(EthereumBaseExtractor):
    
    pass

class OptimismExtractor(EthereumBaseExtractor):
    
    pass

class BinanceSmartChainExtractor(EthereumBaseExtractor):
    
    pass

class FantomExtractor(EthereumBaseExtractor):
    
    pass

class XDaiExtractor(EthereumBaseExtractor):
    
    pass


class EthereumEcosystemExtractor:
    

    def __init__(self):
        self.extractors = {
            'ETH': EthereumExtractor(),
            'ETC': EthereumClassicExtractor(),
            'ARB': ArbitrumExtractor(),
            'AVAX': AvalancheExtractor(),
            'MATIC': PolygonExtractor(),
            'OP': OptimismExtractor(),
            'BSC': BinanceSmartChainExtractor(),
            'FTM': FantomExtractor(),
            'GNO': XDaiExtractor(),
        }

    def extract_all_addresses(self, text: str) -> dict:
        
        results = {}
        for chain, extractor in self.extractors.items():
            addresses = extractor.extract_addresses(text)
            if addresses:
                results[chain] = addresses
        return results

    def extract_addresses(self, text: str) -> List[str]:
        
        all_addresses = set()
        for extractor in self.extractors.values():
            all_addresses.update(extractor.extract_addresses(text))
        return list(all_addresses)