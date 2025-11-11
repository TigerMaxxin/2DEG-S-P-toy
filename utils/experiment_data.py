"""
Experimental data import and validation utilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
import io


def validate_csv_data(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate imported CSV data.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to validate

    Returns
    -------
    is_valid : bool
        True if data is valid
    message : str
        Validation message or error description
    """
    # Check if dataframe is empty
    if df.empty:
        return False, "CSV file is empty"

    # Check for NaN values
    if df.isnull().values.any():
        return False, "Data contains NaN values. Please clean your data."

    # Check data ranges
    if 'Delta_WF_eV' in df.columns:
        if np.any(np.abs(df['Delta_WF_eV']) > 3.0):
            return False, "ΔWF values exceed ±3 eV. Please check your data."

    if 'Delta_CL_eV' in df.columns:
        if np.any(np.abs(df['Delta_CL_eV']) > 2.0):
            return False, "ΔE_CL values exceed ±2 eV. Please check your data."

    return True, "Data validated successfully"


def detect_format(df: pd.DataFrame) -> str:
    """
    Detect the format of the CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe

    Returns
    -------
    format_type : str
        'processed' or 'raw' or 'unknown'
    """
    # Check for processed format (Delta values already calculated)
    if 'Delta_WF_eV' in df.columns and 'Delta_CL_eV' in df.columns:
        return 'processed'

    # Check for raw format (absolute values)
    if 'WF_eV' in df.columns and ('CL_eV' in df.columns or 'In3d_eV' in df.columns):
        return 'raw'

    return 'unknown'


def process_raw_data(df: pd.DataFrame) -> Dict[str, np.ndarray]:
    """
    Process raw measurement data.

    Calculates Delta values relative to first measurement point.

    Parameters
    ----------
    df : pd.DataFrame
        Raw data with 'T_degC', 'WF_eV', and core level columns

    Returns
    -------
    data : dict
        Processed data dictionary
    """
    # Get temperature
    T = df['T_degC'].values if 'T_degC' in df.columns else np.arange(len(df))

    # Calculate Delta WF
    WF = df['WF_eV'].values
    Delta_WF = WF - WF[0]

    # Calculate Delta CL (check for different column names)
    if 'CL_eV' in df.columns:
        CL = df['CL_eV'].values
    elif 'In3d_eV' in df.columns:
        CL = df['In3d_eV'].values
    elif 'O1s_eV' in df.columns:
        CL = df['O1s_eV'].values
    else:
        raise ValueError("No core level column found (expected 'CL_eV', 'In3d_eV', or 'O1s_eV')")

    Delta_CL = CL - CL[0]

    return {
        'T_degC': T,
        'Delta_WF': Delta_WF,
        'Delta_CL': Delta_CL,
        'WF_abs': WF,
        'CL_abs': CL
    }


def process_processed_data(df: pd.DataFrame) -> Dict[str, np.ndarray]:
    """
    Process already-processed data.

    Parameters
    ----------
    df : pd.DataFrame
        Processed data with Delta values

    Returns
    -------
    data : dict
        Data dictionary
    """
    data = {
        'Delta_WF': df['Delta_WF_eV'].values,
        'Delta_CL': df['Delta_CL_eV'].values,
    }

    # Optional columns
    if 'T_degC' in df.columns:
        data['T_degC'] = df['T_degC'].values

    if 'ns_cm2' in df.columns:
        data['ns'] = df['ns_cm2'].values * 1e17  # Convert to m^-2

    return data


def import_experimental_data(file_content: bytes) -> Dict[str, Any]:
    """
    Import and process experimental data from CSV.

    Parameters
    ----------
    file_content : bytes
        Content of uploaded CSV file

    Returns
    -------
    result : dict
        Dictionary containing:
        - 'success': bool
        - 'data': dict or None
        - 'message': str
        - 'format': str
    """
    try:
        # Read CSV
        df = pd.read_csv(io.BytesIO(file_content))

        # Detect format
        format_type = detect_format(df)

        if format_type == 'unknown':
            return {
                'success': False,
                'data': None,
                'message': "Unrecognized CSV format. Expected columns: 'T_degC, WF_eV, CL_eV' or 'Delta_WF_eV, Delta_CL_eV'",
                'format': 'unknown'
            }

        # Validate
        is_valid, msg = validate_csv_data(df)
        if not is_valid:
            return {
                'success': False,
                'data': None,
                'message': msg,
                'format': format_type
            }

        # Process data
        if format_type == 'raw':
            data = process_raw_data(df)
        else:
            data = process_processed_data(df)

        return {
            'success': True,
            'data': data,
            'message': f"Successfully imported {len(df)} data points ({format_type} format)",
            'format': format_type
        }

    except Exception as e:
        return {
            'success': False,
            'data': None,
            'message': f"Error reading CSV: {str(e)}",
            'format': 'error'
        }


def get_format_example_text() -> str:
    """
    Get example CSV format text for user guidance.

    Returns
    -------
    example_text : str
        Formatted example text
    """
    example = """
**Format A: Raw Measurements**
```
T_degC,WF_eV,In3d_eV
25,4.20,444.50
100,4.28,444.42
150,4.35,444.35
200,4.42,444.27
```

**Format B: Processed Data**
```
Delta_WF_eV,Delta_CL_eV,T_degC
0.000,0.000,25
0.080,-0.080,100
0.150,-0.150,150
0.220,-0.220,200
```

**Notes:**
- First row must contain column headers
- Decimal separator: period (.)
- Temperature column optional for Format B
- Core level can be named: CL_eV, In3d_eV, O1s_eV, etc.
"""
    return example


def create_sample_data() -> pd.DataFrame:
    """
    Create sample experimental data for testing.

    Returns
    -------
    df : pd.DataFrame
        Sample data
    """
    # Simulate In2O3 annealing experiment
    T = np.array([25, 100, 150, 200, 250, 300, 350, 400])

    # Work function increases with temperature (water desorption + oxygen vacancy formation)
    WF_base = 4.20
    Delta_WF = np.array([0.00, 0.08, 0.15, 0.22, 0.28, 0.32, 0.36, 0.38])
    WF = WF_base + Delta_WF

    # Core level shifts with factor ~0.85
    In3d_base = 444.50
    Delta_CL = Delta_WF * 0.85
    In3d = In3d_base - Delta_CL  # Core level moves opposite to WF

    df = pd.DataFrame({
        'T_degC': T,
        'WF_eV': WF,
        'In3d_eV': In3d
    })

    return df
