# config/processing_config.py
"""
Data processing configuration
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ProcessingConfig:
    """Data processing configuration"""
    
    # Facility settings
    num_floors: int = 1
    top_n_heuristic_entrances: int = 5
    
    # Event filtering
    primary_positive_indicator: str = "ACCESS GRANTED"
    invalid_phrases_exact: List[str] = None
    invalid_phrases_contain: List[str] = None
    
    # Cleaning thresholds
    same_door_scan_threshold_seconds: int = 10
    ping_pong_threshold_minutes: int = 1
    
    # Performance limits
    max_processing_time: int = 300  # 5 minutes
    chunk_size: int = 10000
    
    def __post_init__(self):
        if self.invalid_phrases_exact is None:
            self.invalid_phrases_exact = ["INVALID ACCESS LEVEL"]
            
        if self.invalid_phrases_contain is None:
            self.invalid_phrases_contain = ["NO ENTRY MADE"]

def get_processing_config() -> ProcessingConfig:
    """Get processing configuration"""
    return ProcessingConfig()