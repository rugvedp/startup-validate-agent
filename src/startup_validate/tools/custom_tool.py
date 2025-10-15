from crewai.tools import BaseTool
from typing import Type, List, Dict, Union, Optional, Any
from pydantic import BaseModel, Field, validator
import json
import urllib.parse


class QuickChartToolInput(BaseModel):
    """Input schema for QuickChartTool to generate chart URLs."""
    chart_type: str = Field(..., description="Type of chart: bar, line, pie, doughnut, scatter, sparkline, progressBar, radialGauge")
    labels: Optional[List[str]] = Field(None, description="Labels for the X-axis or categories")
    datasets: List[Dict[str, Any]] = Field(
        ..., description="List of datasets with 'label', 'data', optional 'backgroundColor', 'borderColor', 'fill'"
    )
    title: Optional[str] = Field(None, description="Optional title for the chart")
    width: int = Field(800, description="Width of the chart in pixels (100-2000)")
    height: int = Field(400, description="Height of the chart in pixels (100-2000)")
    theme: Optional[str] = Field("default", description="Chart theme: default, dark, corporate, financial, modern, colorful")
    format: Optional[str] = Field("png", description="Output format: png, jpeg, svg, webp")
    background_color: Optional[str] = Field(None, description="Chart background color (hex, rgb, rgba)")
    
    @validator('datasets', pre=True)
    def validate_datasets(cls, v):
        """Clean and validate datasets to handle fill parameter properly."""
        if not isinstance(v, list):
            raise ValueError("Datasets must be a list")
        
        cleaned_datasets = []
        for dataset in v:
            if not isinstance(dataset, dict):
                raise ValueError("Each dataset must be a dictionary")
            
            # Clean the dataset by removing or converting problematic values
            cleaned_dataset = {}
            for key, value in dataset.items():
                if key == 'fill' and isinstance(value, bool):
                    # Convert boolean fill to string or remove it
                    if value:
                        cleaned_dataset[key] = 'origin'
                    # If False, we can omit the fill property entirely
                else:
                    cleaned_dataset[key] = value
            
            cleaned_datasets.append(cleaned_dataset)
        
        return cleaned_datasets


