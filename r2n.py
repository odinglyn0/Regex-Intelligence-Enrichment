import logging
from typing import List, Dict
from utils.email import EmailExtractor
from utils.cryptos.bitcoin_forks import BitcoinExtractor, BitcoinCashExtractor, BitcoinSVExtractor, BitcoinGoldExtractor, NamecoinExtractor
from utils.cryptos.ethereum_ecosystem import EthereumEcosystemExtractor
from utils.cryptos.privacy_coins import MoneroExtractor, ZcashExtractor, DashExtractor, VergeExtractor
from utils.cryptos.litecoin_derivatives import LitecoinExtractor, DogecoinExtractor, DigiByteExtractor, FeathercoinExtractor
from utils.cryptos.ripple_stellar import RippleExtractor, StellarExtractor
from utils.cryptos.cardano_tezos import CardanoExtractor, TezosExtractor
from utils.cryptos.other_cryptos import MonacoinExtractor, VertcoinExtractor, SyscoinExtractor, PeercoinExtractor, PrimecoinExtractor, NexusExtractor
from utils.hashes.md5 import MD5Extractor
from utils.hashes.sha1 import SHA1Extractor
from utils.hashes.sha224 import SHA224Extractor
from utils.hashes.sha256 import SHA256Extractor
from utils.hashes.sha384 import SHA384Extractor
from utils.hashes.sha512 import SHA512Extractor
from utils.hashes.blake2b import BLAKE2bExtractor
from utils.hashes.blake2s import BLAKE2sExtractor
from utils.hashes.blake3 import BLAKE3Extractor
from utils.passwords.bcrypt import BcryptExtractor
from utils.passwords.argon2 import Argon2Extractor
from utils.ip import IPExtractor
from utils.domain import DomainExtractor
from utils.phone import PhoneExtractor
from utils.ssn import SSNExtractor
from utils.mac import MACExtractor
from utils.card import CardExtractor


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailExtractionEngine:
    

    def __init__(self):
        self.extractor = EmailExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> List[str]:
        
        logger.info(f"Starting email extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            emails = self.extractor.extract_emails(text)
            logger.info(f"Extracted {len(emails)} unique emails")
            return emails
        except Exception as e:
            logger.error(f"Error during email extraction: {e}")
            raise

class CryptoExtractionEngine:
    

    def __init__(self):
        self.extractors = {
            'Bitcoin': BitcoinExtractor(),
            'BitcoinCash': BitcoinCashExtractor(),
            'BitcoinSV': BitcoinSVExtractor(),
            'BitcoinGold': BitcoinGoldExtractor(),
            'Namecoin': NamecoinExtractor(),
            'EthereumEcosystem': EthereumEcosystemExtractor(),
            'Monero': MoneroExtractor(),
            'Zcash': ZcashExtractor(),
            'Dash': DashExtractor(),
            'Verge': VergeExtractor(),
            'Litecoin': LitecoinExtractor(),
            'Dogecoin': DogecoinExtractor(),
            'DigiByte': DigiByteExtractor(),
            'Feathercoin': FeathercoinExtractor(),
            'Ripple': RippleExtractor(),
            'Stellar': StellarExtractor(),
            'Cardano': CardanoExtractor(),
            'Tezos': TezosExtractor(),
            'Monacoin': MonacoinExtractor(),
            'Vertcoin': VertcoinExtractor(),
            'Syscoin': SyscoinExtractor(),
            'Peercoin': PeercoinExtractor(),
            'Primecoin': PrimecoinExtractor(),
            'Nexus': NexusExtractor(),
        }
        self.extraction_count = 0

    def process_text(self, text: str) -> Dict[str, List[str]]:
        
        logger.info(f"Starting crypto address extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            results = {}
            total_addresses = 0
            for crypto, extractor in self.extractors.items():
                addresses = extractor.extract_addresses(text)
                if addresses:
                    results[crypto] = addresses
                    total_addresses += len(addresses)
            logger.info(f"Extracted {total_addresses} crypto addresses across {len(results)} types")
            return results
        except Exception as e:
            logger.error(f"Error during crypto extraction: {e}")
            raise

class HashExtractionEngine:
    

    def __init__(self):
        self.extractors = {
            'MD5': MD5Extractor(),
            'SHA1': SHA1Extractor(),
            'SHA224': SHA224Extractor(),
            'SHA256': SHA256Extractor(),
            'SHA384': SHA384Extractor(),
            'SHA512': SHA512Extractor(),
            'BLAKE2b': BLAKE2bExtractor(),
            'BLAKE2s': BLAKE2sExtractor(),
            'BLAKE3': BLAKE3Extractor(),
            'Bcrypt': BcryptExtractor(),
            'Argon2': Argon2Extractor(),
        }
        self.extraction_count = 0

    def process_text(self, text: str) -> Dict[str, List[str]]:
        
        logger.info(f"Starting hash extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            results = {}
            total_hashes = 0
            for hash_type, extractor in self.extractors.items():
                hashes = extractor.extract_hashes(text)
                if hashes:
                    results[hash_type] = hashes
                    total_hashes += len(hashes)
            logger.info(f"Extracted {total_hashes} hashes across {len(results)} types")
            return results
        except Exception as e:
            logger.error(f"Error during hash extraction: {e}")
            raise

class IPExtractionEngine:
    

    def __init__(self):
        self.extractor = IPExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> Dict[str, List[str]]:
        
        logger.info(f"Starting IP extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            ips = self.extractor.extract_ips(text)
            total_items = sum(len(v) for v in ips.values())
            logger.info(f"Extracted {total_items} IP addresses and CIDRs")
            return ips
        except Exception as e:
            logger.error(f"Error during IP extraction: {e}")
            raise

class DomainExtractionEngine:
    

    def __init__(self):
        self.extractor = DomainExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> List[str]:
        
        logger.info(f"Starting domain extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            domains = self.extractor.extract_domains(text)
            logger.info(f"Extracted {len(domains)} domains")
            return domains
        except Exception as e:
            logger.error(f"Error during domain extraction: {e}")
            raise

class PhoneExtractionEngine:
    

    def __init__(self):
        self.extractor = PhoneExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> List[str]:
        
        logger.info(f"Starting phone extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            phones = self.extractor.extract_phones(text)
            logger.info(f"Extracted {len(phones)} phone numbers")
            return phones
        except Exception as e:
            logger.error(f"Error during phone extraction: {e}")
            raise

class SSNExtractionEngine:
    

    def __init__(self):
        self.extractor = SSNExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> List[str]:
        
        logger.info(f"Starting SSN extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            ssns = self.extractor.extract_ssns(text)
            logger.info(f"Extracted {len(ssns)} SSNs")
            return ssns
        except Exception as e:
            logger.error(f"Error during SSN extraction: {e}")
            raise

class MACExtractionEngine:
    

    def __init__(self):
        self.extractor = MACExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> List[str]:
        
        logger.info(f"Starting MAC extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            macs = self.extractor.extract_macs(text)
            logger.info(f"Extracted {len(macs)} MAC addresses")
            return macs
        except Exception as e:
            logger.error(f"Error during MAC extraction: {e}")
            raise

class CardExtractionEngine:
    

    def __init__(self):
        self.extractor = CardExtractor()
        self.extraction_count = 0

    def process_text(self, text: str) -> List[str]:
        
        logger.info(f"Starting card extraction on text of length {len(text)}")
        self.extraction_count += 1

        try:
            cards = self.extractor.extract_cards(text)
            logger.info(f"Extracted {len(cards)} card numbers")
            return cards
        except Exception as e:
            logger.error(f"Error during card extraction: {e}")
            raise

def extract_emails(text: str) -> List[str]:
    
    engine = EmailExtractionEngine()
    return engine.process_text(text)

def extract_crypto_addresses(text: str) -> Dict[str, List[str]]:
    
    engine = CryptoExtractionEngine()
    return engine.process_text(text)

def extract_crypto_addresses(text: str) -> Dict[str, List[str]]:
    
    engine = CryptoExtractionEngine()
    return engine.process_text(text)

def extract_hashes(text: str) -> Dict[str, List[str]]:
    
    engine = HashExtractionEngine()
    return engine.process_text(text)

def extract_ips(text: str) -> Dict[str, List[str]]:
    
    engine = IPExtractionEngine()
    return engine.process_text(text)

def extract_domains(text: str) -> List[str]:
    
    engine = DomainExtractionEngine()
    return engine.process_text(text)

def extract_phones(text: str) -> List[str]:
    
    engine = PhoneExtractionEngine()
    return engine.process_text(text)

def extract_ssns(text: str) -> List[str]:
    
    engine = SSNExtractionEngine()
    return engine.process_text(text)

def extract_macs(text: str) -> List[str]:
    
    engine = MACExtractionEngine()
    return engine.process_text(text)

def extract_cards(text: str) -> List[str]:
    
    engine = CardExtractionEngine()
    return engine.process_text(text)

def extract_all(text: str) -> Dict[str, List[str]]:
    
    results = {}
    results['emails'] = list(set(extract_emails(text)))
    crypto_results = extract_crypto_addresses(text)
    for k, v in crypto_results.items():
        results[k] = list(set(v))
    hash_results = extract_hashes(text)
    for k, v in hash_results.items():
        results[k] = list(set(v))
    ip_results = extract_ips(text)
    results['ipv4'] = list(set(ip_results.get('ipv4', [])))
    results['cidr4'] = list(set(ip_results.get('cidr4', [])))
    results['ipv6'] = list(set(ip_results.get('ipv6', [])))
    results['cidr6'] = list(set(ip_results.get('cidr6', [])))
    results['domains'] = list(set(extract_domains(text)))
    results['phones'] = list(set(extract_phones(text)))
    results['ssns'] = list(set(extract_ssns(text)))
    results['macs'] = list(set(extract_macs(text)))
    results['cards'] = list(set(extract_cards(text)))
    return results

if __name__ == "__main__":

    import sys
    import time

    if len(sys.argv) < 2:
        print("Usage: python main.py 'text with emails, crypto addresses, hashes, IPs, domains, phones, SSNs, MACs, cards, and more'")
        sys.exit(1)

    text = ' '.join(sys.argv[1:])
    start_time = time.perf_counter_ns()
    all_extracted = extract_all(text)
    end_time = time.perf_counter_ns()
    exec_time_microseconds = int((end_time - start_time) / 1000)
    print("Extracted items:")
    for category, items in all_extracted.items():
        if items:
            print(f"{category}:")
            for item in items:
                print(f"  - {item}")
    print(f"EXEC_TIME: {exec_time_microseconds}MiS")
