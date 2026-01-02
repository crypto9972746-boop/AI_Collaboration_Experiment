"""
Kryptos K4 最終幾何学検証タスク
物理的起点からの測量データ抽出と検証
"""

import math

# K4暗号文（97文字）
K4_CIPHER = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

# 座標データ
POINT_A = {
    'name': 'Alexandrinenstraße 123 (Berlin Wall remnant)',
    'lat': 52 + 30/60 + 18.8/3600,  # 52°30'18.8"N
    'lon': 13 + 23/60 + 42.4/3600   # 13°23'42.4"E
}

POINT_B = {
    'name': 'Urania World Clock',
    'lat': 52 + 31/60 + 15.5/3600,  # 52°31'15.5"N
    'lon': 13 + 24/60 + 46.3/3600   # 13°24'46.3"E
}

CIA_LANGLEY = {
    'name': 'CIA Headquarters',
    'lat': 38 + 57/60 + 6/3600,     # 38°57'06"N
    'lon': -(77 + 8/60 + 48/3600)   # 77°08'48"W
}

# 地球半径（メートル）
EARTH_RADIUS = 6371000

def char_to_num(char):
    """文字を数値に変換（A=0, B=1, ..., Z=25）"""
    return ord(char) - ord('A')

def haversine_distance(lat1, lon1, lat2, lon2):
    """2点間のHaversine距離（メートル）"""
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return EARTH_RADIUS * c

def calculate_bearing(lat1, lon1, lat2, lon2):
    """2点間の方位角（度数法、真北を0度）"""
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)
    
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
    
    bearing_rad = math.atan2(x, y)
    bearing_deg = math.degrees(bearing_rad)
    
    # 0-360度に正規化
    return (bearing_deg + 360) % 360

def bearing_to_direction(bearing):
    """方位角を16方位に変換"""
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = int((bearing + 11.25) / 22.5) % 16
    return directions[index]

def task_a_bearing_verification():
    """タスクA: 方位角とヒントの一致検証"""
    print("=" * 70)
    print("タスクA: 方位角（アジマス）とヒントの一致検証")
    print("=" * 70)
    print()
    
    # Point A → Point B の方位角
    bearing_ab = calculate_bearing(
        POINT_A['lat'], POINT_A['lon'],
        POINT_B['lat'], POINT_B['lon']
    )
    
    direction = bearing_to_direction(bearing_ab)
    
    print(f"Point A: {POINT_A['name']}")
    print(f"  座標: {POINT_A['lat']:.6f}°N, {POINT_A['lon']:.6f}°E")
    print()
    print(f"Point B: {POINT_B['name']}")
    print(f"  座標: {POINT_B['lat']:.6f}°N, {POINT_B['lon']:.6f}°E")
    print()
    print(f"Point A → Point B:")
    print(f"  真方位角: {bearing_ab:.2f}°")
    print(f"  16方位: {direction}")
    print()
    
    # EASTNORTHEAST = 67.5度と比較
    ene_bearing = 67.5
    print(f"既知ヒント 'EASTNORTHEAST' = {ene_bearing}°")
    print(f"実測方位角との差: {abs(bearing_ab - ene_bearing):.2f}°")
    print()
    
    # 磁気偏角補正（1990年ベルリン: 約1°E）
    magnetic_declination = 1.0
    magnetic_bearing = bearing_ab - magnetic_declination
    
    print(f"磁気偏角補正後（1990年ベルリン +1°E）:")
    print(f"  磁気方位角: {magnetic_bearing:.2f}°")
    print(f"  ENEとの差: {abs(magnetic_bearing - ene_bearing):.2f}°")
    print()
    
    # K4内での方位角数値探索
    print("K4内での方位角関連数値探索:")
    print("-" * 70)
    
    target_values = [
        bearing_ab,
        magnetic_bearing,
        ene_bearing,
        bearing_ab / 10,  # スケール調整
        bearing_ab % 26   # 26進法剰余
    ]
    
    # Unknown-2 (Position 39-63) を重点的に探索
    unknown2_start = 38  # 0-indexed
    unknown2_end = 63
    
    print(f"\nUnknown-2 (Position 39-63) 詳細スキャン:")
    for size in [3, 4, 5]:
        for i in range(unknown2_start, unknown2_end - size + 1):
            segment = K4_CIPHER[i:i+size]
            nums = [char_to_num(c) for c in segment]
            avg = sum(nums) / len(nums)
            total = sum(nums)
            
            for target in target_values:
                if abs(avg - target) < 1.0 or abs(total - target) < 2.0:
                    print(f"  Pos {i+1}-{i+size}: '{segment}' 平均={avg:.2f}, 合計={total} (目標: {target:.2f})")

