"""
Advanced statistical analysis and data processing
Provides comprehensive statistical insights and pattern detection
"""

import math
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class AdvancedAnalyzer:
    """Advanced statistical and data analysis"""
    
    @staticmethod
    def calculate_mean(data: List[float]) -> float:
        """Calculate arithmetic mean"""
        if not data:
            return 0
        return sum(data) / len(data)
    
    @staticmethod
    def calculate_median(data: List[float]) -> float:
        """Calculate median value"""
        if not data:
            return 0
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        return sorted_data[n // 2]
    
    @staticmethod
    def calculate_mode(data: List[float]) -> List[float]:
        """Calculate mode(s) - most frequent value(s)"""
        if not data:
            return []
        frequency = Counter(data)
        max_freq = max(frequency.values())
        modes = [k for k, v in frequency.items() if v == max_freq]
        return modes if max_freq > 1 else []
    
    @staticmethod
    def calculate_variance(data: List[float], sample: bool = True) -> float:
        """Calculate variance"""
        if len(data) < 2:
            return 0
        mean = AdvancedAnalyzer.calculate_mean(data)
        squared_diff_sum = sum((x - mean) ** 2 for x in data)
        if sample:
            return squared_diff_sum / (len(data) - 1)
        return squared_diff_sum / len(data)
    
    @staticmethod
    def calculate_std_dev(data: List[float], sample: bool = True) -> float:
        """Calculate standard deviation"""
        variance = AdvancedAnalyzer.calculate_variance(data, sample)
        return math.sqrt(variance)
    
    @staticmethod
    def calculate_range(data: List[float]) -> Tuple[float, float, float]:
        """Calculate range (min, max, range)"""
        if not data:
            return 0, 0, 0
        return min(data), max(data), max(data) - min(data)
    
    @staticmethod
    def calculate_iqr(data: List[float]) -> Tuple[float, float, float, float]:
        """Calculate Interquartile Range and quartiles"""
        if len(data) < 4:
            return 0, 0, 0, 0
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        # Calculate quartiles
        q1_idx = n // 4
        q2_idx = n // 2
        q3_idx = 3 * n // 4
        
        q1 = sorted_data[q1_idx]
        q2 = sorted_data[q2_idx]
        q3 = sorted_data[q3_idx]
        iqr = q3 - q1
        
        return q1, q2, q3, iqr
    
    @staticmethod
    def calculate_percentiles(data: List[float], percentiles: List[int] = None) -> Dict[int, float]:
        """Calculate percentiles"""
        if percentiles is None:
            percentiles = [10, 25, 50, 75, 90, 95, 99]
        
        if not data or len(data) < 2:
            return {p: 0 for p in percentiles}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        result = {}
        
        for p in percentiles:
            if p < 0 or p > 100:
                continue
            index = (p / 100) * (n - 1)
            lower = int(index)
            upper = min(lower + 1, n - 1)
            weight = index - lower
            result[p] = sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
        
        return result
    
    @staticmethod
    def detect_outliers(data: List[float], method: str = "iqr", threshold: float = 1.5) -> Tuple[List[float], List[int]]:
        """
        Detect outliers using specified method
        method: 'iqr' (Interquartile Range) or 'zscore'
        """
        if len(data) < 4:
            return [], []
        
        outliers = []
        indices = []
        
        if method == "iqr":
            q1, _, q3, iqr = AdvancedAnalyzer.calculate_iqr(data)
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            for idx, x in enumerate(data):
                if x < lower_bound or x > upper_bound:
                    outliers.append(x)
                    indices.append(idx)
        
        elif method == "zscore":
            mean = AdvancedAnalyzer.calculate_mean(data)
            std = AdvancedAnalyzer.calculate_std_dev(data)
            
            if std == 0:
                return [], []
            
            for idx, x in enumerate(data):
                z_score = abs((x - mean) / std)
                if z_score > threshold:
                    outliers.append(x)
                    indices.append(idx)
        
        return outliers, indices
    
    @staticmethod
    def calculate_skewness(data: List[float]) -> float:
        """Calculate skewness (measure of asymmetry)"""
        if len(data) < 3:
            return 0
        
        mean = AdvancedAnalyzer.calculate_mean(data)
        std = AdvancedAnalyzer.calculate_std_dev(data)
        n = len(data)
        
        if std == 0:
            return 0
        
        skewness = (sum((x - mean) ** 3 for x in data) / n) / (std ** 3)
        return skewness
    
    @staticmethod
    def calculate_kurtosis(data: List[float]) -> float:
        """Calculate kurtosis (measure of tail heaviness)"""
        if len(data) < 4:
            return 0
        
        mean = AdvancedAnalyzer.calculate_mean(data)
        std = AdvancedAnalyzer.calculate_std_dev(data)
        n = len(data)
        
        if std == 0:
            return 0
        
        kurtosis = (sum((x - mean) ** 4 for x in data) / n) / (std ** 4) - 3
        return kurtosis
    
    @staticmethod
    def calculate_correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        mean_x = AdvancedAnalyzer.calculate_mean(x)
        mean_y = AdvancedAnalyzer.calculate_mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(
            sum((xi - mean_x) ** 2 for xi in x) * 
            sum((yi - mean_y) ** 2 for yi in y)
        )
        
        return numerator / denominator if denominator != 0 else 0
    
    @staticmethod
    def calculate_regression(x: List[float], y: List[float]) -> Dict[str, float]:
        """Calculate linear regression (slope, intercept, R-squared)"""
        if len(x) != len(y) or len(x) < 2:
            return {'slope': 0, 'intercept': 0, 'r_squared': 0, 'se': 0}
        
        n = len(x)
        mean_x = AdvancedAnalyzer.calculate_mean(x)
        mean_y = AdvancedAnalyzer.calculate_mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = sum((xi - mean_x) ** 2 for xi in x)
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = mean_y - slope * mean_x
        
        # Calculate R-squared
        ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
        ss_tot = sum((yi - mean_y) ** 2 for yi in y)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Calculate standard error
        se = math.sqrt(ss_res / (n - 2)) if n > 2 else 0
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'se': se
        }
    
    @staticmethod
    def calculate_moving_average(data: List[float], window: int = 5) -> List[float]:
        """Calculate simple moving average"""
        if len(data) < window:
            return []
        
        return [
            sum(data[i:i+window]) / window 
            for i in range(len(data) - window + 1)
        ]
    
    @staticmethod
    def detect_trends(data: List[float]) -> Dict[str, Any]:
        """Detect data trends"""
        if len(data) < 3:
            return {'trend': 'insufficient_data'}
        
        # Calculate linear regression
        x = list(range(len(data)))
        regression = AdvancedAnalyzer.calculate_regression(x, data)
        
        slope = regression['slope']
        r_squared = regression['r_squared']
        
        if slope > 0.1:
            trend = "upward"
        elif slope < -0.1:
            trend = "downward"
        else:
            trend = "stable"
        
        # Calculate acceleration
        if len(data) >= 4:
            first_half = data[:len(data)//2]
            second_half = data[len(data)//2:]
            
            slope1 = AdvancedAnalyzer.calculate_regression(list(range(len(first_half))), first_half)['slope']
            slope2 = AdvancedAnalyzer.calculate_regression(list(range(len(second_half))), second_half)['slope']
            
            acceleration = slope2 - slope1
        else:
            acceleration = 0
        
        return {
            'trend': trend,
            'slope': slope,
            'r_squared': r_squared,
            'acceleration': acceleration,
            'strength': 'strong' if abs(r_squared) > 0.7 else 'moderate' if abs(r_squared) > 0.4 else 'weak'
        }
    
    @staticmethod
    def calculate_cv(data: List[float]) -> float:
        """Calculate coefficient of variation (std dev / mean)"""
        mean = AdvancedAnalyzer.calculate_mean(data)
        if mean == 0:
            return 0
        std_dev = AdvancedAnalyzer.calculate_std_dev(data)
        return (std_dev / mean) * 100  # As percentage
    
    @staticmethod
    def generate_comprehensive_analysis(data: List[float]) -> Dict[str, Any]:
        """Generate comprehensive statistical analysis"""
        try:
            logger.info(f"Starting comprehensive analysis on {len(data)} data points")
            
            mean_val = AdvancedAnalyzer.calculate_mean(data)
            median_val = AdvancedAnalyzer.calculate_median(data)
            mode_vals = AdvancedAnalyzer.calculate_mode(data)
            std_dev = AdvancedAnalyzer.calculate_std_dev(data)
            variance = AdvancedAnalyzer.calculate_variance(data)
            range_min, range_max, range_val = AdvancedAnalyzer.calculate_range(data)
            q1, q2, q3, iqr = AdvancedAnalyzer.calculate_iqr(data)
            skewness = AdvancedAnalyzer.calculate_skewness(data)
            kurtosis = AdvancedAnalyzer.calculate_kurtosis(data)
            cv = AdvancedAnalyzer.calculate_cv(data)
            outliers, outlier_indices = AdvancedAnalyzer.detect_outliers(data)
            percentiles = AdvancedAnalyzer.calculate_percentiles(data)
            trends = AdvancedAnalyzer.detect_trends(data)
            
            return {
                'count': len(data),
                'central_tendency': {
                    'mean': round(mean_val, 4),
                    'median': round(median_val, 4),
                    'mode': [round(m, 4) for m in mode_vals] if mode_vals else None
                },
                'dispersion': {
                    'std_dev': round(std_dev, 4),
                    'variance': round(variance, 4),
                    'cv': round(cv, 2),  # Coefficient of variation %
                    'range': {
                        'min': round(range_min, 4),
                        'max': round(range_max, 4),
                        'span': round(range_val, 4)
                    }
                },
                'quartiles': {
                    'q1': round(q1, 4),
                    'median': round(q2, 4),
                    'q3': round(q3, 4),
                    'iqr': round(iqr, 4)
                },
                'shape': {
                    'skewness': round(skewness, 4),
                    'skew_interpretation': AdvancedAnalyzer._interpret_skewness(skewness),
                    'kurtosis': round(kurtosis, 4),
                    'kurtosis_interpretation': AdvancedAnalyzer._interpret_kurtosis(kurtosis)
                },
                'outliers': {
                    'count': len(outliers),
                    'values': [round(o, 4) for o in outliers[:10]],  # Limit to 10
                    'indices': outlier_indices[:10] if outlier_indices else []
                },
                'percentiles': {str(k): round(v, 4) for k, v in percentiles.items()},
                'trends': trends
            }
        
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def _interpret_skewness(skewness: float) -> str:
        """Interpret skewness value"""
        abs_skew = abs(skewness)
        if abs_skew < 0.5:
            direction = "symmetric"
        elif skewness > 0:
            direction = f"right-skewed (positive, {abs_skew:.2f})"
        else:
            direction = f"left-skewed (negative, {abs_skew:.2f})"
        return direction
    
    @staticmethod
    def _interpret_kurtosis(kurtosis: float) -> str:
        """Interpret kurtosis value"""
        if abs(kurtosis) < 0.5:
            return "mesokurtic (normal tails)"
        elif kurtosis > 0:
            return f"leptokurtic (heavy tails, {kurtosis:.2f})"
        else:
            return f"platykurtic (light tails, {kurtosis:.2f})"
    
    @staticmethod
    def generate_insights(analysis: Dict[str, Any]) -> List[str]:
        """Generate human-readable insights from analysis"""
        insights = []
        
        try:
            if 'error' in analysis:
                return [f"Error during analysis: {analysis['error']}"]
            
            # Insight about central tendency
            mean = analysis['central_tendency']['mean']
            median = analysis['central_tendency']['median']
            if abs(mean - median) > (analysis['dispersion']['std_dev'] * 0.1):
                insights.append(f"Mean ({mean}) differs significantly from median ({median}), suggesting skewed data.")
            
            # Insight about spread
            cv = analysis['dispersion']['cv']
            if cv > 50:
                insights.append(f"High variability detected (CV: {cv}%). Data points are highly dispersed.")
            elif cv < 10:
                insights.append(f"Low variability detected (CV: {cv}%). Data points are tightly clustered.")
            
            # Insight about skewness
            skew = analysis['shape']['skewness']
            if abs(skew) > 0.5:
                insights.append(f"Data is {analysis['shape']['skew_interpretation']}. Consider this when interpreting results.")
            
            # Insight about outliers
            outlier_count = analysis['outliers']['count']
            if outlier_count > 0:
                pct = (outlier_count / analysis['count']) * 100
                insights.append(f"Detected {outlier_count} outliers ({pct:.1f}% of data). Review these values for data quality issues.")
            
            # Insight about trends
            trend_data = analysis['trends']
            if trend_data.get('trend') != 'insufficient_data':
                trend = trend_data.get('trend', 'unknown')
                strength = trend_data.get('strength', 'unknown')
                insights.append(f"Data shows {strength} {trend} trend (slope: {trend_data.get('slope', 0):.4f}).")
            
            # Insight about distribution shape
            kurtosis_interp = analysis['shape']['kurtosis_interpretation']
            insights.append(f"Distribution is {kurtosis_interp}.")
            
            return insights if insights else ["Data appears normally distributed with no significant anomalies."]
        
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return [f"Could not generate insights: {str(e)}"]


class CorrelationAnalyzer:
    """Analyze correlations between datasets"""
    
    @staticmethod
    def find_correlations(datasets: Dict[str, List[float]]) -> Dict[str, Any]:
        """Find correlations between multiple datasets"""
        if len(datasets) < 2:
            return {'error': 'At least 2 datasets required'}
        
        names = list(datasets.keys())
        correlations = {}
        
        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                corr = AdvancedAnalyzer.calculate_correlation(
                    datasets[name1],
                    datasets[name2]
                )
                pair_name = f"{name1} vs {name2}"
                correlations[pair_name] = {
                    'correlation': round(corr, 4),
                    'interpretation': CorrelationAnalyzer._interpret_correlation(corr)
                }
        
        return correlations
    
    @staticmethod
    def _interpret_correlation(corr: float) -> str:
        """Interpret correlation value"""
        abs_corr = abs(corr)
        if abs_corr > 0.9:
            strength = "very strong"
        elif abs_corr > 0.7:
            strength = "strong"
        elif abs_corr > 0.5:
            strength = "moderate"
        elif abs_corr > 0.3:
            strength = "weak"
        else:
            strength = "very weak"
        
        direction = "positive" if corr > 0 else "negative"
        return f"{strength} {direction} correlation"
