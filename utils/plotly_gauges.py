import plotly.graph_objects as go

def traffic_light_gauge(
    title: str,
    value: float,
    min_val: float,
    max_val: float,
    status: str,
    mom_change: float = None, # type: ignore
    confidence: float = None, # type: ignore
    is_good_up: bool = True  # True if upward MoM change is good, False if downward is good
):
    """
    Plotly gauge with MoM delta arrow, dynamically coloring delta arrows
    based on whether upward movement is positive or negative.

    Parameters
    ----------
    title : str
        Gauge title.
    value : float
        Latest value.
    min_val, max_val : float
        Axis range for gauge.
    status : str
        'green', 'amber', 'red' for bar color.
    mom_change : float, optional
        Month-on-month delta for arrow.
    confidence : float, optional
        Display below gauge.
    is_good_up : bool
        If True, upward MoM change is good (green up, red down).
        If False, downward MoM change is good (green down, red up).
    """

    # --- Color map for bar
    color_map = {
        "green": "#2ecc71",
        "amber": "#f39c12",
        "red": "#e74c3c"
    }

    # --- Delta configuration
    delta_config = None
    if mom_change is not None:
        delta_config = {
            "reference": value - mom_change,
            "position": "top",
            "increasing": {"color": "#2ecc71" if is_good_up else "#e74c3c", "symbol": "▲"},
            "decreasing": {"color": "#e74c3c" if is_good_up else "#2ecc71", "symbol": "▼"},
        }

    # --- Create figure
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta" if mom_change is not None else "gauge+number",
            value=value,
            delta=delta_config,
            title={"text": title},
            gauge={
                "axis": {"range": [min_val, max_val]},
                "bar": {"color": color_map.get(status, "gray")},
                "steps": [
                    {"range": [min_val, min_val + (max_val - min_val)*0.5], "color": "#ecf0f1"},
                    {"range": [min_val + (max_val - min_val)*0.5, min_val + (max_val - min_val)*0.75], "color": "#fef5e7"},
                    {"range": [min_val + (max_val - min_val)*0.75, max_val], "color": "#fdecea"},
                ],
            },
            number={"suffix": "%"} if "%" in title else {}
        )
    )

    # --- Add confidence annotation
    if confidence is not None:
        fig.add_annotation(
            text=f"Confidence: {confidence}%",
            x=0.5,
            y=-0.25,
            showarrow=False,
            font=dict(size=12),
            xref="paper",
            yref="paper",
        )

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig
