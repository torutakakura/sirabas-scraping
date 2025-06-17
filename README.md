# 京都芸術大学シラバススクレイパー

京都芸術大学通信教育部のWebサイトから、シラバス情報を自動的に収集し、構造化されたデータとして出力するPythonツールです。

## 概要

本ツールは、学科・コース・科目の階層構造を再帰的に辿りながら、全科目の詳細情報を効率的に収集します。収集したデータはCSVファイルまたはGoogleスプレッドシートに出力可能です。

## 機能

- 🕷️ **階層的Webスクレイピング**: 24学科の全科目情報を自動収集
- 📊 **データ抽出**: 16項目以上の詳細情報を抽出
- 💾 **柔軟な出力形式**: CSV/Googleスプレッドシート対応
- 📈 **進捗管理**: リアルタイムの進捗表示とログ機能
- 🔄 **レジューム機能**: 中断からの再開が可能

## インストール

### 前提条件

- Python 3.12以上
- uv (Python Package Manager)

### セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/sirabas-scraping.git
cd sirabas-scraping

# 仮想環境の作成
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係のインストール（実装予定）
uv pip install -r requirements.txt
```

## 使用方法

```bash
# スクレイパーの実行（実装予定）
sirabas-scraper
```

## プロジェクト構造

```
sirabas-scraping/
├── src/
│   ├── scrapers/      # スクレイピングモジュール
│   ├── parsers/       # HTMLパーサー
│   ├── models/        # データモデル
│   ├── exporters/     # データ出力
│   └── utils/         # ユーティリティ
├── tests/             # テストコード
├── config/            # 設定ファイル
├── logs/              # ログファイル
├── output/            # 出力ファイル
└── pyproject.toml     # プロジェクト設定
```

## 開発状況

- [x] プロジェクト初期化
- [ ] 依存関係のインストール
- [ ] 設定管理システム
- [ ] HTTPクライアント実装
- [ ] HTMLパーサー開発
- [ ] データベース設計
- [ ] スクレイピング機能実装
- [ ] 出力機能実装

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを作成して変更内容を議論してください。
