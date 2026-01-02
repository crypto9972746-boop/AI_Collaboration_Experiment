"""
Kryptos K4 リバイズド・タスク2：「J」をマーカーとした座標オフセット適用
Position 52の「J」を原点（0）とし、そこからの相対位置にある文字を
「偏角」として計算し、既知ヒント以外の文字を復号
"""

# K4暗号文（97文字）
K4_CIPHER = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

def char_to_num(char):
    """文字を数値に変換（A=0, B=1, ..., Z=25）"""
    return ord(char) - ord('A')

def num_to_char(num):
    """数値を文字に変換（0=A, 1=B, ..., 25=Z）"""
    return chr((num % 26) + ord('A'))

def apply_j_offset():
    """Position 52の「J」を原点としたオフセット適用"""
    print("=" * 70)
    print("リバイズド・タスク2：Position 52 'J' 原点オフセット適用")
    print("=" * 70)
    print()
    
    j_position = 51  # 0-indexed
    j_value = char_to_num(K4_CIPHER[j_position])
    
    print(f"原点設定: Position 52 = '{K4_CIPHER[j_position]}' (数値: {j_value})")
    print()
    
    # 方法1: Position 52からの距離をオフセットとして使用
    print("=== 方法1: Position 52からの距離をオフセット ===")
    print("-" * 70)
    
    result1 = []
    for i, char in enumerate(K4_CIPHER):
        original_num = char_to_num(char)
        distance = i - j_position  # Position 52からの距離
        shifted_num = original_num - distance  # 距離を引く
        shifted_char = num_to_char(shifted_num)
        
        result1.append(shifted_char)
        
        if i < 10 or (j_position - 5 <= i <= j_position + 5) or i >= len(K4_CIPHER) - 5:
            marker = " <-- Position 52" if i == j_position else ""
            print(f"Pos {i+1:2d}: {char} ({original_num:2d}) - {distance:+4d} = {shifted_char} ({shifted_num % 26:2d}){marker}")
        elif i == 10 or i == j_position + 6:
            print("...")
    
    print("-" * 70)
    print(f"復号結果1: {''.join(result1)}")
    print()
    
    # 方法2: 「J」の値（9）を全体に適用
    print("=== 方法2: J値（9）を全体のオフセットとして適用 ===")
    print("-" * 70)
    
    result2_plus = ''.join([num_to_char(char_to_num(c) + j_value) for c in K4_CIPHER])
    result2_minus = ''.join([num_to_char(char_to_num(c) - j_value) for c in K4_CIPHER])
    
    print(f"J値加算: {result2_plus[:50]}...")
    print(f"J値減算: {result2_minus[:50]}...")
    print()
    
    # 方法3: Position 52を境に前後で異なるシフト
    print("=== 方法3: Position 52を境界とした2区間処理 ===")
    print("-" * 70)
    
    result3 = []
    for i, char in enumerate(K4_CIPHER):
        original_num = char_to_num(char)
        
        if i < j_position:
            # Position 52より前: 正のシフト
            shift = j_value
        elif i == j_position:
            # Position 52: シフトなし
            shift = 0
        else:
            # Position 52より後: 負のシフト
            shift = -j_value
        
        shifted_num = original_num + shift
        shifted_char = num_to_char(shifted_num)
        result3.append(shifted_char)
        
        if i == 0 or i == j_position or i == j_position + 1:
            print(f"Pos {i+1:2d}: {char} ({original_num:2d}) + {shift:+3d} = {shifted_char}")
    
    print("-" * 70)
    print(f"復号結果3: {''.join(result3)}")
    print()
    
    # 方法4: 相対位置の二乗をオフセットに使用（非線形）
    print("=== 方法4: 相対位置の二乗オフセット（非線形変換） ===")
    print("-" * 70)
    
    result4 = []
    for i, char in enumerate(K4_CIPHER):
        original_num = char_to_num(char)
        distance = i - j_position
        offset = (distance * distance) % 26  # 二乗を26で割った余り
        
        if distance < 0:
            offset = -offset
        
        shifted_num = original_num + offset
        shifted_char = num_to_char(shifted_num)
        result4.append(shifted_char)
        
        if abs(distance) <= 3:
            print(f"Pos {i+1:2d}: {char} ({original_num:2d}) + {offset:+4d} (dist²={distance}²) = {shifted_char}")
    
    print("-" * 70)
    print(f"復号結果4: {''.join(result4)[:50]}...")
    print()
    
    # 既知ヒント部分の検証
    print("=== 既知ヒント部分での検証 ===")
    print("-" * 70)
    
    known_hints = [
        ('EASTNORTHEAST', 21, 13),
        ('BERLIN', 63, 6),
        ('CLOCK', 69, 5)
    ]
    
    for plaintext, start_pos, length in known_hints:
        print(f"\n平文: {plaintext} (Position {start_pos+1}-{start_pos+length})")
        
        # 各方法での復号結果
        segment1 = ''.join(result1[start_pos:start_pos+length])
        segment2_minus = result2_minus[start_pos:start_pos+length]
        segment3 = ''.join(result3[start_pos:start_pos+length])
        
        print(f"  原文     : {K4_CIPHER[start_pos:start_pos+length]}")
        print(f"  方法1結果: {segment1}")
        print(f"  方法2結果: {segment2_minus}")
        print(f"  方法3結果: {segment3}")
        print(f"  目標     : {plaintext}")
        
        # 一致度チェック
        match1 = sum(1 for a, b in zip(segment1, plaintext) if a == b)
        match2 = sum(1 for a, b in zip(segment2_minus, plaintext) if a == b)
        match3 = sum(1 for a, b in zip(segment3, plaintext) if a == b)
        
        print(f"  一致度   : 方法1={match1}/{length}, 方法2={match2}/{length}, 方法3={match3}/{length}")
    
    print()
    
    # IOC分析
    print("=== IOC分析 ===")
    print("-" * 70)
    
    def calculate_ioc(text):
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        n = len(text)
        if n <= 1:
            return 0
        ioc = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
        return ioc
    
    all_results = {
        '方法1（距離オフセット）': ''.join(result1),
        '方法2（J値減算）': result2_minus,
        '方法3（2区間処理）': ''.join(result3),
        '方法4（非線形）': ''.join(result4)
    }
    
    for method, text in all_results.items():
        ioc = calculate_ioc(text)
        status = "★ 自然文の可能性" if ioc > 0.060 else "  ランダム的"
        print(f"{method:25s}: IOC = {ioc:.4f} {status}")
    
    print()
    
    # 英単語パターン検索
    print("=== 英単語パターン検索 ===")
    print("-" * 70)
    
    keywords = ['COORDINATE', 'LATITUDE', 'LONGITUDE', 'DEGREE', 'MINUTE',
                'NORTH', 'EAST', 'WEST', 'SOUTH', 'TIME', 'HOUR', 'CLOCK',
                'DISTANCE', 'DIRECTION', 'ANGLE', 'POSITION']
    
    found = False
    for method, text in all_results.items():
        for word in keywords:
            if word in text:
                pos = text.index(word)
                print(f"✓ {method}: '{word}' を Position {pos+1} で発見")
                found = True
    
    if not found:
        print("既知の英単語パターンは見つかりませんでした")

if __name__ == "__main__":
    apply_j_offset()
