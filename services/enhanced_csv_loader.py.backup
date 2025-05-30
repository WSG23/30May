# data_io/enhanced_csv_loader.py
"""
Enhanced CSV loader with comprehensive error handling and validation
Compatible with existing Yosai codebase
"""

import pandas as pd
import io
import traceback
from typing import Dict, Optional, List, Tuple, Any
import logging
from datetime import datetime, timedelta

from constants.constants import REQUIRED_INTERNAL_COLUMNS

logger = logging.getLogger(__name__)

class CSVProcessingError(Exception):
    """Custom exception for CSV processing errors"""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class EnhancedCSVLoader:
    """Enhanced CSV loader with robust error handling"""
    
    def __init__(self):
        # Set up basic logging if not already configured
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def load_csv_event_log(
        self, 
        csv_file_obj: io.StringIO, 
        column_mapping: Dict[str, str], 
        timestamp_format: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        Load and process CSV event log with enhanced error handling
        
        Args:
            csv_file_obj: CSV file object (StringIO)
            column_mapping: Mapping from CSV columns to standardized names
            timestamp_format: Optional timestamp format string
            
        Returns:
            Processed DataFrame or None if processing failed
        """
        try:
            logger.info("Starting CSV event log processing")
            
            # Step 1: Load and validate CSV structure
            df = self._load_and_validate_csv(csv_file_obj)
            
            # Step 2: Validate column mapping
            self._validate_column_mapping(df, column_mapping)
            
            # Step 3: Apply column mapping
            df_mapped = self._apply_column_mapping(df, column_mapping)
            
            # Step 4: Process timestamp column
            df_processed = self._process_timestamp_column(df_mapped, timestamp_format)
            
            # Step 5: Clean and validate data
            df_final = self._clean_and_validate_data(df_processed)
            
            # Step 6: Final validation
            self._validate_final_data(df_final)
            
            logger.info(f"Successfully processed CSV with {len(df_final)} records")
            return df_final
            
        except (ValidationError, CSVProcessingError) as e:
            logger.error(f"CSV processing failed: {str(e)}")
            print(f"Error: {str(e)}")  # Keep print for compatibility with existing code
            return None
        except Exception as e:
            logger.error(f"Unexpected error in CSV processing: {str(e)}")
            print(f"Unexpected error: {str(e)}")
            traceback.print_exc()
            return None
    
    def _load_and_validate_csv(self, csv_file_obj: io.StringIO) -> pd.DataFrame:
        """Load CSV and perform basic validation"""
        try:
            # Read CSV with error handling for common issues
            df = pd.read_csv(
                csv_file_obj, 
                dtype=str,  # Load all as strings initially
                na_values=['', 'NULL', 'null', 'None', 'N/A', 'n/a'],
                keep_default_na=True
            )
            
            # Basic validation
            if df.empty:
                raise ValidationError("CSV file is empty")
            
            if len(df.columns) == 0:
                raise ValidationError("CSV file has no columns")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Check for minimum viable data
            if len(df) < 2:
                raise ValidationError("CSV file must contain at least 2 rows (header + data)")
            
            logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            return df
            
        except pd.errors.EmptyDataError:
            raise ValidationError("CSV file is empty")
        except pd.errors.ParserError as e:
            raise ValidationError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise CSVProcessingError(f"Failed to read CSV file: {str(e)}")
    
    def _validate_column_mapping(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> None:
        """Validate that column mapping is correct"""
        # Check that all source columns exist in CSV
        missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
        if missing_columns:
            available_cols = ", ".join(df.columns.tolist())
            raise ValidationError(
                f"Source columns not found in CSV: {', '.join(missing_columns)}. "
                f"Available columns: {available_cols}"
            )
        
        # Check that all required internal columns are mapped
        required_internal_keys = set(REQUIRED_INTERNAL_COLUMNS.keys())
        mapped_internal_keys = set(column_mapping.values())
        missing_mappings = required_internal_keys - mapped_internal_keys
        
        if missing_mappings:
            missing_display_names = [REQUIRED_INTERNAL_COLUMNS[key] for key in missing_mappings]
            raise ValidationError(f"Required columns not mapped: {', '.join(missing_display_names)}")
    
    def _apply_column_mapping(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """Apply column mapping to standardize column names"""
        try:
            # Create standardized data with mapped columns
            standardized_data = {}
            for source_col, internal_key in column_mapping.items():
                if source_col in df.columns:
                    # Get the display name for this internal key
                    display_name = REQUIRED_INTERNAL_COLUMNS.get(internal_key, internal_key)
                    # Clean the data - strip whitespace and handle nulls
                    cleaned_data = df[source_col].astype(str).str.strip()
                    # Replace 'nan' strings with actual NaN
                    cleaned_data = cleaned_data.replace(['nan', 'None', 'NULL', ''], pd.NA)
                    standardized_data[display_name] = cleaned_data
            
            df_mapped = pd.DataFrame(standardized_data)
            
            # Validate that all required columns are present
            required_display_names = list(REQUIRED_INTERNAL_COLUMNS.values())
            missing_required = [col for col in required_display_names if col not in df_mapped.columns]
            if missing_required:
                raise ValidationError(f"Required columns missing after mapping: {', '.join(missing_required)}")
            
            logger.info(f"Applied column mapping successfully. Final columns: {list(df_mapped.columns)}")
            return df_mapped
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise CSVProcessingError(f"Failed to apply column mapping: {str(e)}")
    
    def _process_timestamp_column(self, df: pd.DataFrame, timestamp_format: Optional[str] = None) -> pd.DataFrame:
        """Process and validate timestamp column"""
        timestamp_col = REQUIRED_INTERNAL_COLUMNS['Timestamp']
        
        if timestamp_col not in df.columns:
            raise ValidationError(f"Timestamp column '{timestamp_col}' not found")
        
        try:
            original_count = len(df)
            
            # Convert to datetime
            if timestamp_format:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], format=timestamp_format, errors='coerce')
            else:
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
            
            # Check for failed conversions
            invalid_timestamps = df[timestamp_col].isna().sum()
            
            if invalid_timestamps == original_count:
                raise ValidationError("No valid timestamps found in the timestamp column")
            
            # Remove rows with invalid timestamps
            df_clean = df.dropna(subset=[timestamp_col]).copy()
            
            if invalid_timestamps > 0:
                logger.warning(f"Removed {invalid_timestamps} rows with invalid timestamps")
                print(f"Warning: Removed {invalid_timestamps} rows with invalid timestamps")
            
            # Validate timestamp range
            min_date = df_clean[timestamp_col].min()
            max_date = df_clean[timestamp_col].max()
            
            # Check for reasonable date range (not too far in past/future)
            now = datetime.now()
            if min_date < (now - timedelta(days=10*365)):  # 10 years ago
                logger.warning(f"Very old timestamps detected (earliest: {min_date})")
            if max_date > (now + timedelta(days=30)):  # 30 days in future
                logger.warning(f"Future timestamps detected (latest: {max_date})")
            
            logger.info(f"Processed timestamps. Date range: {min_date} to {max_date}")
            return df_clean
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise CSVProcessingError(f"Failed to process timestamp column: {str(e)}")
    
    def _clean_and_validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the processed data"""
        try:
            # Get column display names
            doorid_col = REQUIRED_INTERNAL_COLUMNS['DoorID']
            userid_col = REQUIRED_INTERNAL_COLUMNS['UserID']
            eventtype_col = REQUIRED_INTERNAL_COLUMNS['EventType']
            
            # Clean and validate required columns
            for col_name in [doorid_col, userid_col, eventtype_col]:
                if col_name in df.columns:
                    # Convert to string and clean
                    df[col_name] = df[col_name].astype(str).str.strip()
                    
                    # Remove empty values
                    empty_mask = df[col_name].isin(['', 'nan', 'None', 'NULL', '<NA>'])
                    if empty_mask.any():
                        empty_count = empty_mask.sum()
                        logger.warning(f"Removing {empty_count} rows with empty {col_name} values")
                        print(f"Warning: Removing {empty_count} rows with empty {col_name} values")
                        df = df[~empty_mask].copy()
            
            # Remove duplicate rows
            initial_count = len(df)
            df = df.drop_duplicates().reset_index(drop=True)
            if len(df) < initial_count:
                removed_count = initial_count - len(df)
                logger.info(f"Removed {removed_count} duplicate rows")
                print(f"Info: Removed {removed_count} duplicate rows")
            
            # Final validation
            if len(df) == 0:
                raise ValidationError("No valid data remaining after cleaning")
            
            logger.info(f"Data cleaning completed. Final dataset: {len(df)} rows")
            return df
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise CSVProcessingError(f"Failed to clean and validate data: {str(e)}")
    
    def _validate_final_data(self, df: pd.DataFrame) -> None:
        """Perform final validation on the processed data"""
        try:
            # Check minimum data requirements
            if len(df) < 1:
                raise ValidationError("No data remaining after processing")
            
            # Check that all required columns exist and have data
            required_columns = list(REQUIRED_INTERNAL_COLUMNS.values())
            for col in required_columns:
                if col not in df.columns:
                    raise ValidationError(f"Required column '{col}' missing from final dataset")
                
                # Check for completely empty columns
                non_null_count = df[col].notna().sum()
                if non_null_count == 0:
                    raise ValidationError(f"Column '{col}' has no valid data")
                
                # Warn if column has too few valid values
                valid_percentage = (non_null_count / len(df)) * 100
                if valid_percentage < 50:
                    logger.warning(f"Column '{col}' has only {valid_percentage:.1f}% valid data")
            
            # Check for reasonable data distribution
            doorid_col = REQUIRED_INTERNAL_COLUMNS['DoorID']
            userid_col = REQUIRED_INTERNAL_COLUMNS['UserID']
            
            unique_doors = df[doorid_col].nunique()
            unique_users = df[userid_col].nunique()
            
            if unique_doors < 1:
                raise ValidationError("No unique door IDs found in data")
            if unique_users < 1:
                raise ValidationError("No unique user IDs found in data")
            
            logger.info(f"Final validation passed: {unique_doors} doors, {unique_users} users")
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise CSVProcessingError(f"Final validation failed: {str(e)}")


# Backward compatibility function that mimics the original csv_loader
def load_csv_event_log(csv_file_obj, column_mapping, timestamp_format=None):
    """
    Backward compatible function for the original csv_loader.py interface
    """
    loader = EnhancedCSVLoader()
    return loader.load_csv_event_log(csv_file_obj, column_mapping, timestamp_format)