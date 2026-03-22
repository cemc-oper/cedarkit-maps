"""
集成测试专用 fixtures
提供模拟气象数据和测试输出目录
"""
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import pytest
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，避免弹出窗口
import matplotlib.colors as mcolors

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.colormap import get_ncl_colormap, generate_colormap_using_ncl_colors


@pytest.fixture(scope="module")
def output_dir() -> Path:
    """测试图片输出目录"""
    output_path = Path(__file__).parent.parent / "output"
    output_path.mkdir(exist_ok=True)
    return output_path


@pytest.fixture
def east_asia_coords():
    """东亚区域坐标网格"""
    lons = np.linspace(70, 140, 141)  # 0.5度分辨率
    lats = np.linspace(15, 55, 81)
    return lons, lats


@pytest.fixture
def sample_temperature_field(east_asia_coords):
    """
    模拟 2m 温度场数据
    使用正弦函数模拟南北温度梯度 + 随机扰动
    """
    lons, lats = east_asia_coords
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # 从坐标派生参数
    lat_min, lat_max = lats.min(), lats.max()
    lon_min = lons.min()
    
    # 基础温度场：南暖北冷
    base_temp = 30 - 0.8 * (lat_grid - lat_min)
    # 添加经向变化
    lon_effect = 5 * np.sin(np.radians(lon_grid - lon_min) * 2)
    # 添加随机扰动
    noise = np.random.randn(*base_temp.shape) * 2
    
    temperature = base_temp + lon_effect + noise
    
    return xr.DataArray(
        temperature,
        dims=['latitude', 'longitude'],
        coords={'latitude': lats, 'longitude': lons},
        attrs={'units': 'degC', 'long_name': '2m Temperature'}
    )


@pytest.fixture
def sample_pressure_field(east_asia_coords):
    """
    模拟海平面气压场数据
    模拟一个低压中心
    """
    lons, lats = east_asia_coords
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # 从坐标派生低压中心位置（区域中心偏西）
    center_lon = (lons.min() + lons.max()) / 2
    center_lat = (lats.min() + lats.max()) / 2
    
    # 基础气压场
    base_pressure = 1013.25
    distance = np.sqrt((lon_grid - center_lon)**2 + (lat_grid - center_lat)**2)
    pressure_anomaly = -15 * np.exp(-distance**2 / 200)
    
    pressure = base_pressure + pressure_anomaly + np.random.randn(*lon_grid.shape) * 0.5
    
    return xr.DataArray(
        pressure,
        dims=['latitude', 'longitude'],
        coords={'latitude': lats, 'longitude': lons},
        attrs={'units': 'hPa', 'long_name': 'Mean Sea Level Pressure'}
    )


@pytest.fixture
def sample_wind_fields(east_asia_coords):
    """
    模拟风场数据 (u, v 分量)
    基于气压场模拟地转风
    """
    lons, lats = east_asia_coords
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # 从坐标派生参数
    lat_min = lats.min()
    center_lon = (lons.min() + lons.max()) / 2
    center_lat = (lats.min() + lats.max()) / 2
    
    # 模拟西风带 + 低压环流
    dx = lon_grid - center_lon
    dy = lat_grid - center_lat
    distance = np.sqrt(dx**2 + dy**2) + 0.1
    
    # 基础西风（随纬度增加）
    u_base = 5 + 0.2 * (lat_grid - lat_min)
    v_base = np.zeros_like(u_base)
    
    # 低压环流（逆时针）
    wind_speed = 10 * np.exp(-distance**2 / 300)
    u_cyclone = wind_speed * dy / distance
    v_cyclone = -wind_speed * dx / distance
    
    u = u_base + u_cyclone + np.random.randn(*lon_grid.shape) * 1
    v = v_base + v_cyclone + np.random.randn(*lon_grid.shape) * 1
    
    u_field = xr.DataArray(
        u,
        dims=['latitude', 'longitude'],
        coords={'latitude': lats, 'longitude': lons},
        attrs={'units': 'm/s', 'long_name': 'U component of wind'}
    )
    v_field = xr.DataArray(
        v,
        dims=['latitude', 'longitude'],
        coords={'latitude': lats, 'longitude': lons},
        attrs={'units': 'm/s', 'long_name': 'V component of wind'}
    )
    
    return u_field, v_field


@pytest.fixture
def sample_precipitation_field(east_asia_coords):
    """
    模拟降水场数据
    模拟几个降水中心
    """
    lons, lats = east_asia_coords
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # 从坐标派生降水中心位置
    lon_min, lon_max = lons.min(), lons.max()
    lat_min, lat_max = lats.min(), lats.max()
    lon_range = lon_max - lon_min
    lat_range = lat_max - lat_min
    
    # 在区域内分布几个降水中心
    centers = [
        (lon_min + 0.6 * lon_range, lat_min + 0.4 * lat_range),  # 中部偏东偏南
        (lon_min + 0.7 * lon_range, lat_min + 0.25 * lat_range), # 东南部
        (lon_min + 0.5 * lon_range, lat_min + 0.5 * lat_range),  # 中部
    ]
    
    precipitation = np.zeros_like(lon_grid)
    for center_lon, center_lat in centers:
        distance = np.sqrt((lon_grid - center_lon)**2 + (lat_grid - center_lat)**2)
        precipitation += 50 * np.exp(-distance**2 / 50)
    
    # 确保非负
    precipitation = np.maximum(precipitation + np.random.randn(*lon_grid.shape) * 2, 0)
    
    return xr.DataArray(
        precipitation,
        dims=['latitude', 'longitude'],
        coords={'latitude': lats, 'longitude': lons},
        attrs={'units': 'mm', 'long_name': '24h Precipitation'}
    )


@pytest.fixture
def sample_start_time():
    """模拟起报时间"""
    return pd.Timestamp("2024-11-09 00:00:00")


@pytest.fixture
def sample_forecast_time():
    """模拟预报时效"""
    return pd.Timedelta("24h")


@pytest.fixture
def temperature_style():
    """温度场填充图样式 - 使用 NCL colormap"""
    color_map = get_ncl_colormap("BlAqGrYeOrReVi200")
    t_2m_level = [-12, -8, -4, 0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44]
    color_index = np.array([2, 18, 34, 50, 66, 82, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]) - 2
    t_2m_color_map = mcolors.ListedColormap(color_map(color_index))
    return ContourStyle(
        colors=t_2m_color_map,
        levels=t_2m_level,
        fill=True,
    )


@pytest.fixture
def precipitation_style():
    """降水场填充图样式 - 使用 NCL 命名颜色"""
    rain_contour_lev = np.array([0.1, 10, 25, 50, 100, 200])
    rain_color_map = generate_colormap_using_ncl_colors(
        [
            "transparent",
            "White",
            "DarkOliveGreen3",
            "forestgreen",
            "deepSkyBlue",
            "Blue",
            "Magenta",
            "deeppink4"
        ],
        name="rain"
    )
    return ContourStyle(
        colors=rain_color_map,
        levels=rain_contour_lev,
        fill=True,
    )
