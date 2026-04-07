# WarEraAPI (unofficial)

An API client for the online multiplayer game WarEra written in Python.

## Overview

WarEraAPI is an asynchronous Python client that provides access to (most of) the WarEra game API. It allows developers to interact with various aspects of the game including companies, battles, users, articles, MUs, and more.

## Features

- **Comprehensive API Coverage**: Access to most WarEra API endpoints
- **Asynchronous Support**: Built with `aiohttp` for efficient async operations
- **Type Safety**: Full type hints and data models for all API responses
- **Pagination Support**: Built-in pagination handling for large datasets
- **Rate Limiting Support**: yeah, thats it

## Installation

```bash
pip install WarEraAPI
```

## Requirements

- Python 3.10+
- aiohttp>=3.13.4

## Quick Start

```python
import asyncio
from WarEraAPI import WarEraClient

async def main():
    # Initialize client with API key (optional)
    client = WarEraClient(api_key="your_api_key_here")
    
    # Get user information
    user = await client.get_user(userId="user_id_here")
    print(user)
    
    # Get 3 active battles
    battles = await client.get_battles(limit=3, isActive=True)
    print(battles)
    
    # Get company information
    company = await client.get_company(companyId="company_id_here")
    print(company)

# Run the async function
asyncio.run(main())
```


### Check [Documentation](https://wareraapi.readthedocs.io/en/latest/)!

## Development

This project is currently in development and provides access to most of the WarEra API. The full API is not fully documented in the current time so further developments intend to support as much from the api as possible

### Currently Unsupported Documented Endpoints

* battleRanking
  * getRanking
* itemOffer
  * getById
* gameConfig
  * getGameConfig

### Roadmap

- [ ] adding use examples
- [ ] documenting types
- [ ] implementing the unsupported endpoints
- [ ] add more abstract/QOL methods

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

- **Author**: SpicyPenguin
- **Email**: kerolisand@gmail.com