import re
from typing import List, Set

class TLDValidator:
    
    
    COMMON_TLDS = {
        'com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'info', 'biz', 'name', 'pro', 'coop', 'aero', 'museum', 'travel',
        'cat', 'jobs', 'mobi', 'tel', 'asia', 'post', 'geo', 'coop', 'travel', 'xxx', 'arpa',
        
        'us', 'uk', 'de', 'fr', 'it', 'es', 'ca', 'au', 'jp', 'cn', 'in', 'br', 'mx', 'ru', 'za', 'kr', 'tr', 'nl', 'se', 'no', 'fi', 'dk', 'pl', 'cz', 'sk', 'hu', 'ro', 'bg', 'hr', 'si', 'ee', 'lv', 'lt', 'mt', 'cy', 'gr', 'pt', 'es', 'it', 'sm', 'va', 'mc', 'li', 'ch', 'at', 'be', 'lu', 'nl', 'de', 'dk', 'se', 'no', 'fi', 'is', 'fo', 'gl', 'sj', 'ax', 'gb', 'ie', 'im', 'gg', 'je', 'gs', 'sh', 'pn', 'io', 'ac', 'uk', 'eu', 'cat', 'coop', 'int', 'gov', 'edu', 'mil', 'arpa',
        
        'academy', 'accountants', 'active', 'actor', 'adult', 'aero', 'agency', 'airforce', 'apartments', 'app', 'archi', 'army', 'associates', 'attorney', 'auction', 'audio', 'autos', 'band', 'bank', 'bar', 'bargains', 'beer', 'best', 'bid', 'bike', 'bingo', 'bio', 'biz', 'black', 'blackfriday', 'blog', 'blue', 'boo', 'boutique', 'build', 'builders', 'business', 'buzz', 'cab', 'camera', 'camp', 'cancerresearch', 'capital', 'cards', 'care', 'career', 'careers', 'cash', 'casino', 'catering', 'center', 'ceo', 'channel', 'chat', 'cheap', 'christmas', 'church', 'city', 'claims', 'cleaning', 'clinic', 'clothing', 'cloud', 'club', 'coach', 'codes', 'coffee', 'college', 'community', 'company', 'computer', 'condos', 'construction', 'consulting', 'contractors', 'cooking', 'cool', 'coop', 'country', 'coupons', 'credit', 'creditcard', 'cricket', 'cruises', 'dad', 'dance', 'dating', 'day', 'deal', 'degree', 'delivery', 'democrat', 'dental', 'dentist', 'design', 'dev', 'diamonds', 'diet', 'digital', 'direct', 'directory', 'discount', 'doctor', 'dog', 'domains', 'download', 'earth', 'education', 'email', 'energy', 'engineer', 'engineering', 'enterprises', 'equipment', 'estate', 'events', 'exchange', 'expert', 'exposed', 'express', 'fail', 'faith', 'family', 'fans', 'farm', 'fashion', 'film', 'finance', 'financial', 'fish', 'fishing', 'fit', 'fitness', 'flights', 'florist', 'flowers', 'fm', 'football', 'forsale', 'foundation', 'fun', 'fund', 'furniture', 'futbol', 'fyi', 'gallery', 'garden', 'gift', 'gifts', 'gives', 'glass', 'global', 'gold', 'golf', 'graphics', 'gratis', 'green', 'gripe', 'group', 'guide', 'guitars', 'guru', 'hair', 'healthcare', 'help', 'hiphop', 'hockey', 'holdings', 'holiday', 'homes', 'horse', 'host', 'hosting', 'house', 'how', 'icu', 'immo', 'immobilien', 'industries', 'ink', 'institute', 'insure', 'international', 'investments', 'io', 'irish', 'jewelry', 'juegos', 'kaufen', 'kim', 'kitchen', 'land', 'law', 'lawyer', 'lease', 'legal', 'lgbt', 'life', 'lighting', 'limited', 'limo', 'link', 'live', 'loan', 'loans', 'lol', 'london', 'love', 'ltd', 'luxury', 'maison', 'management', 'market', 'marketing', 'mba', 'media', 'meet', 'meme', 'memorial', 'men', 'menu', 'miami', 'mobi', 'moda', 'moe', 'money', 'mortgage', 'motorcycles', 'mov', 'movie', 'museum', 'name', 'navy', 'network', 'new', 'news', 'ninja', 'nyc', 'one', 'online', 'ooo', 'organic', 'partners', 'parts', 'party', 'pet', 'photo', 'photography', 'photos', 'physio', 'pics', 'pictures', 'pink', 'pizza', 'place', 'plumbing', 'plus', 'poker', 'porn', 'press', 'pro', 'productions', 'promo', 'properties', 'property', 'protection', 'pub', 'qpon', 'racing', 'realty', 'recipes', 'red', 'rehab', 'rent', 'rentals', 'repair', 'report', 'republican', 'rest', 'restaurant', 'review', 'reviews', 'rich', 'rip', 'rocks', 'rodeo', 'rsvp', 'run', 'sale', 'salon', 'sarl', 'school', 'schule', 'science', 'security', 'services', 'sex', 'sexy', 'shoes', 'shop', 'shopping', 'show', 'singles', 'site', 'ski', 'skin', 'soccer', 'social', 'software', 'solar', 'solutions', 'space', 'sport', 'storage', 'store', 'stream', 'studio', 'study', 'style', 'sucks', 'supplies', 'supply', 'support', 'surf', 'surgery', 'systems', 'tattoo', 'tax', 'taxi', 'team', 'tech', 'technology', 'tel', 'tennis', 'theater', 'theatre', 'tickets', 'tienda', 'tips', 'tires', 'today', 'tokyo', 'tools', 'top', 'tours', 'town', 'toys', 'trade', 'training', 'travel', 'university', 'uno', 'vacations', 'ventures', 'vet', 'video', 'villas', 'vin', 'vip', 'vision', 'vodka', 'vote', 'voting', 'voto', 'voyage', 'watch', 'webcam', 'website', 'wed', 'wedding', 'whoswho', 'wiki', 'win', 'wine', 'work', 'works', 'world', 'wtf', 'xxx', 'xyz', 'yoga', 'zone',
        
    }

    @staticmethod
    def is_valid_tld(tld: str) -> bool:
        return tld.lower() in TLDValidator.COMMON_TLDS

class DomainExtractor:
    

    def __init__(self):
        
        self.pattern = re.compile(
            r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'  
            r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.'  
            r'[a-zA-Z]{2,}\b',  
            re.IGNORECASE
        )

    def extract_domains(self, text: str) -> List[str]:
        
        matches = self.pattern.findall(text)
        validated = []
        for match in matches:
            if self._validate_domain(match):
                validated.append(match.lower())
        return validated

    def _validate_domain(self, candidate: str) -> bool:
        
        if not candidate or len(candidate) > 253:
            return False

        parts = candidate.split('.')
        if len(parts) < 2:
            return False

        tld = parts[-1]
        if not TLDValidator.is_valid_tld(tld):
            return False

        
        for label in parts[:-1]:  
            if not label or len(label) > 63:
                return False
            if label.startswith('-') or label.endswith('-'):
                return False
            if not re.match(r'^[a-zA-Z0-9-]+$', label):
                return False

        
        if 'xn--' in candidate:
            
            pass

        return True

    def extract_domains_with_context(self, text: str) -> List[dict]:
        
        results = []
        for match in self.pattern.finditer(text):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end]
            if self._validate_domain(match.group()):
                results.append({
                    'domain': match.group().lower(),
                    'context': context
                })
        return results