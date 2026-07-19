# news-digest

RSSで収集したニュース記事をGemini APIで自動要約し、Obsidian Syncのvaultに保存する。

## フロー

```
GitHub Actions (cron: JST 6:00)
  → feeds.yaml からRSSを取得
  → Gemini APIで各記事を要約（失敗した場合はdescriptionをそのまま保存）
  → Obsidian Syncのvaultにnews/YYYY-MM-DD.mdとして1日1ファイルで保存
```

## ファイル構成

```
news-digest/
├── feeds.yaml              # 購読するRSSフィードリスト
└── scripts/
    ├── fetch_rss.py        # RSSフェッチ・記事をarticles/YYYY-MM-DD/に保存
    ├── summarize.py        # Gemini APIで記事を要約しai_summaryをフロントマターに追記
    └── save_to_obsidian.py # 記事をObsidian vaultのnews/YYYY-MM-DD.mdに保存
```

## 必要なSecrets

| Secret名 | 内容 |
|---|---|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) でAPIキーを発行して設定 |
| `OBSIDIAN_EMAIL` | Obsidianアカウントのメールアドレス |
| `OBSIDIAN_PASSWORD` | Obsidianアカウントのパスワード |
| `OBSIDIAN_VAULT_NAME` | リモートvault名（`ob sync-list-remote` で確認） |
| `OBSIDIAN_VAULT_PASSWORD` | vaultのE2E暗号化パスワード（アカウントパスワードとは別） |

## RSSフィードのカスタマイズ

`feeds.yaml` を編集する。

```yaml
feeds:
  - https://example.com/feed.rss
```
