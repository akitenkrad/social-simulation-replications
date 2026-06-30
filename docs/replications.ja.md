[English](replications.md) | **日本語**

# 再現実装カタログ

社会シミュレーション系論文の再現実装 全 27 件を，モデリングパラダイムごとに分類しています：古典的エージェントベースモデル 6 件，LLM ベースの社会シミュレーション 20 件，ゲーム AI・その他 1 件．

## 古典的エージェントベースモデル

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 1971 | Schelling, "Dynamic Models of Segregation" | 住み分け（分居） | [schelling1971](https://github.com/akitenkrad/schelling1971) |
| 1973 | Granovetter, "The Strength of Weak Ties" | 弱い紐帯・ネットワーク | [granovetter1973](https://github.com/akitenkrad/granovetter1973) |
| 1974 | Noelle-Neumann, "The Spiral of Silence: A Theory of Public Opinion" | 沈黙の螺旋 (世論形成) | [noelleneumann1974](https://github.com/akitenkrad/noelleneumann1974) |
| 1997 | Axelrod, "The Dissemination of Culture" | 文化の伝播 | [axelrod1997](https://github.com/akitenkrad/axelrod1997) |
| 2002 | Hegselmann & Krause, "Opinion Dynamics and Bounded Confidence: Models, Analysis and Simulation" | 限定信頼モデル | [hegselmann2002](https://github.com/akitenkrad/hegselmann2002) |
| 2005 | Hegselmann & Krause, "Opinion Dynamics Driven by Various Ways of Averaging" | 意見ダイナミクス (平均演算子) | [hegselmann2005](https://github.com/akitenkrad/hegselmann2005) |

## LLM ベースの社会シミュレーション

### 意見・規範・集合行動

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 1999 | Edmondson, "Psychological Safety and Learning Behavior in Work Teams" | 心理的安全性とチーム学習 | [edmondson1999](https://github.com/akitenkrad/edmondson1999) |
| 2011 | Detert & Edmondson, "Implicit Voice Theories: Taken-for-Granted Rules of Self-Censorship at Work" | 暗黙の発言理論 (自己検閲) | [detert2011](https://github.com/akitenkrad/detert2011) |
| 2013 | Knoll & van Dick, "Do I Hear the Whistle…? A First Attempt to Measure Four Forms of Employee Silence and Their Correlates" | 従業員サイレンス (4 動機形態) | [knoll2013](https://github.com/akitenkrad/knoll2013) |
| 2013 | Brinsfield, "Employee Silence Motives: Investigation of Dimensionality and Development of Measures" | 従業員サイレンス (6 動機次元) | [brinsfield2013](https://github.com/akitenkrad/brinsfield2013) |
| 2019 | Fujimura & Hino, "Silence and Voice in the Organization: The Influences of Silence Motives and Psychological Safety" | 沈黙・発言の規定要因 SEM (日本) | [fujimura2019](https://github.com/akitenkrad/fujimura2019) |
| 2023 | Argyle et al., "Out of One, Many: Using Language Models to Simulate Human Samples" | シリコンサンプル (世論・調査) | [argyle2023](https://github.com/akitenkrad/argyle2023) |
| 2024 | Chuang et al., "Simulating Opinion Dynamics with Networks of LLM-based Agents" | 意見ダイナミクス | [chuang2024](https://github.com/akitenkrad/chuang2024) |
| 2024 | Ren et al., "Emergence of Social Norms in Generative Agent Societies (CRSEC)" | 社会規範 | [ren2024](https://github.com/akitenkrad/ren2024) |
| 2024 | Mou et al., "Unveiling the Truth and Facilitating Change: Towards Agent-based Large-scale Social Movement Simulation (HiSim)" | 社会運動 | [mou2024](https://github.com/akitenkrad/mou2024) |
| 2024 | Sun et al., "Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a Large Language Model Based on Group-Level Demographic Information" | 集団レベルのシリコンサンプリング (logprob 非依存) | [sun2024](https://github.com/akitenkrad/sun2024) |
| 2026 | Gong et al., "Characterizing the Ability of LLMs to Recapitulate Americans' Distributional Responses to Public Opinion Polling Questions Across Political Issues" | 分布直接予測 (DD) と個人反復 (SI) の比較 (logprob 非依存) | [gong2026](https://github.com/akitenkrad/gong2026) |

### 経済・市場・資源

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 2023 | Han et al., "Guinea Pig Trials Utilizing GPT: A Smart Agent-Based Modeling Approach for Studying Firm Competition and Collusion (SABM)" | 企業間競争・共謀 | [han2023](https://github.com/akitenkrad/han2023) |
| 2024 | Li et al., "EconAgent: LLM-Empowered Agents for Simulating Macroeconomic Activities" | マクロ経済 | [li2024](https://github.com/akitenkrad/li2024) |
| 2024 | Ji et al., "SRAP-Agent: Simulating and Optimizing Scarce Resource Allocation Policy with LLM-based Agent" | 資源配分 | [ji2024](https://github.com/akitenkrad/ji2024) |

### 競争・紛争

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 2024 | Zhao et al., "CompeteAI: Understanding the Competition Dynamics of LLM-based Agents" | 競争 | [zhao2024](https://github.com/akitenkrad/zhao2024) |
| 2024 | Hua et al., "War and Peace (WarAgent): LLM-based Multi-Agent Simulation of World Wars" | 国際紛争 | [hua2024](https://github.com/akitenkrad/hua2024) |

### 基盤・大規模シミュレータ

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 2023 | Gao et al., "S3: Social-network Simulation System with LLM-Empowered Agents" | ソーシャルネットワーク基盤 | [gao2023](https://github.com/akitenkrad/gao2023) |
| 2024 | Yang et al., "OASIS: Open Agent Social Interaction Simulations with One Million Agents" | 大規模シミュレーション基盤 | [yang2024](https://github.com/akitenkrad/yang2024) |
| 2025 | Wang et al., "YuLan-OneSim: Towards the Next Generation of Social Simulator with Large Language Models" | シミュレータ基盤 | [wang2025](https://github.com/akitenkrad/wang2025) |

### 認知バイアス・行動評価

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 2022 | Jones & Steinhardt, "Capturing Failures of Large Language Models via Human Cognitive Biases" | 人間の認知バイアスを介した LLM の質的失敗の誘発 | [jones2022](https://github.com/akitenkrad/jones2022) |

## ゲーム AI・その他

| 年 | 論文 | テーマ | リポジトリ |
|----|------|--------|------------|
| 1994–1999 | Buro, "Logistello (7 papers)" | オセロのゲーム AI | [logistello](https://github.com/akitenkrad/rs-logistello) |
