# Grid Analysis Tool

A Python script for analyzing PowerWorld CSV data with support for bus, branch, and generator analysis. Features include load tracking, generation analysis, and MVA calculations with formatted visual output.

## Features

### Data Analysis
- Bus load and generation analysis
- Substation load tracking
- Branch power analysis
- Generator type ranking by MVA
- Automatic file type detection

### Visualization
- Generation heat maps
- Load distribution heat maps
- Color-coded console output
- Formatted data tables

## How to Use

1. Make sure you have Python installed with the required packages:
   ```bash
   pip install matplotlib seaborn numpy scipy
   ```

2. Run the script:
   ```bash
   python gridAnalysis.py
   ```

3. When prompted, enter the path to your CSV file
   - Supports Bus, Branch, and Generator data files
   - Files must be properly formatted CSVs

4. Choose from the available options:
   ```
   BUS OPERATIONS:
   1. Find Max Active Bus Load
   2. Find Max Active Bus Generation

   SUBSTATION OPERATIONS:
   3. Find Max Active Substation Load
   4. Find Max Active Substation Generation

   BRANCH OPERATIONS:
   5. Find Largest Line Apparent Power

   GENERATOR OPERATIONS:
   6. Rank Generation Types by MVA

   VISUALIZATION:
   7. Generate Generation Heat Map
   8. Generate Load Heat Map

   OTHER:
   9. Select another file
   10. Display loaded files
   11. Exit
   ```

## Input File Requirements

### Bus Data Files
- 20 columns
- First line must contain "Bus"
- Second line contains headers

### Branch Data Files
- 15 columns
- First line must contain "Branch"
- Second line contains headers

### Generator Data Files
- 25 columns
- First line must contain "Gen"
- Second line contains headers
- Generation type in column 18
- MW in column 5
- Mvar in column 6

## Example Output

```
Generation Type Rankings by MVA:
Type                              MVA          MW        Mvar    Count
---------------------------------------------------------------------
Nuclear                       1234.56     1000.00     750.00       5
Solar                         987.65      800.00     600.00       3
Wind                          456.78      400.00     300.00       2
---------------------------------------------------------------------
TOTAL                        2678.99     2200.00    1650.00      10
```

## Requirements
- Python 3.x
- matplotlib
- seaborn
- numpy
- scipy

## Error Handling
- Validates file formats before processing
- Checks for correct number of columns
- Handles missing or invalid data gracefully
- Provides clear error messages for troubleshooting
