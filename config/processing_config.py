# config/processing_config.py
"""
Data processing configuration - FIXED TYPE ANNOTATIONS
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ProcessingConfig:
    """Data processing configuration"""
    
    # Facility settings
    num_floors: int = 1
    top_n_heuristic_entrances: int = 5
    
    # Event filtering
    primary_positive_indicator: str = "ACCESS GRANTED"
    # FIXED: Use field(default_factory) instead of None
    invalid_phrases_exact: List[str] = field(default_factory=lambda: ["INVALID ACCESS LEVEL"])
    invalid_phrases_contain: List[str] = field(default_factory=lambda: ["NO ENTRY MADE"])
    
    # Cleaning thresholds
    same_door_scan_threshold_seconds: int = 10
    ping_pong_threshold_minutes: int = 1
    
    # Performance limits
    max_processing_time: int = 300  # 5 minutes
    chunk_size: int = 10000

def get_processing_config() -> ProcessingConfig:
    """Get processing configuration"""
    return ProcessingConfig()