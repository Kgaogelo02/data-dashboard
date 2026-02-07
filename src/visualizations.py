"""
Visualization functions for the dashboard using Plotly.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class Visualizer:
    """Create interactive visualizations."""
    
    @staticmethod
    def create_revenue_line_chart(df, x_col, y_col, title="Revenue Trend"):
        """Create a line chart for revenue trends."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        fig = px.line(df, x=x_col, y=y_col, 
                     title=title,
                     labels={x_col: x_col.title(), y_col: 'Revenue ($)'},
                     markers=True)
        
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        fig.update_traces(line_color='#1f77b4', line_width=2)
        
        return fig
    
    @staticmethod
    def create_bar_chart(df, x_col, y_col, title="", orientation='v', color=None):
        """Create a bar chart."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        if orientation == 'h':
            fig = px.bar(df, y=x_col, x=y_col, 
                        title=title,
                        orientation='h',
                        color=color,
                        labels={x_col: x_col.title(), y_col: 'Revenue ($)'})
        else:
            fig = px.bar(df, x=x_col, y=y_col, 
                        title=title,
                        color=color,
                        labels={x_col: x_col.title(), y_col: 'Revenue ($)'})
        
        fig.update_layout(
            showlegend=True if color else False,
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(df, names_col, values_col, title="Distribution"):
        """Create a pie chart."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        fig = px.pie(df, names=names_col, values=values_col,
                    title=title,
                    hole=0.3)  # Donut chart
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_multi_bar_chart(df, x_col, y_cols, title="", barmode='group'):
        """Create a multi-series bar chart."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        fig = go.Figure()
        
        for col in y_cols:
            fig.add_trace(go.Bar(
                x=df[x_col],
                y=df[col],
                name=col.replace('_', ' ').title()
            ))
        
        fig.update_layout(
            title=title,
            barmode=barmode,
            template='plotly_white',
            height=400,
            xaxis_title=x_col.title(),
            yaxis_title='Value'
        )
        
        return fig
    
    @staticmethod
    def create_scatter_plot(df, x_col, y_col, color_col=None, size_col=None, title=""):
        """Create a scatter plot."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        fig = px.scatter(df, x=x_col, y=y_col,
                        color=color_col,
                        size=size_col,
                        title=title,
                        labels={x_col: x_col.replace('_', ' ').title(),
                               y_col: y_col.replace('_', ' ').title()})
        
        fig.update_layout(
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_heatmap(df, x_col, y_col, value_col, title="Heatmap"):
        """Create a heatmap."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Pivot data for heatmap
        pivot_df = df.pivot(index=y_col, columns=x_col, values=value_col)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Blues'
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=400,
            xaxis_title=x_col.title(),
            yaxis_title=y_col.title()
        )
        
        return fig
    
    @staticmethod
    def create_metric_cards(metrics_dict):
        """Create metric display cards."""
        # This returns data for Streamlit metric display
        return metrics_dict
    
    @staticmethod
    def create_combo_chart(df, x_col, bar_cols, line_cols, title=""):
        """Create a combination chart with bars and lines."""
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add bar traces
        for col in bar_cols:
            fig.add_trace(
                go.Bar(x=df[x_col], y=df[col], name=col.title()),
                secondary_y=False
            )
        
        # Add line traces
        for col in line_cols:
            fig.add_trace(
                go.Scatter(x=df[x_col], y=df[col], name=col.title(), mode='lines+markers'),
                secondary_y=True
            )
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=400
        )
        
        return fig