# AI Collaboration Experiment

ClaudeとGeminiによる協働対話実験プロジェクト

## 概要

2つの異なるAIシステム（AnthropicのClaudeとGoogleのGemini）を対話させ、複雑な問題解決や創造的なタスクに取り組ませる実験プロジェクトです。

### 実験の目的

- AI間の協働による問題解決能力の検証
- 異なるアーキテクチャ・学習データによる視点の多様性
- 人間の介入なしでの自律的な議論の質の評価

## 現在の実験

### セッション001: Kryptos K4暗号解読
- **日付**: 2024-12-24
- **参加AI**: Claude (Sonnet 4) × Gemini
- **議題**: 35年未解決のKryptos K4暗号の解読アプローチ
- **結果**: [logs/kryptos_k4_dialogue_20241224.json](logs/kryptos_k4_dialogue_20241224.json)

## プロジェクト構成

```
AI_Collaboration_Experiment/
├── README.md              # このファイル
├── docs/
│   └── insights.md       # 実験から得られた知見
└── logs/
    └── *.json            # 対話ログ（JSON形式）
```

## ログ形式

対話ログはJSON形式で保存されます：

```json
{
  "session_info": {
    "session_id": "session_001",
    "date": "2024-12-24",
    "topic": "研究テーマ",
    "participants": { ... }
  },
  "dialogue": [ ... ],
  "summary": { ... }
}
```

## 次のステップ

- さらなる暗号解読議論の深化
- 他の未解決問題への挑戦
- AI間対話の質的分析

## ライセンス

このプロジェクトは実験的研究目的で作成されています。

---

**実験開始日**: 2024年12月24日  
**最終更新**: 2024年12月24日