def task_b_distance_scaling():
    """タスクB: 物理距離の文字変換"""
    print("\n" + "=" * 70)
    print("タスクB: 物理距離の文字変換")
    print("=" * 70)
    print()
    
    # Point A → Point B の距離
    distance_ab = haversine_distance(
        POINT_A['lat'], POINT_A['lon'],
        POINT_B['lat'], POINT_B['lon']
    )
    
    print(f"Point A → Point B の直線距離:")
    print(f"  {distance_ab:.2f} メートル")
    print(f"  {distance_ab/1000:.3f} キロメートル")
    print()
    
    # CIA → Berlin の距離
    distance_cia_berlin = haversine_distance(
        CIA_LANGLEY['lat'], CIA_LANGLEY['lon'],
        POINT_B['lat'], POINT_B['lon']
    )
    
    print(f"CIA本部 → Berlin (Point B) の直線距離:")
    print(f"  {distance_cia_berlin:.2f} メートル")
    print(f"  {distance_cia_berlin/1000:.3f} キロメートル")
    print()
    
    # K4の文字スケール
    k4_length = len(K4_CIPHER)
    
    print(f"K4文字スケール計算:")
    print(f"  K4全長: {k4_length} 文字")
    print()
    
    # スケール1: CIA → Berlin を97文字で表現
    scale1_meter_per_char = distance_cia_berlin / k4_length
    print(f"スケール1（全体距離）:")
    print(f"  1文字 = {scale1_meter_per_char:.2f} メートル")
    print(f"  1文字 = {scale1_meter_per_char/1000:.3f} キロメートル")
    print()
    
    # BERLINCLOCKの位置（64-74）での期待距離
    berlin_start = 63  # 0-indexed
    berlin_end = 74
    berlin_position_avg = (berlin_start + berlin_end) / 2
    
    expected_distance_at_berlin = berlin_position_avg * scale1_meter_per_char
    
    print(f"BERLINCLOCK位置（Position 64-74）での期待距離:")
    print(f"  中央位置: Position {berlin_position_avg:.1f}")
    print(f"  期待累積距離: {expected_distance_at_berlin/1000:.2f} km")
    print(f"  全体距離に対する割合: {berlin_position_avg/k4_length*100:.1f}%")
    print()
    
    # Point A → Point B の距離を文字数で表現
    chars_for_ab = distance_ab / scale1_meter_per_char
    
    print(f"Point A → Point B の距離を文字数で表現:")
    print(f"  約 {chars_for_ab:.2f} 文字分")
    print()
    
    # スケール2: Point A → Point B を特定文字数で表現
    # 仮説: Position 52-97の45文字がベルリン内の移動を表す
    berlin_segment_length = 97 - 52
    scale2_meter_per_char = distance_ab / berlin_segment_length
    
    print(f"スケール2（ベルリン内移動）:")
    print(f"  Position 52-97の{berlin_segment_length}文字")
    print(f"  1文字 = {scale2_meter_per_char:.2f} メートル")
    print()
    
    # BERLINCLOCK位置での検証
    berlin_clock_relative_pos = (berlin_start - 52) + (berlin_end - 52) / 2
    expected_distance_berlin_clock = berlin_clock_relative_pos * scale2_meter_per_char
    
    print(f"BERLINCLOCK位置での検証（ベルリン内スケール）:")
    print(f"  Position 52からの相対位置: {berlin_clock_relative_pos:.1f}")
    print(f"  期待距離: {expected_distance_berlin_clock:.2f} メートル")
    print(f"  実際の総距離: {distance_ab:.2f} メートル")
    print(f"  到達割合: {expected_distance_berlin_clock/distance_ab*100:.1f}%")

