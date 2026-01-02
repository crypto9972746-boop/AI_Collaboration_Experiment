"""
Kryptos K4 リバイズド・タスク3：ウラニア24分割変換
BERLINCLOCK (64-74) 直後の文字群に対し、
26進法ではなく24進法（ウラニア世界時計の24時間分割）での換字を適用
"""

# K4暗号文（97文字）
K4_CIPHER = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

def char_to_num(char):
    """文字を数値に変換（A=0, B=1, ..., Z=25）"""
    return ord(char) - ord('A')

def num_to_char_26(num):
    """26進法での文字変換（0=A, 1=B, ..., 25=Z）"""
    return chr((num % 26) + ord('A'))

def num_to_char_24(num):
    """24進法での文字変換（0-23 → A-X、24,25は折り返し）"""
    return chr((num % 24) + ord('A'))

def apply_24_base_conversion():
    """24進法変換の適用"""
    print("=" * 70)
    print("リバイズド・タスク3：ウラニア24分割（24進法）変換")
    print("=" * 70)
    print()
    
    # BERLINCLOCK以降のセクション（Position 75-97）
    berlin_end = 74  # BERLINCLOCKの終了位置（1-indexed: 74 → 0-indexed: 73）
    section_start = 74  # 0-indexed
    section = K4_CIPHER[section_start:]
    
    print(f"=== 対象セクション: Position {section_start+1}-97 (BERLINCLOCK直後) ===")
    print(f"暗号文: {section}")
    print(f"文字数: {len(section)}")
    print()
    
    # 方法1: 26進法 → 24進法変換
    print("=== 方法1: 26進法 → 24進法直接変換 ===")
    print("26文字(A-Z)を24文字(A-X)にマッピング、Y,Zは折り返し")
    print("-" * 70)
    
    result1 = []
    for i, char in enumerate(section):
        num_26 = char_to_num(char)
        # 24進法に変換（Y=0, Z=1として折り返し）
        if num_26 < 24:
            char_24 = chr(num_26 + ord('A'))
        elif num_26 == 24:  # Y
            char_24 = 'A'
        else:  # Z
            char_24 = 'B'
        
        result1.append(char_24)
        
        if i < 10:
            print(f"Pos {section_start+i+1:2d}: {char} ({num_26:2d}) → {char_24}")
    
    print("...")
    print("-" * 70)
    print(f"復号結果1: {''.join(result1)}")
    print()
    
    # 方法2: 24時間制時刻として解釈
    print("=== 方法2: 24時間制時刻エンコーディング ===")
    print("2文字ペアで時刻を表現（例: AB → 01時, WX → 23時）")
    print("-" * 70)
    
    result2_times = []
    for i in range(0, len(section) - 1, 2):
        if i + 1 < len(section):
            char1 = section[i]
            char2 = section[i+1]
            num1 = char_to_num(char1)
            num2 = char_to_num(char2)
            
            # 24時間制の時刻に変換
            hour = (num1 % 24)
            minute = ((num2 * 60) // 26)  # 26分割を60分に変換
            
            result2_times.append(f"{hour:02d}:{minute:02d}")
            
            if len(result2_times) <= 5:
                print(f"Pos {section_start+i+1:2d}-{section_start+i+2:2d}: {char1}{char2} ({num1},{num2}) → {hour:02d}:{minute:02d}")
    
    print("...")
    print("-" * 70)
    print(f"時刻列: {', '.join(result2_times)}")
    print()
    
    # 方法3: 24で割った余りをシフト量として使用
    print("=== 方法3: 24進法シフト暗号 ===")
    print("文字の数値を24で割った余りでシフト")
    print("-" * 70)
    
    result3 = []
    for i, char in enumerate(section):
        original_num = char_to_num(char)
        shift = original_num % 24
        # 次の文字に適用
        if i + 1 < len(section):
            next_char = section[i + 1]
            next_num = char_to_num(next_char)
            shifted_num = (next_num - shift) % 26
            shifted_char = num_to_char_26(shifted_num)
            result3.append(shifted_char)
            
            if i < 5:
                print(f"Pos {section_start+i+2:2d}: {next_char} ({next_num:2d}) - {shift:2d} = {shifted_char} ({shifted_num:2d})")
    
    print("...")
    print("-" * 70)
    print(f"復号結果3: {''.join(result3)}")
    print()
    
    # 方法4: ウラニア時計の24都市時差を適用
    print("=== 方法4: ウラニア24都市時差パターン適用 ===")
    print("-" * 70)
    
    # 24都市の時差パターン（簡略版: -12から+12への推移）
    timezone_pattern = []
    for i in range(24):
        tz = -12 + i  # -12, -11, ..., +11
        timezone_pattern.append(tz)
    
    result4 = []
    for i, char in enumerate(section):
        original_num = char_to_num(char)
        tz = timezone_pattern[i % 24]
        shifted_num = original_num - tz
        shifted_char = num_to_char_26(shifted_num)
        result4.append(shifted_char)
        
        if i < 10:
            print(f"Pos {section_start+i+1:2d}: {char} ({original_num:2d}) - {tz:+3d} = {shifted_char} ({shifted_num % 26:2d})")
    
    print("...")
    print("-" * 70)
    print(f"復号結果4: {''.join(result4)}")
    print()
    
    # 全K4に24進法を適用
    print("=== K4全体への24進法適用 ===")
    print("-" * 70)
    
    full_result = []
    for char in K4_CIPHER:
        num = char_to_num(char)
        char_24 = num_to_char_24(num)
        full_result.append(char_24)
    
    print(f"26進法原文: {K4_CIPHER[:40]}...")
    print(f"24進法変換: {''.join(full_result[:40])}...")
    print()
    
    # 既知ヒント部分での検証
    print("=== 既知ヒント部分での24進法変換結果 ===")
    print("-" * 70)
    
    known_hints = [
        ('EASTNORTHEAST', 21, 13),
        ('BERLIN', 63, 6),
        ('CLOCK', 69, 5)
    ]
    
    for plaintext, start_pos, length in known_hints:
        original = K4_CIPHER[start_pos:start_pos+length]
        converted = ''.join(full_result[start_pos:start_pos+length])
        
        print(f"\n{plaintext} (Position {start_pos+1}-{start_pos+length}):")
        print(f"  26進法: {original}")
        print(f"  24進法: {converted}")
        print(f"  目標  : {plaintext}")
    
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
        '方法1（24進法直接）': ''.join(result1),
        '方法3（24進シフト）': ''.join(result3),
        '方法4（時差パターン）': ''.join(result4),
        'K4全体24進法': ''.join(full_result)
    }
    
    for method, text in all_results.items():
        if len(text) > 10:
            ioc = calculate_ioc(text)
            status = "★ 自然文の可能性" if ioc > 0.060 else "  ランダム的"
            print(f"{method:25s}: IOC = {ioc:.4f} {status}")
    
    print()
    
    # 24進法での座標パターン探索
    print("=== 24進法での座標数値探索 ===")
    print("-" * 70)
    
    # 24進法で52や13を探す
    print("24進法文字列での数値パターン:")
    
    full_24_nums = [char_to_num(c) % 24 for c in full_result]
    
    # 3-5文字のウィンドウで52や13を探す
    targets = {'緯度52': 52, '経度13': 13, '緯度2.5': 2.5, '経度1.3': 1.3}
    
    for name, target in targets.items():
        for size in [3, 4, 5]:
            for i in range(len(full_24_nums) - size + 1):
                segment = full_24_nums[i:i+size]
                avg = sum(segment) / len(segment)
                
                if abs(avg - target) < 0.3:
                    seg_chars = ''.join(full_result[i:i+size])
                    print(f"  {name} 候補: Pos {i+1}-{i+size} '{seg_chars}' 平均={avg:.2f}")

if __name__ == "__main__":
    apply_24_base_conversion()
