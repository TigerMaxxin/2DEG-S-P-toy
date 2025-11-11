# Changelog

## Version 2.0 - 2025-11-11

### Major New Features

#### 🔬 Experiment Comparison (High Priority)
- **CSV Data Import**: Support for two formats:
  - Format A: Raw measurements (T_degC, WF_eV, CL_eV)
  - Format B: Processed data (Delta_WF_eV, Delta_CL_eV)
- **Data Validation**: Automatic format detection and data quality checks
- **Sample Data**: Built-in sample In₂O₃ annealing data for testing

#### 🎯 Theory-Experiment Fitting (High Priority)
- **Automatic Parameter Fitting**: Optimize W (depletion width) and η (XPS sampling factor)
- **Scipy-based Optimization**: L-BFGS-B algorithm for robust convergence
- **Goodness-of-Fit Metrics**: R², RMSE, residual analysis
- **Fitting Diagnostics**:
  - Residuals vs ΔWF plot
  - Residuals histogram
  - Predicted vs actual scatter
  - Statistical summary table

#### 📊 New Visualization Plots
- **ΔE_CL vs ΔWF Comparison Plot**: Overlay experimental and fitted data
- **Annealing Trajectory Plot**: Show evolution with temperature (if T data available)
- **Comprehensive Residual Analysis**: 4-panel diagnostic plot

#### 📤 Publication-Quality Export (High Priority)
- **High-Quality Figure Export**:
  - SVG (vector graphics, infinite resolution)
  - PNG (raster, 300/600/1200 DPI)
  - PDF (document format)
- **Journal-Specific Styles**:
  - Nature (warm colors, grid)
  - Science (cool colors, no grid)
  - ACS (standard colors)
  - Grayscale (B&W with different markers)
- **Customizable Settings**:
  - Figure size presets (single/double column, custom)
  - Font size control
  - Line width adjustment
- **Matplotlib Backend**: High-quality rendering for publication

#### 🧪 Beta Features Tab
- Placeholder for upcoming features:
  - Self-consistent S-P diagnostic
  - Experimental guidance mode
  - Uncertainty propagation analysis
  - Material database
  - Annealing trajectory animation

### Technical Improvements

#### New Modules
- `utils/experiment_data.py`: Data import and validation
- `utils/fitting.py`: Parameter optimization and linear regression
- `utils/publication_export.py`: High-quality figure generation with journal styles

#### Enhanced UI
- 6 tabs (was 4): Core Figures, Additional Plots, Experiment Comparison, Publication Export, Beta Features, About
- Better organization and workflow
- Improved user feedback and error messages

#### Dependencies
- Added `matplotlib>=3.7.0` for publication-quality exports
- Existing `scipy>=1.11.0` now used for fitting

### Files Added
- `utils/experiment_data.py`
- `utils/fitting.py`
- `utils/publication_export.py`
- `sample_data_In2O3.csv`
- `CHANGELOG.md`

### Files Modified
- `app.py`: Major refactor with new tabs and features
- `ui/plots.py`: Added new plotting functions
- `requirements.txt`: Added matplotlib dependency

## Version 1.0 - 2025-11-XX

Initial release with:
- Three physical models (M1-Triangular, M2-Fang-Howard, M3-Parabolic)
- Core figures (ns vs Φs, ΔWF vs ns)
- Additional plots (V(z), n(z), w(z))
- Parameter controls
- Model comparison
- Basic data export (CSV, JSON)
