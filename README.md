# cybersecurity-glossary

A searchable glossary of **60+ cybersecurity terms**, with definitions written to
be useful during study, onboarding and report writing. Includes a quiz mode that
pulls random terms so you can test recall.

## Features

- `data/terms.json`: terms, definitions and tags.
- Search across terms, definitions and tags.
- Look up one term, list by tag, or quiz yourself.
- JSON output for building flashcards or documentation.

## Installation

```bash
git clone https://github.com/victor-harden/cybersecurity-glossary.git
cd cybersecurity-glossary
```

## Usage

```bash
python3 glossary.py --search "injection"
python3 glossary.py --term "CVE"
python3 glossary.py --tag crypto
python3 glossary.py --random
python3 glossary.py --quiz 5
python3 glossary.py --list --json
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).
