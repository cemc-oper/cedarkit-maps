"""
EastAsiaMapTemplate 集成测试

测试类型: 集成测试 (Integration Test)
测试目标: 验证 EastAsiaMapTemplate 与 Panel、Chart、Layer 等组件的协同工作
测试内容:
    1. 等值线填充图 (contourf) - 温度场
    2. 等值线图 (contour) - 气压场
    3. 风羽图 (barb) - 风场
    4. 组合图 - 多要素叠加
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from cedarkit.maps.domains import EastAsiaMapTemplate
from cedarkit.maps.chart import Panel
from cedarkit.maps.style import ContourStyle, BarbStyle


class TestEastAsiaMapTemplateContourf:
    
    def test_contourf_temperature(
        self, 
        sample_temperature_field, 
        sample_start_time,
        sample_forecast_time,
        temperature_style,
        output_dir
    ):
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        
        panel.plot(sample_temperature_field, style=temperature_style)

        domain.set_title(
            panel=panel,
            graph_name="2m Temperature (°C)",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        
        domain.add_colorbar(panel=panel, style=temperature_style)
        
        output_path = output_dir / "east_asia_temperature_contourf.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"
    
    def test_contourf_precipitation(
        self,
        sample_precipitation_field,
        sample_start_time,
        sample_forecast_time,
        precipitation_style,
        output_dir
    ):
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        panel.plot(sample_precipitation_field, style=precipitation_style)
        
        domain.set_title(
            panel=panel,
            graph_name="24h Precipitation (mm)",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        domain.add_colorbar(panel=panel, style=precipitation_style)
        
        output_path = output_dir / "east_asia_precipitation_contourf.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"


class TestEastAsiaMapTemplateContour:
    
    def test_pressure_contour(
        self,
        sample_pressure_field,
        sample_start_time,
        sample_forecast_time,
        output_dir
    ):
        levels = np.arange(990, 1030, 2.5)

        style = ContourStyle(
            colors="blue",
            levels=levels,
            linewidths=1,
            fill=False,
        )
        
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        panel.plot(sample_pressure_field, style=style)
        
        domain.set_title(
            panel=panel,
            graph_name="MSLP (hPa)",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        
        output_path = output_dir / "east_asia_pressure_contour.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"


class TestEastAsiaMapTemplateBarb:
    def test_wind_barb(
        self,
        sample_wind_fields,
        sample_start_time,
        sample_forecast_time,
        output_dir
    ):
        u_field, v_field = sample_wind_fields
        
        style = BarbStyle(
            length=5,
            linewidth=0.4,
            barbcolor="blue",
            flagcolor="blue",
        )
        
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        
        panel.charts[0].plot([u_field, v_field], style=style, layer=[0])
        
        domain.set_title(
            panel=panel,
            graph_name="10m Wind (m/s)",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        
        output_path = output_dir / "east_asia_wind_barb.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"


class TestEastAsiaMapTemplateCombined:
    def test_temperature_with_wind(
        self,
        sample_temperature_field,
        sample_wind_fields,
        sample_start_time,
        sample_forecast_time,
        temperature_style,
        output_dir
    ):
        u_field, v_field = sample_wind_fields

        wind_style = BarbStyle(
            length=4,
            linewidth=0.3,
            barbcolor="black",
            flagcolor="black",
        )
        
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)

        panel.plot(sample_temperature_field, style=temperature_style)
        panel.charts[0].plot([u_field, v_field], style=wind_style, layer=[0])
        
        domain.set_title(
            panel=panel,
            graph_name="2m Temperature (°C) & 10m Wind",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        domain.add_colorbar(panel=panel, style=temperature_style)
        
        output_path = output_dir / "east_asia_temperature_wind_combined.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"
    
    def test_pressure_contour_with_temperature_fill(
        self,
        sample_temperature_field,
        sample_pressure_field,
        sample_start_time,
        sample_forecast_time,
        temperature_style,
        output_dir
    ):
        pressure_levels = np.arange(990, 1030, 4)
        pressure_style = ContourStyle(
            colors="blue",
            levels=pressure_levels,
            linewidths=1.0,
            fill=False,
        )
        
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        
        panel.plot(sample_temperature_field, style=temperature_style)
        panel.plot(sample_pressure_field, style=pressure_style)
        
        domain.set_title(
            panel=panel,
            graph_name="MSLP (hPa) & 2m Temperature (°C)",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        domain.add_colorbar(panel=panel, style=temperature_style)
        
        output_path = output_dir / "east_asia_pressure_temperature_combined.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"


class TestEastAsiaMapTemplateOptions:
    def test_without_sub_area(
        self,
        sample_temperature_field,
        sample_start_time,
        sample_forecast_time,
        temperature_style,
        output_dir
    ):
        domain = EastAsiaMapTemplate(with_sub_area=False)
        panel = Panel(domain=domain)
        panel.plot(sample_temperature_field, style=temperature_style)
        
        domain.set_title(
            panel=panel,
            graph_name="2m Temperature (°C)",
            system_name="Test-Model",
            start_time=sample_start_time,
            forecast_time=sample_forecast_time,
        )
        domain.add_colorbar(panel=panel, style=temperature_style)
        
        output_path = output_dir / "east_asia_without_sub_area.png"
        panel.save(output_path, dpi=150)
        plt.close()

        # 验证只有一个 layer（无南海子图）
        assert len(panel.charts[0].layers) == 1
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"
    
    def test_with_sub_area(
        self,
        sample_temperature_field,
        temperature_style,
        output_dir
    ):
        domain = EastAsiaMapTemplate(with_sub_area=True)
        panel = Panel(domain=domain)
        panel.plot(sample_temperature_field, style=temperature_style)
        
        output_path = output_dir / "east_asia_with_sub_area.png"
        panel.save(output_path, dpi=150)
        plt.close()

        assert len(panel.charts[0].layers) == 2
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"


class TestEastAsiaMapTemplateEdgeCases:
    
    def test_empty_style_levels(self, sample_temperature_field, output_dir):
        """测试空 levels 的处理"""
        style = ContourStyle(
            colors="RdYlBu_r",
            levels=None,
            fill=True,
        )
        
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        
        panel.plot(sample_temperature_field, style=style)
        output_path = output_dir / "east_asia_empty_levels.png"
        panel.save(output_path, dpi=150)
        plt.close()

        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"

    
    def test_single_value_field(
        self, 
        east_asia_coords, 
        temperature_style,
        output_dir
    ):
        """测试单一值场的处理"""
        import xarray as xr
        
        lons, lats = east_asia_coords
        data = np.full((len(lats), len(lons)), 25.0)
        field = xr.DataArray(
            data,
            dims=['latitude', 'longitude'],
            coords={'latitude': lats, 'longitude': lons}
        )
        
        domain = EastAsiaMapTemplate()
        panel = Panel(domain=domain)
        panel.plot(field, style=temperature_style)
        
        output_path = output_dir / "east_asia_single_value_field.png"
        panel.save(output_path, dpi=150)
        plt.close()
        
        assert output_path.exists(), "image file should be created"
        assert output_path.stat().st_size > 0, "image file should not be empty"