class QuickChartTool(BaseTool):
    name: str = "QuickChart Generator"
    description: str = (
        "Generates QuickChart.io URLs for rendering professional charts. "
        "Supports common chart types with themes and basic customization. "
        "Perfect for financial reports and dashboards."
    )
    args_schema: Type[BaseModel] = QuickChartToolInput
    
    def _get_theme_colors(self, theme: str) -> List[str]:
        """Get color palette for theme."""
        palettes = {
            "default": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"],
            "dark": ["#1e40af", "#059669", "#d97706", "#dc2626", "#7c3aed", "#0891b2"],
            "corporate": ["#1e3a8a", "#047857", "#92400e", "#991b1b", "#5b21b6", "#0e7490"],
            "financial": ["#1e40af", "#059669", "#d97706", "#dc2626", "#7c3aed", "#0891b2"],
            "modern": ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"],
            "colorful": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#feca57", "#ff9ff3"]
        }
        return palettes.get(theme, palettes["default"])

    def _run(
        self,
        chart_type: str,
        datasets: List[Dict[str, Any]],
        labels: Optional[List[str]] = None,
        title: Optional[str] = None,
        width: int = 800,
        height: int = 400,
        theme: str = "default",
        format: str = "png",
        background_color: Optional[str] = None
    ) -> str:
        try:
            # Basic validation
            if not (100 <= width <= 2000) or not (100 <= height <= 2000):
                raise ValueError("Width and height must be between 100 and 2000 pixels")
            
            if not datasets or not isinstance(datasets, list):
                raise ValueError("Datasets must be a non-empty list")
            
            # Apply theme colors if not specified
            datasets = self._apply_theme_colors(datasets, theme)
            
            # Build chart configuration
            chart_config = {
                "type": chart_type,
                "data": {
                    "datasets": datasets
                }
            }
            
            # Add labels if provided
            if labels:
                chart_config["data"]["labels"] = labels
            
            # Add background color
            if background_color:
                chart_config["data"]["backgroundColor"] = background_color
            
            # Build basic options
            options = {
                "responsive": True,
                "plugins": {
                    "legend": {"display": True, "position": "top"}
                }
            }
            
            # Add title
            if title:
                options["plugins"]["title"] = {
                    "display": True,
                    "text": title,
                    "font": {"size": 16, "weight": "bold"}
                }
            
            chart_config["options"] = options
            
            # Build URL parameters
            params = {
                "c": json.dumps(chart_config),
                "width": width,
                "height": height,
                "format": format
            }
            
            # Generate URL
            query_string = urllib.parse.urlencode(params)
            url = f"https://quickchart.io/chart?{query_string}"
            
            return url

        except Exception as e:
            return f"Error generating chart URL: {str(e)}"
    
    def _apply_theme_colors(self, datasets: List[Dict], theme: str) -> List[Dict]:
        """Apply theme colors to datasets that don't have colors specified."""
        colors = self._get_theme_colors(theme)
        
        for i, dataset in enumerate(datasets):
            # Apply background colors if not specified
            if "backgroundColor" not in dataset:
                if isinstance(dataset["data"], list) and len(dataset["data"]) > 0:
                    if isinstance(dataset["data"][0], (int, float)):
                        # For simple data, use single color
                        dataset["backgroundColor"] = colors[i % len(colors)]
                    else:
                        # For complex data, use color array
                        dataset["backgroundColor"] = [colors[j % len(colors)] for j in range(len(dataset["data"]))]
            
            # Apply border colors if not specified
            if "borderColor" not in dataset:
                dataset["borderColor"] = dataset.get("backgroundColor", colors[i % len(colors)])
        
        return datasets

    @staticmethod
    def create_bar_chart(labels: List[str], data: List[float], title: str = None, 
                        theme: str = "default", width: int = 800, height: int = 400) -> str:
        """Create a bar chart."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="bar",
            labels=labels,
            datasets=[{
                "label": "Data",
                "data": data
            }],
            title=title,
            theme=theme,
            width=width,
            height=height
        )

    @staticmethod
    def create_line_chart(labels: List[str], data: List[float], title: str = None,
                         theme: str = "default", width: int = 800, height: int = 400) -> str:
        """Create a line chart."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="line",
            labels=labels,
            datasets=[{
                "label": "Data",
                "data": data,
                "tension": 0.4
            }],
            title=title,
            theme=theme,
            width=width,
            height=height
        )

    @staticmethod
    def create_pie_chart(labels: List[str], data: List[float], title: str = None,
                        theme: str = "default", width: int = 400, height: int = 400) -> str:
        """Create a pie chart."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="pie",
            labels=labels,
            datasets=[{
                "data": data
            }],
            title=title,
            theme=theme,
            width=width,
            height=height
        )

    @staticmethod
    def create_doughnut_chart(labels: List[str], data: List[float], title: str = None,
                             theme: str = "default", width: int = 400, height: int = 400) -> str:
        """Create a doughnut chart."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="doughnut",
            labels=labels,
            datasets=[{
                "data": data
            }],
            title=title,
            theme=theme,
            width=width,
            height=height
        )

    @staticmethod
    def create_sparkline(data: List[float], theme: str = "default") -> str:
        """Create a sparkline chart."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="sparkline",
            datasets=[{
                "data": data
            }],
            theme=theme,
            width=200,
            height=50
        )

    @staticmethod
    def create_progress_bar(value: float, theme: str = "default") -> str:
        """Create a progress bar."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="progressBar",
            datasets=[{
                "data": [value]
            }],
            theme=theme,
            width=300,
            height=30
        )

    @staticmethod
    def create_radial_gauge(value: float, theme: str = "default") -> str:
        """Create a radial gauge chart."""
        tool = QuickChartTool()
        return tool._run(
            chart_type="radialGauge",
            datasets=[{
                "data": [value]
            }],
            title=str(value),
            theme=theme,
            width=300,
            height=300
        )

    @staticmethod
    def create_financial_chart(labels: List[str], data: List[float], 
                              chart_type: str = "line", title: str = None) -> str:
        """Create a financial chart with corporate theme."""
        tool = QuickChartTool()
        return tool._run(
            chart_type=chart_type,
            labels=labels,
            datasets=[{
                "label": "Financial Data",
                "data": data
            }],
            title=title,
            theme="financial",
            width=1000,
            height=500
        )
