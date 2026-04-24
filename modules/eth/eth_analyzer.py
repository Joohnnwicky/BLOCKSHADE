"""ETH transaction analyzer with address validation and Stargate detection.

Implements D-04: Query ETH transactions with user-provided API key.
Implements ADDR-05: API key passed per-request, never stored.
"""

import re
from typing import Dict, Any, List

from modules.core.api_client import get_eth_transactions, get_erc20_transfers
from .stargate_detector import detect_stargate_bridge


def is_valid_eth_address(address: str) -> bool:
    """Validate ETH address format.

    Args:
        address: Potential ETH address string

    Returns:
        True if address matches ETH format (0x prefix + 40 hex chars)
        False otherwise

    Threat model T-02-02-01 mitigation: Validate address format before API call.
    """
    if not address:
        return False
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))


def query_eth_transactions_web(address: str, api_key: str) -> Dict[str, Any]:
    """Query ETH transactions with user-provided API key.

    Implements D-04: Per-query API key input, no storage.
    Implements ADDR-05: API key passed as parameter, never stored in session/cookie.

    Args:
        address: ETH wallet address (0x prefix, 40 hex chars)
        api_key: User's Etherscan API key (per-query input)

    Returns:
        dict with keys:
            - success: bool
            - address: str
            - transactions: dict with normal, erc20, total_count
            - stargate_events: list of detected bridge events
            - error: str (if success=False)

    Security:
        - Address validated per threat model T-02-02-01
        - API key validated per threat model T-02-02-03
        - API key never logged per threat model T-02-02-02
    """
    # Validate ETH address format
    if not is_valid_eth_address(address):
        return {
            'success': False,
            'address': address,
            'error': '无效的ETH地址格式（应以0x开头，42位字符）',
            'transactions': None,
            'stargate_events': None
        }

    # Validate API key (minimum reasonable length)
    if not api_key or len(api_key) < 20:
        return {
            'success': False,
            'address': address,
            'error': '请输入有效的Etherscan API密钥',
            'transactions': None,
            'stargate_events': None
        }

    # Query normal ETH transactions
    # API key passed directly to function, never stored
    normal_txs = get_eth_transactions(address, api_key, limit=50)

    # Query ERC20 token transfers
    erc20_txs = get_erc20_transfers(address, api_key, limit=50)

    # Combine all transactions for Stargate detection
    all_txs = normal_txs + erc20_txs

    # Detect Stargate bridge events
    stargate_events = detect_stargate_bridge(all_txs)

    return {
        'success': True,
        'address': address,
        'transactions': {
            'normal': normal_txs,
            'erc20': erc20_txs,
            'total_count': len(all_txs)
        },
        'stargate_events': stargate_events,
        'error': None
    }