"""
Kryptos K4 リバイズド・タスク1：数値セグメント・スキャン
3-5文字のスライディングウィンドウで目標数値（座標、年、日付など）を探索
"""

# K4暗号文（97文字）
K4_CIPHER = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"

def char_to_num(char):
    """文字を数値に変換（A=0, B=1, ..., Z=25）"""
    return ord(char) - ord('A')

def sliding_window_scan():
    """スライディングウィンドウで目標数値を探索"""
    print("=" * 70)
    print("リバイズド・タスク1：数値セグメント・スキャン")
    print("=" * 70)
    print()
    
    # 目標数値
    targets = {
        '緯度（北緯52.5°）': [52.5, 5.25, 2.5, 52, 25],
        '経度（東経13.4°）': [13.4, 1.34, 134, 13],
        '1990年': [1990, 199, 19.90, 90],
        '壁崩壊（11月9日）': [1109, 119, 11.9, 11, 9],
        '緯度分（30分）': [30, 3.0, 0.5],  # 52°30' = 52.5°
        '経度分（24分）': [24, 2.4, 0.4],  # 13°24' = 13.4°
    }
    
    # ウィンドウサイズ3-6で探索
    for window_size in range(3, 7):
        print(f"\n{'='*70}")
        print(f"ウィンドウサイズ: {window_size}文字")
        print(f"{'='*70}\n")
        
        matches_found = False
        
        for i in range(len(K4_CIPHER) - window_size + 1):
            segment = K4_CIPHER[i:i+window_size]
            nums = [char_to_num(c) for c in segment]
            
            # 各種計算
            total = sum(nums)
            average = total / len(nums)
            product = 1
            for n in nums:
                product *= n
            
            # 目標数値との照合（許容誤差0.5）
            tolerance = 0.5
            
            for category, target_values in targets.items():
                for target in target_values:
                    # 平均値チェック
                    if abs(average - target) < tolerance:
                        print(f"✓ Position {i+1:2d}-{i+window_size:2d}: '{segment}'")
                        print(f"  カテゴリ: {category}")
                        print(f"  平均値: {average:.3f} (目標: {target}, 差: {abs(average-target):.3f})")
                        print(f"  数値: {nums}")
                        print()
                        matches_found = True
                    
                    # 合計値チェック
                    if abs(total - target) < tolerance:
                        print(f"✓ Position {i+1:2d}-{i+window_size:2d}: '{segment}'")
                        print(f"  カテゴリ: {category}")
                        print(f"  合計値: {total} (目標: {target}, 差: {abs(total-target):.3f})")
                        print(f"  数値: {nums}")
                        print()
                        matches_found = True
                    
                    # 合計値を10で割った値チェック
                    if abs(total/10 - target) < tolerance:
                        print(f"✓ Position {i+1:2d}-{i+window_size:2d}: '{segment}'")
                        print(f"  カテゴリ: {category}")
                        print(f"  合計÷10: {total/10:.3f} (目標: {target}, 差: {abs(total/10-target):.3f})")
                        print(f"  数値: {nums}")
                        print()
                        matches_found = True
        
        if not matches_found:
            print(f"  (このウィンドウサイズでは目標数値に近いセグメント見つからず)")
    
    # Position 1-21の詳細スキャン（緯度候補）
    print("\n" + "="*70)
    print("Position 1-21の詳細スキャン（緯度52.5°候補）")
    print("="*70 + "\n")
    
    section_1_21 = K4_CIPHER[0:21]
    print(f"対象文字列: {section_1_21}")
    print()
    
    # 全ての連続部分文字列を探索
    best_matches = []
    
    for start in range(21):
        for end in range(start + 3, min(start + 7, 21)):
            segment = section_1_21[start:end]
            nums = [char_to_num(c) for c in segment]
            total = sum(nums)
            average = total / len(nums)
            
            # 緯度関連の数値をチェック
            for target, name in [(52.5, '緯度52.5'), (5.25, '緯度5.25'), (2.5, '緯度2.5'), 
                                 (52, '緯度52'), (30, '分30'), (0.5, '分0.5')]:
                if abs(average - target) < 0.5:
                    best_matches.append({
                        'pos': f"{start+1}-{end}",
                        'segment': segment,
                        'nums': nums,
                        'average': average,
                        'target': target,
                        'name': name,
                        'diff': abs(average - target)
                    })
    
    # 差の小さい順にソート
    best_matches.sort(key=lambda x: x['diff'])
    
    if best_matches:
        print("緯度候補（差が小さい順）:")
        print("-" * 70)
        for match in best_matches[:10]:  # 上位10件
            print(f"Position {match['pos']:6s}: '{match['segment']:8s}'")
            print(f"  → {match['name']:12s} 平均値: {match['average']:.3f} (差: {match['diff']:.3f})")
            print(f"     数値: {match['nums']}")
    else:
        print("緯度候補が見つかりませんでした")
    
    # Position 63-66（経度13.25の再確認）
    print("\n" + "="*70)
    print("Position 63-66の再確認（経度13.4°）")
    print("="*70 + "\n")
    
    segment_bnyp = K4_CIPHER[62:66]
    nums_bnyp = [char_to_num(c) for c in segment_bnyp]
    
    print(f"文字列: {segment_bnyp}")
    print(f"数値: {nums_bnyp}")
    print(f"合計: {sum(nums_bnyp)}")
    print(f"平均: {sum(nums_bnyp)/len(nums_bnyp):.3f}")
    print(f"目標（東経13.413°）との差: {abs(sum(nums_bnyp)/len(nums_bnyp) - 13.413):.3f}")
    print()
    
    # BERLIN全体（Position 64-69）でも確認
    segment_berlin = K4_CIPHER[63:69]
    nums_berlin = [char_to_num(c) for c in segment_berlin]
    
    print(f"BERLIN全体（Position 64-69）:")
    print(f"文字列: {segment_berlin}")
    print(f"数値: {nums_berlin}")
    print(f"合計: {sum(nums_berlin)}")
    print(f"平均: {sum(nums_berlin)/len(nums_berlin):.3f}")

if __name__ == "__main__":
    sliding_window_scan()
