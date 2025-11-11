"""
2DEG Surface Electron Gas Visualization Tool

Interactive tool connecting surface band bending (Φs) → 2DEG sheet density (ns)
→ XPS/UPS observables (ΔWF, ΔE_CL)
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import io

# Import models
from models import TriangularModel, FangHowardModel, ParabolicModel
from physics.constants import (
    M0, DEFAULT_M_STAR, DEFAULT_EPSILON_R, DEFAULT_TEMPERATURE,
    DEFAULT_W, DEFAULT_LAMBDA_XPS, M_STAR_RANGE, EPSILON_R_RANGE,
    TEMPERATURE_RANGE, W_RANGE, PHI_S_RANGE, LAMBDA_XPS_RANGE,
    THETA_XPS_RANGE, DELTA_PHI_DIP_RANGE
)
from physics.xps import XPSModel, calculate_xps_weight
from physics.units import ns_to_display, ns_from_display, m_to_nm, nm_to_m, J_to_eV
from ui.plots import (
    create_ns_vs_Phi_s_plot, create_Delta_WF_vs_ns_plot,
    create_potential_profile_plot, create_electron_density_plot,
    create_xps_weight_plot, create_combined_profile_plot
)

# Page configuration
st.set_page_config(
    page_title="2DEG Visualization Tool",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("2DEG Surface Electron Gas Visualization Tool")
st.markdown("**Interactive tool for exploring 2DEG physics and XPS measurements**")

# Initialize session state for comparison curves
if 'comparison_curves' not in st.session_state:
    st.session_state.comparison_curves = []

# Sidebar - Parameter Controls
st.sidebar.header("Parameters")

# Model selection
model_type = st.sidebar.selectbox(
    "Model Selection",
    options=["M1-Triangular", "M2-Fang-Howard", "M3-Parabolic"],
    index=0,
    help="Select the potential well model"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Material Parameters")

# Effective mass
m_star_ratio = st.sidebar.slider(
    "m*/m₀",
    min_value=M_STAR_RANGE[0],
    max_value=M_STAR_RANGE[1],
    value=DEFAULT_M_STAR / M0,
    step=0.01,
    help="Effective mass ratio"
)
m_star = m_star_ratio * M0

# Relative permittivity
epsilon_r = st.sidebar.slider(
    "εᵣ (Relative Permittivity)",
    min_value=EPSILON_R_RANGE[0],
    max_value=EPSILON_R_RANGE[1],
    value=DEFAULT_EPSILON_R,
    step=1,
    help="Relative dielectric constant"
)

# Temperature
temperature = st.sidebar.slider(
    "T (K)",
    min_value=TEMPERATURE_RANGE[0],
    max_value=TEMPERATURE_RANGE[1],
    value=DEFAULT_TEMPERATURE,
    step=10,
    help="Temperature in Kelvin"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Surface Electrostatics")

# Surface potential
Phi_s = st.sidebar.slider(
    "Φₛ (eV)",
    min_value=PHI_S_RANGE[0],
    max_value=PHI_S_RANGE[1],
    value=0.4,
    step=0.01,
    help="Surface potential (band bending)"
)

# Depletion width
W_nm = st.sidebar.slider(
    "W (nm)",
    min_value=W_RANGE[0],
    max_value=W_RANGE[1],
    value=DEFAULT_W,
    step=0.1,
    help="Depletion layer width"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Surface Adsorbates")

# Adsorbate checkbox
show_adsorbates = st.sidebar.checkbox(
    "Show with adsorbates",
    value=False,
    help="Include adsorbate dipole layer effects"
)

if show_adsorbates:
    # Coverage
    coverage = st.sidebar.slider(
        "θ (Coverage)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Adsorbate coverage fraction"
    )

    # Dipole moment
    mu_debye = st.sidebar.slider(
        "μ⊥ (Debye)",
        min_value=0.0,
        max_value=3.0,
        value=1.5,
        step=0.1,
        help="Perpendicular dipole moment"
    )

    # Calculate dipole shift
    N_site = 1e15  # Surface site density in cm⁻²
    from physics.xps import calculate_dipole_from_coverage
    Delta_Phi_dip = calculate_dipole_from_coverage(coverage, N_site, mu_debye)

    st.sidebar.info(f"ΔΦ_dip = {Delta_Phi_dip:+.3f} eV")
else:
    Delta_Phi_dip = 0.0
    coverage = 0.0
    mu_debye = 0.0

st.sidebar.markdown("---")
st.sidebar.subheader("XPS Parameters")

# XPS mean free path
lambda_xps = st.sidebar.slider(
    "λ (nm)",
    min_value=LAMBDA_XPS_RANGE[0],
    max_value=LAMBDA_XPS_RANGE[1],
    value=DEFAULT_LAMBDA_XPS,
    step=0.1,
    help="Inelastic mean free path"
)

# XPS detection angle
theta_xps = st.sidebar.slider(
    "θ (degrees)",
    min_value=THETA_XPS_RANGE[0],
    max_value=THETA_XPS_RANGE[1],
    value=0,
    step=5,
    help="Detection angle (0° = normal emission)"
)

st.sidebar.markdown("---")
st.sidebar.subheader("Visualization Options")

# Visualization checkboxes
show_subbands = st.sidebar.checkbox("Show subband levels (Eₙ)", value=False)
show_n_z = st.sidebar.checkbox("Show n(z) distribution", value=False)
show_w_z = st.sidebar.checkbox("Show XPS weight w(z)", value=False)
show_uncertainty = st.sidebar.checkbox("Show m* uncertainty band", value=False)

# Buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    add_comparison = st.button("Add to Compare", use_container_width=True)
with col2:
    clear_comparison = st.button("Clear Compare", use_container_width=True)

# Main area - Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Core Figures",
    "📈 Additional Plots",
    "💾 Export Data",
    "ℹ️ About"
])

# ============================================================================
# TAB 1: CORE FIGURES
# ============================================================================

with tab1:
    # Initialize the selected model
    if model_type == "M1-Triangular":
        model = TriangularModel(m_star, epsilon_r, W_nm)
    elif model_type == "M2-Fang-Howard":
        model = FangHowardModel(m_star, epsilon_r, W_nm)
    else:  # M3-Parabolic
        model = ParabolicModel(m_star, epsilon_r, W_nm)

    # Initialize XPS model
    xps_model = XPSModel(lambda_xps, theta_xps)

    # Generate curve data for Figure 1: ns vs Phi_s
    Phi_s_range = np.linspace(0.1, 0.6, 100)
    ns_array = model.calculate_ns(Phi_s_range)

    curves_fig1 = [{
        'name': f"{model_type}, W={W_nm:.1f}nm",
        'Phi_s': Phi_s_range,
        'ns': ns_array,
        'color': 'blue'
    }]

    # Generate curve data for Figure 2: Delta_WF vs ns
    ns_range = np.linspace(1e12, 2e13, 100)  # m⁻²

    # Calculate Delta_WF for each ns
    Delta_WF_array = model.calculate_Delta_WF(ns_range)

    # Without adsorbates
    curves_fig2 = [{
        'name': f"{model_type}, W={W_nm:.1f}nm (no ads)",
        'ns': ns_range,
        'Delta_WF': Delta_WF_array,
        'with_adsorbate': False,
        'color': 'blue'
    }]

    # With adsorbates
    if show_adsorbates:
        Delta_WF_with_ads = Delta_WF_array + Delta_Phi_dip
        curves_fig2.append({
            'name': f"{model_type}, W={W_nm:.1f}nm (with ads)",
            'ns': ns_range,
            'Delta_WF': Delta_WF_with_ads,
            'with_adsorbate': True,
            'color': 'blue'
        })

    # Add comparison curves if any
    for comp_curve in st.session_state.comparison_curves:
        # For Figure 1
        curves_fig1.append({
            'name': comp_curve['name'],
            'Phi_s': comp_curve['Phi_s_range'],
            'ns': comp_curve['ns_array'],
            'color': comp_curve.get('color', 'gray')
        })

        # For Figure 2
        curves_fig2.append({
            'name': comp_curve['name'] + " (no ads)",
            'ns': comp_curve['ns_range'],
            'Delta_WF': comp_curve['Delta_WF_array'],
            'with_adsorbate': False,
            'color': comp_curve.get('color', 'gray')
        })

        if comp_curve.get('with_adsorbates', False):
            curves_fig2.append({
                'name': comp_curve['name'] + " (with ads)",
                'ns': comp_curve['ns_range'],
                'Delta_WF': comp_curve['Delta_WF_with_ads'],
                'with_adsorbate': True,
                'color': comp_curve.get('color', 'gray')
            })

    # Create and display plots
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Figure 1: Sheet Density vs Surface Potential")
        fig1 = create_ns_vs_Phi_s_plot(curves_fig1)
        st.plotly_chart(fig1, use_container_width=True)

        # Display current value
        current_ns = model.calculate_ns(Phi_s)
        st.info(f"**Current:** Φₛ = {Phi_s:.3f} eV → nₛ = {ns_to_display(current_ns):.3f} × 10¹³ cm⁻²")

    with col2:
        st.subheader("Figure 2: Work Function Change vs Sheet Density")
        fig2 = create_Delta_WF_vs_ns_plot(curves_fig2)
        st.plotly_chart(fig2, use_container_width=True)

        # Display current value
        current_ns = model.calculate_ns(Phi_s)
        current_Delta_WF = model.calculate_Delta_WF(current_ns)
        if show_adsorbates:
            current_Delta_WF_total = current_Delta_WF + Delta_Phi_dip
            st.info(f"**Current:** nₛ = {ns_to_display(current_ns):.3f} × 10¹³ cm⁻² → ΔWF = {current_Delta_WF:.3f} eV (no ads) / {current_Delta_WF_total:.3f} eV (with ads)")
        else:
            st.info(f"**Current:** nₛ = {ns_to_display(current_ns):.3f} × 10¹³ cm⁻² → ΔWF = {current_Delta_WF:.3f} eV")

    # Calculate and display slope
    if hasattr(model, 'get_slope'):
        slope = model.get_slope()
        st.success(f"**Slope of ΔWF vs nₛ:** {slope:.3f} eV/(10¹³ cm⁻²)")

    # XPS core level shift
    if model_type != "M2-Fang-Howard":  # Simpler calculation for M1 and M3
        Delta_E_CL, eta = xps_model.calculate_shift(model, Phi_s)
        st.success(f"**XPS Core Level Shift:** ΔE_CL = {Delta_E_CL:.3f} eV (η = {eta:.2f})")

# ============================================================================
# TAB 2: ADDITIONAL PLOTS
# ============================================================================

with tab2:
    st.subheader("Depth Profiles and Distributions")

    # Create z array for profiles
    z_max = 3 * W_nm
    z_nm_array = np.linspace(0, z_max, 500)
    z_m_array = nm_to_m(z_nm_array)

    # Get potential profile
    V_z_J = model.get_potential(Phi_s, z_m_array)
    V_z_eV = J_to_eV(V_z_J)

    # Potential profile
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Potential Profile V(z)")
        fig_V = create_potential_profile_plot(z_nm_array, V_z_eV)
        st.plotly_chart(fig_V, use_container_width=True)

    with col2:
        if show_w_z:
            st.markdown("### XPS Sampling Weight w(z)")
            w_z = calculate_xps_weight(z_m_array, lambda_xps, theta_xps)
            fig_w = create_xps_weight_plot(z_nm_array, w_z)
            st.plotly_chart(fig_w, use_container_width=True)

    # Electron density for M2
    if show_n_z and model_type == "M2-Fang-Howard":
        st.markdown("### Electron Density Distribution n(z)")
        n_z = model.get_electron_density(Phi_s, z_m_array)
        fig_n = create_electron_density_plot(z_nm_array, n_z)
        st.plotly_chart(fig_n, use_container_width=True)

    # Subband energies
    if show_subbands:
        st.markdown("### Quantum Subband Energy Levels")
        if hasattr(model, 'get_subband_energies'):
            energies = model.get_subband_energies(Phi_s, n_levels=3)
            df_energies = pd.DataFrame({
                'Level': ['E₁', 'E₂', 'E₃'],
                'Energy (eV)': energies
            })
            st.table(df_energies)
        elif hasattr(model, 'get_harmonic_levels'):
            energies = model.get_harmonic_levels(Phi_s, n_levels=3)
            df_energies = pd.DataFrame({
                'Level': ['E₀', 'E₁', 'E₂'],
                'Energy (eV)': energies
            })
            st.table(df_energies)

# ============================================================================
# TAB 3: EXPORT DATA
# ============================================================================

with tab3:
    st.subheader("Export Data and Figures")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Export Figures")

        # Export Figure 1 as PNG
        if st.button("Download Figure 1 (PNG)", use_container_width=True):
            fig1.write_image("figure1_ns_vs_Phi_s.png", width=800, height=500, scale=2)
            st.success("Figure 1 saved as figure1_ns_vs_Phi_s.png")

        # Export Figure 2 as PNG
        if st.button("Download Figure 2 (PNG)", use_container_width=True):
            fig2.write_image("figure2_Delta_WF_vs_ns.png", width=800, height=500, scale=2)
            st.success("Figure 2 saved as figure2_Delta_WF_vs_ns.png")

    with col2:
        st.markdown("### Export Data")

        # Prepare CSV data
        csv_data = []
        for i, (phi, ns_val) in enumerate(zip(Phi_s_range, ns_array)):
            csv_data.append({
                'model': model_type,
                'W_nm': W_nm,
                'Phi_s_eV': phi,
                'm_star_m0': m_star_ratio,
                'epsilon_r': epsilon_r,
                'T_K': temperature,
                'ns_cm2': ns_to_display(ns_val) * 1e13,
                'Delta_WF_eV': model.calculate_Delta_WF(ns_val),
            })

        df_export = pd.DataFrame(csv_data)

        # CSV download
        csv = df_export.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"2deg_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

        # JSON export with parameters
        json_data = {
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'model': model_type,
                'm_star': m_star_ratio,
                'epsilon_r': epsilon_r,
                'T_K': temperature,
                'W_nm': W_nm,
                'Phi_s': Phi_s,
                'lambda_xps_nm': lambda_xps,
                'theta_xps_deg': theta_xps,
                'Delta_Phi_dip_eV': Delta_Phi_dip
            }
        }

        import json
        json_str = json.dumps(json_data, indent=2)
        st.download_button(
            label="Download JSON Config",
            data=json_str,
            file_name=f"2deg_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

# ============================================================================
# TAB 4: ABOUT
# ============================================================================

with tab4:
    st.markdown("""
    ## About This Tool

    This interactive visualization tool explores the physics of two-dimensional electron gases (2DEG)
    at oxide surfaces, connecting surface band bending to observable quantities in photoemission
    spectroscopy (XPS/UPS).

    ### Three Physical Models

    - **M1 (Triangular)**: Constant electric field approximation
    - **M2 (Fang-Howard)**: Self-consistent variational approach with adaptive width
    - **M3 (Parabolic)**: Linearly decaying field (harmonic potential)

    ### Key Relationships

    1. **Gauss's Law**: nₛ = (ε·Eₛ)/q
    2. **Band Bending**: Φₛ relates to surface field Eₛ
    3. **Work Function**: ΔWF = -Φₛ + ΔΦ_dip
    4. **XPS Shift**: ΔE_CL = weighted average of band bending potential

    ### Model Comparison

    The slope of ΔWF vs nₛ differs between models:
    - **M1**: slope = -q·W/ε
    - **M3**: slope = -q·W/(2ε) (exactly half of M1)
    - **M2**: intermediate, field-dependent

    ### Usage Tips

    1. Use the sidebar to adjust parameters
    2. Compare different models using "Add to Compare"
    3. Export data and figures for publications
    4. Adsorbates shift ΔWF without changing slope

    ### References

    - Fang & Howard, Phys. Rev. B **13**, 1546 (1966)
    - Copie et al., Adv. Mater. **29**, 1604112 (2017)
    - Salvinelli et al., ACS Appl. Mater. Interfaces **10**, 25941 (2018)

    ---
    **Version**: 1.0
    **Created**: November 2025
    **Framework**: Python + Streamlit + Plotly
    """)

# ============================================================================
# COMPARISON FUNCTIONALITY
# ============================================================================

if add_comparison:
    # Generate comparison curve data
    colors = ['red', 'green', 'orange', 'purple']
    color_idx = len(st.session_state.comparison_curves) % len(colors)

    comparison_data = {
        'name': f"{model_type} (W={W_nm:.1f}nm)",
        'model_type': model_type,
        'color': colors[color_idx],
        'Phi_s_range': Phi_s_range,
        'ns_array': ns_array,
        'ns_range': ns_range,
        'Delta_WF_array': Delta_WF_array,
        'with_adsorbates': show_adsorbates,
        'Delta_WF_with_ads': Delta_WF_array + Delta_Phi_dip if show_adsorbates else None,
        'params': {
            'm_star': m_star_ratio,
            'epsilon_r': epsilon_r,
            'W_nm': W_nm
        }
    }

    st.session_state.comparison_curves.append(comparison_data)
    st.sidebar.success(f"Added: {comparison_data['name']}")

if clear_comparison:
    st.session_state.comparison_curves = []
    st.sidebar.info("Comparison curves cleared")

# Display comparison list
if st.session_state.comparison_curves:
    st.sidebar.markdown("### Comparison Curves")
    for i, curve in enumerate(st.session_state.comparison_curves):
        st.sidebar.markdown(f"- {curve['name']}")
