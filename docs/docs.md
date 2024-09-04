# Constants Documentation

## Overview

This document outlines the constants used in the XRP Market Bot project. These constants provide predefined values that are used across various modules of the application. They include internal constants for specific identifiers and limitations, as well as default values that can be overridden in the configuration file.

## Constants

### Internal Constants

These constants are used internally within the application and are not meant to be changed through configuration:

1. **XRP_ID**
   - Value: `"ripple"`
   - Purpose: Represents the Coingecko ID for XRP. This is used when making API calls to Coingecko to fetch XRP-specific data.

2. **MAX_TWEET_LENGTH**
   - Value: `280`
   - Purpose: Defines the maximum number of characters allowed in a tweet. This constant ensures that generated tweets comply with Twitter's character limit.

3. **MAX_TOKENS**
   - Value: `100`
   - Purpose: Specifies the maximum number of tokens for OpenAI API responses. This helps control the length and complexity of AI-generated content.

### Default Values

These constants provide default values that can be overridden in the `config.yaml` file:

1. **DEFAULT_DATABASE_NAME**
   - Value: `"xrp_market_bot.db"`
   - Purpose: Sets the default name for the SQLite database file. This value is used if no database name is specified in the configuration file.

## Usage

To use these constants in your code, import them from the `constants` module:

```python
from src.constants import XRP_ID, MAX_TWEET_LENGTH, MAX_TOKENS, DEFAULT_DATABASE_NAME

# Example usage
def fetch_xrp_data():
    return coingecko_api.get_coin_data(XRP_ID)

def generate_tweet(content):
    if len(content) > MAX_TWEET_LENGTH:
        raise ValueError("Tweet content exceeds maximum length")
    # ... rest of the function

def generate_ai_response(prompt):
    return openai_api.generate(prompt, max_tokens=MAX_TOKENS)

def get_database_name():
    return config.get('database', {}).get('name', DEFAULT_DATABASE_NAME)
```

## Best Practices

1. Use these constants instead of hard-coding values in your application logic. This makes the code more maintainable and reduces the risk of inconsistencies.
2. When adding new constants, consider whether they should be internal constants or default values that can be overridden in the configuration file.
3. Document any new constants added to this file, explaining their purpose and any relevant details about their usage.
4. If you need to change the value of an internal constant, be sure to review and update any code that depends on it.

## Customization

To add or modify constants:

1. For internal constants, simply add or update the constant in the `constants.py` file.
2. For default values that can be overridden, add the constant to `constants.py` and update the configuration loading logic in `config.py` to use this default value if not specified in `config.yaml`.

---

For any questions or issues regarding the constants, please contact the project maintainer.