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
