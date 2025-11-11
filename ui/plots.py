"""
Plotting functions for 2DEG visualization.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from physics.units import ns_to_display


def create_ns_vs_Phi_s_plot(curves_data, title="Sheet Density vs Surface Potential"):
    """
    Create Figure 1: ns vs Φs plot.

    Parameters
    ----------
    curves_data : list of dict
        List of curve data, each dict containing:
        - 'name': curve label
        - 'Phi_s': array of surface potential values (eV)
        - 'ns': array of sheet density values (m⁻²)
        - 'color': optional color
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()

    for curve in curves_data:
        Phi_s = curve['Phi_s']
        ns = curve['ns']
        name = curve['name']
        color = curve.get('color', None)

        # Convert ns to display units (10¹³ cm⁻²)
        ns_display = ns_to_display(ns)

        fig.add_trace(go.Scatter(
            x=Phi_s,
            y=ns_display,
            mode='lines',
            name=name,
            line=dict(color=color, width=2),
            hovertemplate='Φₛ: %{x:.3f} eV<br>nₛ: %{y:.2f} × 10¹³ cm⁻²<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Surface Potential Φₛ (eV)",
        yaxis_title="Sheet Density nₛ (10¹³ cm⁻²)",
        hovermode='closest',
        template='plotly_white',
        font=dict(size=12),
        width=800,
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig


def create_Delta_WF_vs_ns_plot(curves_data, title="Work Function Change vs Sheet Density"):
    """
    Create Figure 2: ΔWF vs ns plot.

    Parameters
    ----------
    curves_data : list of dict
        List of curve data, each dict containing:
        - 'name': curve label
        - 'ns': array of sheet density values (m⁻²)
        - 'Delta_WF': array of work function change (eV)
        - 'with_adsorbate': bool, whether adsorbates are included
        - 'color': optional color
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()

    for curve in curves_data:
        ns = curve['ns']
        Delta_WF = curve['Delta_WF']
        name = curve['name']
        with_ads = curve.get('with_adsorbate', False)
        color = curve.get('color', None)

        # Convert ns to display units
        ns_display = ns_to_display(ns)

        # Use different line styles for with/without adsorbates
        line_style = 'dash' if with_ads else 'solid'

        fig.add_trace(go.Scatter(
            x=ns_display,
            y=Delta_WF,
            mode='lines',
            name=name,
            line=dict(color=color, width=2, dash=line_style),
            hovertemplate='nₛ: %{x:.2f} × 10¹³ cm⁻²<br>ΔWF: %{y:.3f} eV<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Sheet Density nₛ (10¹³ cm⁻²)",
        yaxis_title="Work Function Change ΔWF (eV)",
        hovermode='closest',
        template='plotly_white',
        font=dict(size=12),
        width=800,
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig


def create_potential_profile_plot(z_nm, V_eV, title="Potential Profile"):
    """
    Create potential energy profile V(z) plot.

    Parameters
    ----------
    z_nm : array
        Depth positions in nm
    V_eV : array or dict of arrays
        Potential energy in eV. Can be single array or dict with multiple curves
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()

    if isinstance(V_eV, dict):
        for name, V in V_eV.items():
            fig.add_trace(go.Scatter(
                x=z_nm,
                y=V,
                mode='lines',
                name=name,
                line=dict(width=2),
                hovertemplate='z: %{x:.2f} nm<br>V: %{y:.3f} eV<extra></extra>'
            ))
    else:
        fig.add_trace(go.Scatter(
            x=z_nm,
            y=V_eV,
            mode='lines',
            line=dict(width=2, color='blue'),
            hovertemplate='z: %{x:.2f} nm<br>V: %{y:.3f} eV<extra></extra>',
            showlegend=False
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Depth z (nm)",
        yaxis_title="Potential Energy V (eV)",
        hovermode='closest',
        template='plotly_white',
        font=dict(size=12),
        width=700,
        height=400
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig


def create_electron_density_plot(z_nm, n_z, title="Electron Density Distribution"):
    """
    Create electron density n(z) profile plot.

    Parameters
    ----------
    z_nm : array
        Depth positions in nm
    n_z : array
        Electron density (arbitrary units)
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=z_nm,
        y=n_z,
        mode='lines',
        line=dict(width=2, color='red'),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.1)',
        hovertemplate='z: %{x:.2f} nm<br>n(z): %{y:.2e}<extra></extra>',
        showlegend=False
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Depth z (nm)",
        yaxis_title="Electron Density n(z) (a.u.)",
        hovermode='closest',
        template='plotly_white',
        font=dict(size=12),
        width=700,
        height=400
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig


def create_xps_weight_plot(z_nm, w_z, title="XPS Sampling Weight"):
    """
    Create XPS weight function w(z) plot.

    Parameters
    ----------
    z_nm : array
        Depth positions in nm
    w_z : array
        Weight function values
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=z_nm,
        y=w_z,
        mode='lines',
        line=dict(width=2, color='green'),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.1)',
        hovertemplate='z: %{x:.2f} nm<br>w(z): %{y:.2e}<extra></extra>',
        showlegend=False
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Depth z (nm)",
        yaxis_title="XPS Weight w(z) (nm⁻¹)",
        hovermode='closest',
        template='plotly_white',
        font=dict(size=12),
        width=700,
        height=400
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig


def create_combined_profile_plot(z_nm, V_eV, n_z=None, w_z=None):
    """
    Create combined plot with V(z), n(z), and w(z).

    Parameters
    ----------
    z_nm : array
        Depth positions in nm
    V_eV : array
        Potential energy in eV
    n_z : array, optional
        Electron density
    w_z : array, optional
        XPS weight function

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure with subplots
    """
    n_plots = 1 + (n_z is not None) + (w_z is not None)

    fig = make_subplots(
        rows=n_plots, cols=1,
        subplot_titles=("Potential V(z)",
                       "Electron Density n(z)" if n_z is not None else None,
                       "XPS Weight w(z)" if w_z is not None else None),
        vertical_spacing=0.12
    )

    # Plot V(z)
    fig.add_trace(
        go.Scatter(x=z_nm, y=V_eV, mode='lines',
                  line=dict(color='blue', width=2), name='V(z)'),
        row=1, col=1
    )

    row = 2
    if n_z is not None:
        fig.add_trace(
            go.Scatter(x=z_nm, y=n_z, mode='lines',
                      line=dict(color='red', width=2), name='n(z)',
                      fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.1)'),
            row=row, col=1
        )
        row += 1

    if w_z is not None:
        fig.add_trace(
            go.Scatter(x=z_nm, y=w_z, mode='lines',
                      line=dict(color='green', width=2), name='w(z)',
                      fill='tozeroy', fillcolor='rgba(0, 255, 0, 0.1)'),
            row=row, col=1
        )

    fig.update_xaxes(title_text="Depth z (nm)", row=n_plots, col=1)
    fig.update_yaxes(title_text="V (eV)", row=1, col=1)

    if n_z is not None:
        fig.update_yaxes(title_text="n(z) (a.u.)", row=2, col=1)

    if w_z is not None:
        fig.update_yaxes(title_text="w(z) (nm⁻¹)", row=n_plots, col=1)

    fig.update_layout(
        height=300 * n_plots,
        width=700,
        template='plotly_white',
        showlegend=False
    )

    return fig


def create_comparison_CL_vs_WF_plot(
    exp_data,
    theory_data=None,
    fit_result=None,
    title="Core Level Shift vs Work Function Change"
):
    """
    Create comparison plot: ΔE_CL vs ΔWF.

    Parameters
    ----------
    exp_data : dict
        Experimental data with 'Delta_WF' and 'Delta_CL'
    theory_data : dict, optional
        Theory data with 'Delta_WF' and 'Delta_CL'
    fit_result : dict, optional
        Fitting results
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()

    # Experimental data
    if exp_data is not None:
        fig.add_trace(go.Scatter(
            x=exp_data['Delta_WF'],
            y=exp_data['Delta_CL'],
            mode='markers',
            name='Experiment',
            marker=dict(size=12, color='red', symbol='circle',
                       line=dict(width=1.5, color='black')),
            hovertemplate='ΔWF: %{x:.3f} eV<br>ΔE_CL: %{y:.3f} eV<extra></extra>'
        ))

    # Theory curve
    if theory_data is not None:
        fig.add_trace(go.Scatter(
            x=theory_data['Delta_WF'],
            y=theory_data['Delta_CL'],
            mode='lines',
            name='Theory',
            line=dict(color='blue', width=3),
            hovertemplate='ΔWF: %{x:.3f} eV<br>ΔE_CL: %{y:.3f} eV<extra></extra>'
        ))

    # Fitted curve
    if fit_result is not None and 'theory_Delta_CL' in fit_result:
        # Sort for smooth line
        sort_idx = np.argsort(exp_data['Delta_WF'])
        fig.add_trace(go.Scatter(
            x=exp_data['Delta_WF'][sort_idx],
            y=fit_result['theory_Delta_CL'][sort_idx],
            mode='lines',
            name=f"Fit (η={fit_result['eta_fit']:.3f}, R²={fit_result['r_squared']:.3f})",
            line=dict(color='green', width=3, dash='dash'),
            hovertemplate='ΔWF: %{x:.3f} eV<br>ΔE_CL (fit): %{y:.3f} eV<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Work Function Change ΔWF (eV)",
        yaxis_title="Core Level Shift ΔE_CL (eV)",
        hovermode='closest',
        template='plotly_white',
        font=dict(size=12),
        width=800,
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    return fig


def create_residual_analysis_plot(exp_data, fit_result):
    """
    Create comprehensive residual analysis plots.

    Parameters
    ----------
    exp_data : dict
        Experimental data
    fit_result : dict
        Fitting results with residuals

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure with subplots
    """
    from plotly.subplots import make_subplots
    from scipy import stats

    residuals = fit_result['residuals']

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Residuals vs ΔWF',
            'Residuals Distribution',
            'Predicted vs Actual',
            'Residual Statistics'
        ),
        specs=[[{"type": "scatter"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "table"}]]
    )

    # 1. Residuals vs ΔWF
    fig.add_trace(
        go.Scatter(
            x=exp_data['Delta_WF'],
            y=residuals,
            mode='markers',
            marker=dict(size=10, color='blue'),
            name='Residuals',
            showlegend=False
        ),
        row=1, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)

    # 2. Histogram
    fig.add_trace(
        go.Histogram(
            x=residuals,
            nbinsx=15,
            marker=dict(color='lightblue', line=dict(color='black', width=1)),
            name='Distribution',
            showlegend=False
        ),
        row=1, col=2
    )

    # 3. Predicted vs Actual
    predicted = exp_data['Delta_CL'] - residuals
    fig.add_trace(
        go.Scatter(
            x=exp_data['Delta_CL'],
            y=predicted,
            mode='markers',
            marker=dict(size=10, color='green'),
            name='Data',
            showlegend=False
        ),
        row=2, col=1
    )
    # Perfect fit line
    min_val = min(exp_data['Delta_CL'].min(), predicted.min())
    max_val = max(exp_data['Delta_CL'].max(), predicted.max())
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Perfect fit',
            showlegend=False
        ),
        row=2, col=1
    )

    # 4. Statistics table
    mean_res = np.mean(residuals)
    std_res = np.std(residuals)
    max_res = np.max(np.abs(residuals))

    fig.add_trace(
        go.Table(
            header=dict(values=['Statistic', 'Value'],
                       fill_color='lightgray',
                       align='left'),
            cells=dict(values=[
                ['Mean residual', 'Std residual', 'Max |residual|', 'RMSE', 'R²'],
                [f'{mean_res:.4f} eV', f'{std_res:.4f} eV', f'{max_res:.4f} eV',
                 f"{fit_result['rmse']:.4f} eV", f"{fit_result['r_squared']:.4f}"]
            ],
            fill_color='white',
            align='left')
        ),
        row=2, col=2
    )

    # Update axes labels
    fig.update_xaxes(title_text="ΔWF (eV)", row=1, col=1)
    fig.update_yaxes(title_text="Residual (eV)", row=1, col=1)

    fig.update_xaxes(title_text="Residual (eV)", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=2)

    fig.update_xaxes(title_text="Actual ΔE_CL (eV)", row=2, col=1)
    fig.update_yaxes(title_text="Predicted ΔE_CL (eV)", row=2, col=1)

    fig.update_layout(
        height=800,
        showlegend=False,
        template='plotly_white'
    )

    return fig


def create_annealing_trajectory_plot(exp_data, title="Annealing Trajectory"):
    """
    Create annealing trajectory plot showing evolution with temperature.

    Parameters
    ----------
    exp_data : dict
        Experimental data with 'T_degC', 'Delta_WF', 'Delta_CL'
    title : str
        Plot title

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object
    """
    if 'T_degC' not in exp_data:
        return None

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('ΔWF vs Temperature', 'ΔE_CL vs Temperature')
    )

    # ΔWF vs T
    fig.add_trace(
        go.Scatter(
            x=exp_data['T_degC'],
            y=exp_data['Delta_WF'],
            mode='lines+markers',
            marker=dict(size=10, color='red'),
            line=dict(color='red', width=2),
            name='ΔWF',
            hovertemplate='T: %{x}°C<br>ΔWF: %{y:.3f} eV<extra></extra>'
        ),
        row=1, col=1
    )

    # ΔE_CL vs T
    fig.add_trace(
        go.Scatter(
            x=exp_data['T_degC'],
            y=exp_data['Delta_CL'],
            mode='lines+markers',
            marker=dict(size=10, color='blue'),
            line=dict(color='blue', width=2),
            name='ΔE_CL',
            hovertemplate='T: %{x}°C<br>ΔE_CL: %{y:.3f} eV<extra></extra>'
        ),
        row=1, col=2
    )

    # Update axes
    fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_yaxes(title_text="ΔWF (eV)", row=1, col=1)

    fig.update_xaxes(title_text="Temperature (°C)", row=1, col=2)
    fig.update_yaxes(title_text="ΔE_CL (eV)", row=1, col=2)

    fig.update_layout(
        title=title,
        height=400,
        showlegend=False,
        template='plotly_white'
    )

    return fig
