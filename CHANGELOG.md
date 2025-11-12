# Changelog

## Version 2.1 - 2025-11-12

### Critical Bug Fixes 🐛

#### Unit Conversion Bug Fixed
- **Issue**: `ns_to_display()` function in `physics/units.py` had incorrect density conversion
- **Root Cause**: Used `CM2_TO_M2` (area conversion) instead of inverse for density conversion
- **Impact**: Sheet density displayed values were off by factor of 10⁸
- **Fix**: Corrected to use proper density conversion (1 m⁻² = 10⁻⁴ cm⁻², inverse of area)
- **Files Modified**: `physics/units.py`

#### ns Range Correction in Figure 2
- **Issue**: Figure 2 (ΔWF vs nₛ) used incorrect range `np.linspace(1e12, 2e13, 100)` m⁻²
- **Problem**: This corresponds to 0.00001-0.0002 × 10¹³ cm⁻² (far too small!)
- **Expected**: Typical 2DEG density range should be 0.2-2.0 × 10¹³ cm⁻²
- **Fix**: Updated to `np.linspace(2e16, 2e17, 100)` m⁻² (= 0.2-2.0 × 10¹³ cm⁻²)
- **Impact**: Curves now display proper slopes instead of appearing nearly horizontal
- **Files Modified**: `app.py` line 267-269

#### Adsorbate Input Validation
- **Added**: Input validation in `calculate_dipole_from_coverage()`
  - Clamps coverage θ to [0, 1] range
  - Warns if N_site outside typical range (10¹³-10¹⁶ cm⁻²)
  - Warns if μ⊥ outside typical range (0-10 Debye)
  - Warns if |ΔΦ_dip| > 2 eV (unusually large)
- **Purpose**: Catch unit conversion errors before they corrupt plots
- **Files Modified**: `physics/xps.py`

#### Plot Sanity Checks
- **Added**: Guardrail checks in `create_Delta_WF_vs_ns_plot()`
  - Warns if |ΔWF| > 5 eV (likely unit error)
  - Warns if nₛ display values outside 0.001-1000 × 10¹³ cm⁻² range
- **Purpose**: Prevent nonsensical plots from reaching user
- **Files Modified**: `ui/plots.py`

### Verification
- **Test Suite**: `test_adsorbate_bug.py` now passes all checks
  - ✅ nₛ range: 0.2 to 2.0 × 10¹³ cm⁻²
  - ✅ ΔΦ_dip: -0.283 eV (expected value)
  - ✅ Slope: -0.603 eV/(10¹³ cm⁻²) for M1 with εᵣ=9, W=3nm
  - ✅ Parallel curves: "with ads" and "no ads" have identical slopes
  - ✅ Vertical shift: Exactly equals ΔΦ_dip

### Files Modified
- `physics/units.py`: Fixed density conversion logic
- `physics/xps.py`: Added input validation and warnings
- `ui/plots.py`: Added sanity checks for plot data
- `app.py`: Updated ns_range and version to 2.1

### Documentation Updates
- Updated in-app "About" section with v2.1 bug fix summary
- Updated `CHANGELOG.md` (this file)
- Updated `README.md` with v2.1 information

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
