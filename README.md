# 2DEG Surface Electron Gas Visualization Tool

Interactive tool for exploring two-dimensional electron gas (2DEG) physics at oxide surfaces, connecting surface band bending to observable quantities in X-ray photoelectron spectroscopy (XPS/UPS).

![2DEG Visualization](https://img.shields.io/badge/physics-2DEG-blue) ![Python](https://img.shields.io/badge/python-3.8+-green) ![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## Features

### 🎯 Core Functionality
- **Two Essential Figures**:
  - **Figure 1**: Sheet Density (nₛ) vs Surface Potential (Φₛ)
  - **Figure 2**: Work Function Change (ΔWF) vs Sheet Density (nₛ)

- **Three Physical Models**:
  - **M1 (Triangular)**: Constant electric field approximation
  - **M2 (Fang-Howard)**: Self-consistent variational approach
  - **M3 (Parabolic)**: Linearly decaying field (harmonic potential)

- **XPS Modeling**:
  - Core level shift calculations
  - Escape depth effects (λ, θ dependence)
  - Adsorbate dipole layer effects

### 🔧 Interactive Controls
- Real-time parameter adjustment with sliders
- Model comparison (overlay up to 4 curves)
- Adsorbate effects (coverage, dipole moment)
- Additional visualizations: V(z), n(z), w(z) profiles

### 💾 Export Options
- **Figures**: PNG (300 dpi), SVG (vector)
- **Data**: CSV with all parameters
- **Configuration**: JSON for reproducibility

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/2DEG-S-P-toy.git
cd 2DEG-S-P-toy
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Required Packages
```
streamlit>=1.28.0
plotly>=5.17.0
numpy>=1.24.0
scipy>=1.11.0
pandas>=2.0.0
kaleido>=0.2.1  # For static image export
```

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Basic Workflow

1. **Select Model**: Choose M1, M2, or M3 from the sidebar
2. **Adjust Parameters**:
   - Material: m*/m₀, εᵣ, T
   - Surface: Φₛ, W
   - XPS: λ, θ
3. **View Results**: Observe real-time updates in both figures
4. **Compare Models**: Click "Add to Compare" to overlay multiple curves
5. **Export Data**: Use the Export tab to save figures and data

### Example Use Cases

#### 1. Compare Models for Different Depletion Widths
```
1. Set W = 2 nm, select M1, click "Add to Compare"
2. Set W = 3 nm, select M1, click "Add to Compare"
3. Set W = 5 nm, select M1, click "Add to Compare"
4. Observe linear scaling of nₛ with 1/W
```

#### 2. Explore Adsorbate Effects
```
1. Set Φₛ = 0.4 eV
2. Check "Show with adsorbates"
3. Adjust coverage θ and dipole μ⊥
4. Observe vertical shift in Figure 2 (slope unchanged)
```

#### 3. Validate XPS Depth Sensitivity
```
1. Enable "Show XPS weight w(z)"
2. Vary λ from 0.5 to 3.0 nm
3. Vary θ from 0° to 60°
4. Observe η factor changes
```

## Project Structure

```
2DEG-S-P-toy/
├── app.py                  # Main Streamlit application
├── models/
│   ├── __init__.py
│   ├── triangular.py      # M1: Triangular model
│   ├── fang_howard.py     # M2: Fang-Howard model
│   └── parabolic.py       # M3: Parabolic model
├── physics/
│   ├── __init__.py
│   ├── constants.py       # Physical constants
│   ├── units.py           # Unit conversions
│   └── xps.py             # XPS modeling
├── ui/
│   ├── __init__.py
│   └── plots.py           # Plotly plotting functions
├── utils/
│   ├── __init__.py
│   └── export.py          # Export utilities
├── tests/
│   └── test_models.py     # Unit tests
├── README.md
└── requirements.txt
```

## Physics Background

### Key Relationships

1. **Gauss's Law** (universal):
   ```
   nₛ = (ε·Eₛ) / q
   ```

2. **Model-Specific**:
   - **M1**: Φₛ = Eₛ·W  →  nₛ = (ε/q)·(Φₛ/W)
   - **M2**: Self-consistent iteration with b = (12m*qEₛ/ℏ²)^(1/3)
   - **M3**: Eₛ = 2Φₛ/W  →  nₛ = (2ε/q)·(Φₛ/W)

3. **Work Function**:
   ```
   ΔWF = -Φₛ + ΔΦ_dip
   ```

4. **XPS Core Level Shift**:
   ```
   ΔE_CL = -∫ w(z)·V(z) dz
   w(z) = exp(-z/(λ·cosθ)) / (λ·cosθ)
   ```

### Model Comparison

| Property | M1 | M2 | M3 |
|----------|----|----|----|
| Field profile | Constant | Exponential decay | Linear decay |
| nₛ at Φₛ=0.3eV, W=3nm | 5.3×10¹³ cm⁻² | ~7×10¹³ cm⁻² | 10.6×10¹³ cm⁻² |
| ΔWF slope | -q·W/ε | Intermediate | -q·W/(2ε) |
| Physical regime | Low accumulation | General | High accumulation |

**Key Insight**: M3 gives exactly **2× the nₛ** and **½ the slope** compared to M1!

## Testing

Run validation tests:
```bash
python tests/test_models.py
```

### Test Cases

The test suite validates:
1. ✅ M1 model numerical accuracy
2. ✅ M3 model numerical accuracy
3. ✅ M3/M1 ratio exactly equals 2.0
4. ✅ Adsorbate shift (constant offset)
5. ✅ M2 self-consistent convergence
6. ✅ Zero potential boundary condition

Expected output:
```
=== Test 1: M1 Model Basic ===
Result: ns = 5.285 × 10¹³ cm⁻²
Expected: ns ≈ 5.3 × 10¹³ cm⁻²
✓ Test 1 passed!
...
Results: 6 passed, 0 failed
```

## Default Parameters

```python
m*/m₀ = 0.32          # Effective mass (typical for SrTiO₃)
εᵣ = 9                # Relative permittivity
T = 300 K             # Temperature
W = 3.0 nm            # Depletion width
Φₛ = 0.4 eV           # Surface potential
λ = 1.8 nm            # XPS mean free path
θ = 0°                # XPS detection angle (normal emission)
```

## Scientific References

1. **Fang-Howard Model**:
   - Fang & Howard, *Phys. Rev. B* **13**, 1546 (1966)

2. **2DEG at Oxide Surfaces**:
   - Ohtomo & Hwang, *Nature* **427**, 423 (2004)
   - Copie et al., *Adv. Mater.* **29**, 1604112 (2017)

3. **XPS and Work Function**:
   - Salvinelli et al., *ACS Appl. Mater. Interfaces* **10**, 25941 (2018)
   - Dudy et al., *Adv. Mater.* **28**, 7443 (2016)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Figures not exporting to PNG
- **Solution**: Install kaleido: `pip install kaleido`

**Issue**: M2 model not converging
- **Solution**: Try reducing Φₛ or increasing W (avoid extreme field strengths)

**Issue**: Slow performance
- **Solution**: Reduce number of comparison curves (max 4 recommended)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Authors

- **Aaron** - Initial development
- **Claude (Anthropic)** - Code generation assistance

## Acknowledgments

- Physics models based on established semiconductor theory
- UI framework powered by Streamlit
- Visualizations created with Plotly

## Version History

- **v1.0.0** (2025-11-11): Initial release
  - Three physical models (M1, M2, M3)
  - Interactive Streamlit interface
  - XPS modeling and adsorbate effects
  - Export functionality
  - Comprehensive test suite

---

**Contact**: For questions or feedback, please open an issue on GitHub.

**Citation**: If you use this tool in your research, please cite:
```bibtex
@software{2deg_visualization_2025,
  title = {2DEG Surface Electron Gas Visualization Tool},
  author = {Aaron},
  year = {2025},
  url = {https://github.com/yourusername/2DEG-S-P-toy}
}
```
