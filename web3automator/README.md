# Installation

```
python3 -m venv venv
source ./venv/bin/activate
pip install web3

cp config/wallets_example.json config/wallets.json
```

# Setup

Setup config/config.json
Setup config/wallets.json with your data in format:

```
[
    {
        "name": "Wallet1",
        "eth": ["public_address", "private_key"],
        "stark": ["public_address", "private_key"]
    },
    {
        "name": "Wallet2",
        "eth": ["public_address", "private_key"],
        "stark": ["public_address", "private_key"]
    }
]
```

**name** - some name just for your convenience



# Run

```
python main.py
```