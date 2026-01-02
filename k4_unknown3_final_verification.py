"""
K4 Unknown-3 (Position 77-97) 最終検証
1989年11月9日22:13における天文データと24都市時刻の照合
"""

import math
from datetime import datetime, timezone, timedelta

# K4暗号文
K4_CIPHER = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

# ウラニア世界時計の24都市（1990年当時）
URANIA_CITIES = [
    ("Berlin", 1, "Europe/Berlin"),
    ("London", 0, "Europe/London"),
    ("Paris", 1, "Europe/Paris"),
    ("Rome", 1, "Europe/Rome"),
    ("Moscow", 3, "Europe/Moscow"),
    ("Cairo", 2, "Africa/Cairo"),
    ("Johannesburg", 2, "Africa/Johannesburg"),
    ("Tokyo", 9, "Asia/Tokyo"),
    ("Hong Kong", 8, "Asia/Hong_Kong"),
    ("Singapore", 8, "Asia/Singapore"),
    ("Bangkok", 7, "Asia/Bangkok"),
    ("Sydney", 11, "Australia/Sydney"),
    ("Auckland", 13, "Pacific/Auckland"),
    ("Honolulu", -10, "Pacific/Honolulu"),
    ("Anchorage", -9, "America/Anchorage"),
    ("Los Angeles", -8, "America/Los_Angeles"),
    ("Denver", -7, "America/Denver"),
    ("Chicago", -6, "America/Chicago"),
    ("New York", -5, "America/New_York"),
    ("Buenos Aires", -3, "America/Argentina/Buenos_Aires"),
    ("Rio de Janeiro", -3, "America/Sao_Paulo"),
    ("Mexico City", -6, "America/Mexico_City"),
    ("Caracas", -4, "America/Caracas"),
    ("Reykjavik", 0, "Atlantic/Reykjavik")
]

def char_to_num(char):
    """文字を数値に変換（A=0～Z=25）"""
    return ord(char) - ord('A')

def extract_time_from_pair(char1, char2):
    """2文字ペアから時刻を抽出"""
    n1 = char_to_num(char1)
    n2 = char_to_num(char2)
    
    hour = n1 % 24
    minute = (n2 * 60) // 26
    
    return hour, minute

def calculate_city_time(base_hour, base_minute, utc_offset):
    """ベルリン時刻から各都市の現地時刻を計算"""
    # ベルリンはUTC+1（冬時間、1989年11月）
    berlin_offset = 1
    
    # UTC時刻を計算
    utc_hour = (base_hour - berlin_offset) % 24
    utc_minute = base_minute
    
    # 各都市の現地時刻
    local_hour = (utc_hour + utc_offset) % 24
    
    return local_hour, utc_minute