def task_c_reverse_vector():
    """タスクC: 冒頭セグメント (01-21) の「逆ベクトル」解析"""
    print("\n" + "=" * 70)
    print("タスクC: 冒頭セグメント (01-21) の「逆ベクトル」解析")
    print("=" * 70)
    print()
    
    # Point A → CIA の方位と距離
    bearing_a_to_cia = calculate_bearing(
        POINT_A['lat'], POINT_A['lon'],
        CIA_LANGLEY['lat'], CIA_LANGLEY['lon']
    )
    
    distance_a_to_cia = haversine_distance(
        POINT_A['lat'], POINT_A['lon'],
        CIA_LANGLEY['lat'], CIA_LANGLEY['lon']
    )
    
    direction = bearing_to_direction(bearing_a_to_cia)
    
    print(f"Point A (ベルリン壁跡) → CIA本部:")
    print(f"  方位角: {bearing_a_to_cia:.2f}°")
    print(f"  16方位: {direction}")
    print(f"  距離: {distance_a_to_cia/1000:.2f} km")
    print()
    
    # 座標差分
    delta_lat = CIA_LANGLEY['lat'] - POINT_A['lat']
    delta_lon = CIA_LANGLEY['lon'] - POINT_A['lon']
    
    print(f"座標差分:")
    print(f"  緯度差: {delta_lat:.6f}° ({abs(delta_lat):.6f}°)")
    print(f"  経度差: {delta_lon:.6f}° ({abs(delta_lon):.6f}°)")
    print()
    
    # Unknown-1 (Position 01-21) の数値解析
    unknown1 = K4_CIPHER[0:21]
    print(f"Unknown-1 (Position 01-21): {unknown1}")
    print()
    
    # 各種数値表現
    unknown1_nums = [char_to_num(c) for c in unknown1]
    
    print(f"数値変換: {unknown1_nums}")
    print(f"合計: {sum(unknown1_nums)}")
    print(f"平均: {sum(unknown1_nums)/len(unknown1_nums):.2f}")
    print()
    
    # 方位角・距離との照合
    print("逆ベクトルデータとの照合:")
    print("-" * 70)
    
    target_values = {
        '方位角': bearing_a_to_cia,
        '方位角/10': bearing_a_to_cia / 10,
        '緯度差（絶対値）': abs(delta_lat),
        '緯度差×10': abs(delta_lat) * 10,
        '経度差（絶対値）': abs(delta_lon),
        '経度差×10': abs(delta_lon) * 10,
        '距離/100km': distance_a_to_cia / 100000
    }
    
    for size in [3, 4, 5, 6]:
        for i in range(len(unknown1) - size + 1):
            segment = unknown1[i:i+size]
            nums = [char_to_num(c) for c in segment]
            avg = sum(nums) / len(nums)
            total = sum(nums)
            
            for name, target in target_values.items():
                if abs(avg - target) < 1.0 or abs(total - target) < 2.0:
                    print(f"  Pos {i+1}-{i+size}: '{segment}' 平均={avg:.2f}, 合計={total} → {name}={target:.2f}")

def task_d_timestamp_verification():
    """タスクD: 22:13（Position 75-76）の物理的裏付け"""
    print("\n" + "=" * 70)
    print("タスクD: 22:13（Position 75-76）の物理的裏付け")
    print("=" * 70)
    print()
    
    # Position 75-76の文字
    pos_75_76 = K4_CIPHER[74:76]
    num1 = char_to_num(pos_75_76[0])
    num2 = char_to_num(pos_75_76[1])
    
    print(f"Position 75-76: '{pos_75_76}'")
    print(f"  W = {num1} (22)")
    print(f"  G = {num2} (6)")
    print()
    
    # 時刻解釈
    hour_24 = num1 % 24
    minute_from_26 = (num2 * 60) // 26
    
    print(f"24時間制時刻解釈:")
    print(f"  時: {hour_24} (Wの値22 % 24)")
    print(f"  分: {minute_from_26} (Gの値6を60分にスケール)")
    print(f"  時刻: {hour_24}:{minute_from_26:02d}")
    print()
    
    # 歴史的事件との照合
    print("1989年11月9日（ベルリンの壁崩壊）の主要な時刻:")
    print("-" * 70)
    print("  18:57 - ギュンター・シャボウスキーの記者会見")
    print("  23:00頃 - 最初の検問所が開放")
    print("  22:00-23:00 - 市民が壁に集まり始める")
    print()
    
    print("22:13との関連:")
    print("  壁崩壊の混乱期の時刻として妥当")
    print("  または1990年の特定の記念時刻？")
    print()
    
    # Position 77-97の追加分析
    segment_77_97 = K4_CIPHER[76:97]
    print(f"Position 77-97 (22:13以降): {segment_77_97}")
    print(f"文字数: {len(segment_77_97)}")
    print()
    
    # 2文字ペアで時刻列を抽出
    print("連続時刻列の抽出:")
    print("-" * 70)
    
    for i in range(74, 97, 2):
        if i + 1 < 97:
            pair = K4_CIPHER[i:i+2]
            n1 = char_to_num(pair[0])
            n2 = char_to_num(pair[1])
            h = n1 % 24
            m = (n2 * 60) // 26
            
            print(f"  Pos {i+1}-{i+2}: '{pair}' → {h}:{m:02d}")

if __name__ == "__main__":
    print("Kryptos K4 最終幾何学検証")
    print("=" * 70)
    print()
    
    task_a_bearing_verification()
    task_b_distance_scaling()
    task_c_reverse_vector()
    task_d_timestamp_verification()
    
    print("\n" + "=" * 70)
    print("すべてのタスク完了")
    print("=" * 70)
