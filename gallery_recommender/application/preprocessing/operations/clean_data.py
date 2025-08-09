import datetime
import pandas as pd
from loguru import logger
import re

# Default date if needed (adjust as necessary)
DEFAULT_DATE = datetime.datetime(2000, 1, 1)

def ensure_datetime(x, default_date=DEFAULT_DATE):
    """
    Converts a value to a datetime.datetime object.
    If x is missing, or cannot be parsed, returns default_date.
    """
    if pd.isnull(x) or x == "":
        return default_date

    if isinstance(x, datetime.datetime):
        return x

    if isinstance(x, datetime.date) and not isinstance(x, datetime.datetime):
        # Convert date to datetime by adding time as midnight.
        return datetime.datetime.combine(x, datetime.time.min)

    if isinstance(x, str):
        try:
            # Assumes format 'YYYY-MM-DD'
            return datetime.datetime.strptime(x, "%Y-%m-%d")
        except Exception as e:
            logger.error(f"Failed to parse date string '{x}': {e}")
            return default_date

    # Fallback
    return default_date

def clean_sheets_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame extracted from Google Sheets:
      - Fills missing values with empty strings.
      - Converts specified date columns to datetime.datetime.
    
    Args:
        df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    logger.info(f"Cleaning all fields in the DataFrame from any leading and trailing spaces")
    # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    logger.info(f"Cleaning DataFrame: {df.head()}")
    # Fill missing values for the entire DataFrame.
    df = df.fillna("")

    # Determine the exact column names to process.
    # Check the actual column names in your DataFrame.
    logger.info(f"Columns in DataFrame: {df.columns.tolist()}")
    
    # Use the names as they appear in your final document.
    date_columns = ['Exhibition Start Date', 'Exhibition End Date']
    
    for col in date_columns:
        if col in df.columns:
            # Convert each cell in the column.
            df[col] = df[col].apply(ensure_datetime)
            logger.info(f"Converted column '{col}' to datetime.datetime")
        else:
            logger.warning(f"Date column '{col}' not found in DataFrame.")
    
    return df

# Clean text data, get rid of special characters and extra spaces
def clean_text(text: str) -> str:
    text = re.sub(r"[^\w\s.,!?]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()