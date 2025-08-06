"""
JSON 데이터 정리 유틸리티
"""

import numpy as np
from typing import Any, Dict, List, Union

def clean_json_data(data: Any) -> Any:
    """
    JSON 직렬화 전에 NaN, Infinity 값을 정리하는 함수
    
    Args:
        data: 정리할 데이터 (dict, list, float, int, str 등)
        
    Returns:
        정리된 데이터 (NaN, Infinity 값은 None으로 변환)
    """
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            cleaned[key] = clean_json_data(value)
        return cleaned
    elif isinstance(data, list):
        return [clean_json_data(item) for item in data]
    elif isinstance(data, (np.floating, float)):
        if np.isnan(data) or np.isinf(data):
            return None
        return float(data)
    elif isinstance(data, (np.integer, int)):
        return int(data)
    elif isinstance(data, str):
        return data
    elif data is None:
        return None
    else:
        return str(data)  # 기타 타입은 문자열로 변환
