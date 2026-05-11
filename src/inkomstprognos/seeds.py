"""Deterministic seed management for reproducible computations."""

from __future__ import annotations

import hashlib
import os
import random

import numpy as np

SYNTHETIC_SEED: int = 19960307
MODEL_SEED: int = 20251008


def set_global_seed(seed: int) -> None:
    """Seed all random number generators for reproducibility.

    Args:
        seed: Integer seed value.

    Returns:
        None.

    Raises:
        TypeError: If seed is not an integer.

    Examples:
        >>> set_global_seed(42)
    """
    if not isinstance(seed, int):
        msg = f"seed must be an integer, got {type(seed).__name__}"
        raise TypeError(msg)
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed % (2**32))
    try:
        import jax

        jax.config.update("jax_enable_custom_prng", True)
    except ImportError:
        pass


def derive_seed(base: int, *, namespace: str) -> int:
    """Derive a deterministic seed from a base seed and namespace.

    Uses SHA-256 hashing to produce a reproducible integer seed.

    Args:
        base: Base seed value.
        namespace: String namespace for domain separation.

    Returns:
        Derived integer seed in the range [0, 2**31).

    Raises:
        ValueError: If namespace is empty.

    Examples:
        >>> derive_seed(42, namespace="test")
        1033891752
    """
    if not namespace:
        msg = "namespace must be a non-empty string"
        raise ValueError(msg)
    digest = hashlib.sha256(f"{base}:{namespace}".encode()).hexdigest()
    return int(digest[:8], 16) % (2**31)
