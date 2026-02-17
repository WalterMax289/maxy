"""
Professional chart and visualization generation
Supports multiple chart types with customization
"""

import io
import base64
import logging
from typing import List, Dict, Any, Optional, Union
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

logger = logging.getLogger(__name__)

# Professional color palettes
COLOR_PALETTES = {
    'default': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E'],
    'pastel': ['#FFB4D6', '#A0D5E4', '#FFED99', '#D4E8C1', '#FFC4B0'],
    'dark': ['#1B1B3F', '#16213E', '#0F3460', '#E94560', '#FFAA00'],
    'professional': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
    'rainbow': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
}

class ChartGenerator:
    """Generate professional charts and visualizations"""
    
    @staticmethod
    def fig_to_base64(fig, dpi: int = 100) -> str:
        """Convert matplotlib figure to base64 string"""
        try:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=dpi, facecolor='white')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            return img_base64
        except Exception as e:
            logger.error(f"Error converting figure to base64: {str(e)}")
            plt.close(fig)
            return None
    
    @staticmethod
    def create_pie_chart(
        labels: List[str],
        values: List[float],
        title: str = "Pie Chart",
        palette: str = "default",
        explode: Optional[List[float]] = None
    ) -> Optional[str]:
        """Create professional pie chart"""
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = COLOR_PALETTES.get(palette, COLOR_PALETTES['default'])
            
            if not explode:
                explode = [0.05] * len(labels)
            
            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                autopct='%1.1f%%',
                colors=colors,
                startangle=90,
                explode=explode,
                shadow=True
            )
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            
            # Style text
            for text in texts:
                text.set_fontsize(11)
                text.set_fontweight('bold')
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            return None
    
    @staticmethod
    def create_bar_chart(
        categories: List[str],
        values: List[float],
        title: str = "Bar Chart",
        xlabel: str = "Categories",
        ylabel: str = "Values",
        horizontal: bool = False,
        palette: str = "professional",
        show_values: bool = True
    ) -> Optional[str]:
        """Create professional bar chart"""
        try:
            fig, ax = plt.subplots(figsize=(12, 7))
            colors = COLOR_PALETTES.get(palette, COLOR_PALETTES['professional'])
            
            # Extend colors if needed
            while len(colors) < len(categories):
                colors.extend(colors)
            colors = colors[:len(categories)]
            
            if horizontal:
                bars = ax.barh(categories, values, color=colors, edgecolor='black', linewidth=1.2)
                ax.set_xlabel(ylabel, fontsize=12, fontweight='bold')
                ax.set_ylabel(xlabel, fontsize=12, fontweight='bold')
            else:
                bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)
                ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
                ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_axisbelow(True)
            
            # Add value labels on bars
            if show_values:
                for bar in bars:
                    if horizontal:
                        width = bar.get_width()
                        ax.text(width, bar.get_y() + bar.get_height()/2,
                               f' {width:.2f}', ha='left', va='center',
                               fontsize=10, fontweight='bold')
                    else:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2, height,
                               f'{height:.2f}', ha='center', va='bottom',
                               fontsize=10, fontweight='bold')
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            return None
    
    @staticmethod
    def create_line_chart(
        x: List[float],
        y: List[float],
        title: str = "Line Chart",
        xlabel: str = "X-axis",
        ylabel: str = "Y-axis",
        palette: str = "professional",
        show_points: bool = True,
        multiple_series: Optional[List[Dict]] = None
    ) -> Optional[str]:
        """Create professional line chart"""
        try:
            fig, ax = plt.subplots(figsize=(12, 7))
            colors = COLOR_PALETTES.get(palette, COLOR_PALETTES['professional'])
            
            if multiple_series:
                for i, series in enumerate(multiple_series):
                    color = colors[i % len(colors)]
                    ax.plot(series['x'], series['y'],
                           marker='o' if show_points else '',
                           linewidth=2.5,
                           markersize=7,
                           label=series.get('label', f'Series {i+1}'),
                           color=color,
                           alpha=0.8)
                ax.legend(fontsize=11, loc='best')
            else:
                color = colors[0]
                ax.plot(x, y,
                       marker='o' if show_points else '',
                       linewidth=2.5,
                       markersize=7,
                       color=color,
                       alpha=0.8)
            
            ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating line chart: {str(e)}")
            return None
    
    @staticmethod
    def create_histogram(
        data: List[float],
        bins: int = 20,
        title: str = "Histogram",
        xlabel: str = "Value",
        ylabel: str = "Frequency",
        palette: str = "pastel",
        show_stats: bool = True
    ) -> Optional[str]:
        """Create professional histogram"""
        try:
            fig, ax = plt.subplots(figsize=(12, 7))
            color = COLOR_PALETTES.get(palette, COLOR_PALETTES['pastel'])[0]
            
            n, bins_edges, patches = ax.hist(
                data,
                bins=bins,
                color=color,
                edgecolor='black',
                alpha=0.7,
                linewidth=1.2
            )
            
            ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_axisbelow(True)
            
            # Add statistics text
            if show_stats:
                from data_analyzer import AdvancedAnalyzer
                mean_val = AdvancedAnalyzer.calculate_mean(data)
                median_val = AdvancedAnalyzer.calculate_median(data)
                std_val = AdvancedAnalyzer.calculate_std_dev(data)
                
                stats_text = (
                    f'Count: {len(data)}\n'
                    f'Mean: {mean_val:.2f}\n'
                    f'Median: {median_val:.2f}\n'
                    f'Std Dev: {std_val:.2f}'
                )
                ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
                       fontsize=10, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating histogram: {str(e)}")
            return None
    
    @staticmethod
    def create_scatter_plot(
        x: List[float],
        y: List[float],
        title: str = "Scatter Plot",
        xlabel: str = "X-axis",
        ylabel: str = "Y-axis",
        palette: str = "professional",
        show_regression: bool = True,
        sizes: Optional[List[float]] = None
    ) -> Optional[str]:
        """Create professional scatter plot"""
        try:
            fig, ax = plt.subplots(figsize=(12, 7))
            color = COLOR_PALETTES.get(palette, COLOR_PALETTES['professional'])[0]
            
            scatter_sizes = sizes if sizes else [100] * len(x)
            ax.scatter(x, y, s=scatter_sizes, alpha=0.6, c=color, edgecolors='black', linewidth=0.8)
            
            # Add regression line if requested
            if show_regression and len(x) > 2:
                from data_analyzer import AdvancedAnalyzer
                regression = AdvancedAnalyzer.calculate_regression(x, y)
                
                x_range = np.linspace(min(x), max(x), 100)
                y_range = regression['slope'] * x_range + regression['intercept']
                
                ax.plot(x_range, y_range, 'r--', linewidth=2.5, label='Trend line', alpha=0.8)
                
                # Add regression info
                reg_text = (
                    f"y = {regression['slope']:.4f}x + {regression['intercept']:.4f}\n"
                    f"R² = {regression['r_squared']:.4f}"
                )
                ax.text(0.05, 0.95, reg_text, transform=ax.transAxes,
                       fontsize=10, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
                ax.legend(fontsize=11)
            
            ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating scatter plot: {str(e)}")
            return None
    
    @staticmethod
    def create_box_plot(
        data: Union[List[float], Dict[str, List[float]]],
        title: str = "Box Plot",
        ylabel: str = "Value",
        palette: str = "professional",
        show_points: bool = False
    ) -> Optional[str]:
        """Create professional box plot"""
        try:
            fig, ax = plt.subplots(figsize=(12, 7))
            colors = COLOR_PALETTES.get(palette, COLOR_PALETTES['professional'])
            
            if isinstance(data, dict):
                data_list = list(data.values())
                labels = list(data.keys())
            else:
                data_list = [data]
                labels = ['Data']
            
            # Extend colors if needed
            while len(colors) < len(data_list):
                colors.extend(colors)
            
            bp = ax.boxplot(data_list, labels=labels, patch_artist=True,
                           showmeans=True, meanline=True)
            
            # Style box plot
            for patch, color in zip(bp['boxes'], colors[:len(data_list)]):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
                plt.setp(bp[element], color='black', linewidth=1.5)
            
            # Add points if requested
            if show_points:
                for i, d in enumerate(data_list):
                    x = np.random.normal(i+1, 0.04, size=len(d))
                    ax.scatter(x, d, alpha=0.3, s=30)
            
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_axisbelow(True)
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating box plot: {str(e)}")
            return None
    
    @staticmethod
    def create_heatmap(
        data: List[List[float]],
        title: str = "Heatmap",
        xlabel: str = "X",
        ylabel: str = "Y",
        x_labels: Optional[List[str]] = None,
        y_labels: Optional[List[str]] = None
    ) -> Optional[str]:
        """Create heatmap visualization"""
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('Value', rotation=270, labelpad=20, fontweight='bold')
            
            # Set labels
            if x_labels:
                ax.set_xticks(range(len(x_labels)))
                ax.set_xticklabels(x_labels, rotation=45, ha='right')
            if y_labels:
                ax.set_yticks(range(len(y_labels)))
                ax.set_yticklabels(y_labels)
            
            ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            
            plt.tight_layout()
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            return None
    
    @staticmethod
    def create_combined_chart(
        charts: List[Dict[str, Any]],
        title: str = "Combined Analysis"
    ) -> Optional[str]:
        """Create combined multi-chart visualization"""
        try:
            n_charts = len(charts)
            cols = min(n_charts, 3)
            rows = (n_charts + cols - 1) // cols
            
            fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
            if n_charts == 1:
                axes = [axes]
            else:
                axes = axes.flatten() if rows > 1 or cols > 1 else [axes]
            
            for idx, chart in enumerate(charts):
                ax = axes[idx]
                chart_type = chart.get('type', 'line')
                
                if chart_type == 'bar':
                    ax.bar(chart.get('x', []), chart.get('y', []))
                elif chart_type == 'line':
                    ax.plot(chart.get('x', []), chart.get('y', []))
                
                ax.set_title(chart.get('title', f'Chart {idx+1}'), fontweight='bold')
                ax.grid(True, alpha=0.3)
            
            # Hide extra subplots
            for idx in range(len(charts), len(axes)):
                axes[idx].set_visible(False)
            
            fig.suptitle(title, fontsize=18, fontweight='bold', y=0.995)
            plt.tight_layout()
            
            return ChartGenerator.fig_to_base64(fig)
        
        except Exception as e:
            logger.error(f"Error creating combined chart: {str(e)}")
            return None
