# Regex2NER

# A lightweight Python tool for extracting and validating various data types from text using regex patterns.
## But can't NER models do this better?
### It's a trade-off. NER models excel at accuracy but are slow (milliseconds to seconds per operation), while this tool prioritizes speed over precision - operating in microseconds with accuracy that's sufficient for most use cases. Choose NER for complex entity recognition where context matters, choose RegexExtract for high-throughput scenarios where speed is critical and simple pattern matching suffices.

## Features

- Email addresses
- Cryptocurrency addresses (Bitcoin, Ethereum, Monero, etc.)
- Hash values (MD5, SHA1, SHA256, etc.)
- IP addresses and CIDRs (IPv4/IPv6)
- Domain names
- Phone numbers
- Social Security Numbers (SSNs)
- MAC addresses
- Credit card numbers

## Installation

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd regex-intelligence-enrichment
pip install -r requirements.txt
```

## Usage

### As a Library

```python
from main import extract_all

text = "Contact john@example.com or call 123-456-7890. BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
results = extract_all(text)
print(results)
```

### Command Line

```bash
python main.py "your text here"
```

## Licence: Apache 2.0