def analyze_unknown3():
    """Unknown-3 (Position 77-97) の分析"""
    print("=" * 80)
    print("K4 Unknown-3 (Position 77-97) 最終検証")
    print("1989年11月9日 22:13（ベルリン時間）における世界時刻")
    print("=" * 80)
    print()
    
    # Position 75-76のベルリン時刻
    berlin_time = extract_time_from_pair(K4_CIPHER[74], K4_CIPHER[75])
    print(f"基準時刻（Position 75-76 'WG'）: {berlin_time[0]:02d}:{berlin_time[1]:02d}")
    print()
    
    # Position 77-97を2文字ペアで時刻抽出
    print("Position 77-97 の時刻列:")
    print("-" * 80)
    
    time_pairs = []
    for i in range(76, 96, 2):
        pair = K4_CIPHER[i:i+2]
        hour, minute = extract_time_from_pair(pair[0], pair[1])
        time_pairs.append((i+1, pair, hour, minute))
        print(f"Position {i+1:02d}-{i+2:02d}: '{pair}' → {hour:02d}:{minute:02d}")
    
    print()
    print("=" * 80)
    print("ウラニア世界時計24都市の1989年11月9日22:13の現地時刻")
    print("=" * 80)
    print()
    
    # 各都市の時刻を計算
    city_times = []
    for city, utc_offset, tz_name in URANIA_CITIES:
        local_hour, local_minute = calculate_city_time(22, 13, utc_offset)
        city_times.append((city, local_hour, local_minute, utc_offset))
    
    # 時刻順にソート
    city_times_sorted = sorted(city_times, key=lambda x: x[1] * 60 + x[2])
    
    print("都市名                    現地時刻    UTC差")
    print("-" * 80)
    for city, hour, minute, offset in city_times_sorted:
        print(f"{city:20s}  {hour:02d}:{minute:02d}      UTC{offset:+d}")
    
    print()
    print("=" * 80)
    print("K4時刻列とウラニア都市時刻の照合")
    print("=" * 80)
    print()
    
    # K4の時刻列をソート
    time_pairs_sorted = sorted(time_pairs, key=lambda x: x[2] * 60 + x[3])
    
    print("K4時刻（時刻順）:")
    print("-" * 80)
    for pos, pair, hour, minute in time_pairs_sorted:
        print(f"Position {pos:02d}: {hour:02d}:{minute:02d} ('{pair}')")
    
    print()
    print("一致検証:")
    print("-" * 80)
    
    matches = []
    for k4_pos, k4_pair, k4_hour, k4_min in time_pairs:
        for city, city_hour, city_min, utc_offset in city_times:
            if k4_hour == city_hour:
                time_diff = abs(k4_min - city_min)
                if time_diff < 30:  # 30分以内の誤差を許容
                    matches.append({
                        'k4_pos': k4_pos,
                        'k4_pair': k4_pair,
                        'k4_time': f"{k4_hour:02d}:{k4_min:02d}",
                        'city': city,
                        'city_time': f"{city_hour:02d}:{city_min:02d}",
                        'diff': time_diff
                    })
    
    if matches:
        print(f"一致件数: {len(matches)}")
        print()
        for match in matches:
            print(f"Position {match['k4_pos']:02d} '{match['k4_pair']}' = {match['k4_time']}")
            print(f"  → {match['city']}: {match['city_time']} (誤差{match['diff']}分)")
            print()
    else:
        print("完全一致なし")
        print()
        print("考察:")
        print("- K4の時刻列は24都市の現地時刻ではない可能性")
        print("- 天文データ（月・惑星の位置）の可能性")
        print("- 別の物理データの可能性")
    
    print()
    print("=" * 80)
    print("天文データ仮説の検証")
    print("=" * 80)
    print()
    
    # 1989年11月9日22:13の簡易天文データ
    print("1989年11月9日 22:13 (ベルリン時間) の天体位置:")
    print("-" * 80)
    print()
    print("月齢: 約11日（上弦の月過ぎ）")
    print("月の高度: 約30-40度（南西の空）")
    print("月の方位角: 約220-230度")
    print()
    print("主要惑星:")
    print("  金星: 夕方西の空（すでに沈んでいる）")
    print("  木星: 深夜に昇る")
    print("  火星: 明け方に昇る")
    print("  土星: 夕方西の空")
    print()
    print("恒星:")
    print("  オリオン座: 東の空に昇り始め")
    print("  北極星: 高度約52度（北緯52度に対応）")
    print()
    
    # K4時刻列の数値パターン分析
    print("=" * 80)
    print("K4時刻列の数値パターン分析")
    print("=" * 80)
    print()
    
    hours = [pair[2] for pair in time_pairs]
    minutes = [pair[3] for pair in time_pairs]
    
    print(f"時データ: {hours}")
    print(f"平均: {sum(hours)/len(hours):.2f}時")
    print(f"範囲: {min(hours)}時 - {max(hours)}時")
    print()
    print(f"分データ: {minutes}")
    print(f"平均: {sum(minutes)/len(minutes):.2f}分")
    print(f"範囲: {min(minutes)}分 - {max(minutes)}分")
    print()
    
    # 特定の角度との一致検証
    print("角度データとしての解釈:")
    print("-" * 80)
    
    for pos, pair, hour, minute in time_pairs:
        # 時刻を角度に変換（1時間=15度、1分=0.25度）
        angle_from_time = (hour * 15) + (minute * 0.25)
        
        # または単純な数値を角度として解釈
        n1 = char_to_num(pair[0])
        n2 = char_to_num(pair[1])
        angle_from_chars = (n1 * 360 / 26)
        
        print(f"Position {pos:02d} '{pair}': {hour:02d}:{minute:02d}")
        print(f"  時刻→角度: {angle_from_time:.2f}°")
        print(f"  文字→角度: {angle_from_chars:.2f}°")
        print()

if __name__ == "__main__":
    analyze_unknown3()
