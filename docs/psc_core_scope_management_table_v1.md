# PSC Core v1 スコープ整理表

## 採用機能（Core v1）

項目	機能	             内容	                                             理由
1.	状態監視	        ノード/リンクの混雑・遅延・エラーを取得	      全制御の前提
2.	状態モデル	   NORMAL / WARNING / CONGESTED / DEGRADED	 PSCの核となる制御思想
3.	ルート評価	   cost / latency / stability ベースの比較	      基本機能として必須
4.	hysteresis	   切替の揺れ防止	                                   フラッピング対策
5.	trust制御	   trusted / limited / untrusted 判定	           PSCの差別化要素
6.	degraded mode	条件悪化時も通信継続	                          実運用で重要
7.	基本切替	        単一ルートから別ルートへ切替	                     最低限の機能

## 軽く触れる（将来拡張前提）

項目	機能	             内容	                                            扱い
8.	段階切替	        徐々にルートを移行する考え	                    概念のみ記述
9.	連動切替	        A縮小/B拡張の同期制御	                         将来拡張として言及

## 今回除外（Future Extension）

項目	機能	             内容	                                            理由
10.	チャーター転送   大容量専用ルート                                  高度すぎる
11.	帯域予約	        事前帯域確保                                      制御複雑化
12.	多経路集約       複数ルート帯域合成                                Core範囲外
13.	動的再配分       リアルタイム帯域再構成                            設計肥大化
14. 転送スケジューラ 時間/優先度制御                                   上位レイヤ

## 一行定義（そのまま使える）

PSC Core v1 は、状態監視・信頼度考慮・ヒステリシス付きルート選択・単純切替およびdegraded継続制御を提供し、高度な多経路制御および帯域予約機構は将来拡張とする。

## 拡張予定（Future Extension）
Gradual Route Migration
Linked Route Transition
Crossfade Path Handover
Charter Path Transfer
Aggregated Path Reservation
