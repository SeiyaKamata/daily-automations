# daily-automations

日次自動化タスクをまとめたリポジトリ。

## タスク一覧

| タスク | 概要 |
|---|---|
| [news-digest](tasks/news-digest/README.md) | RSSニュースを要約してObsidian Syncのvaultに保存 |

## セットアップ

### GitHub Secrets

| Secret名 | 用途 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio のAPIキー（news-digest） |
| `OBSIDIAN_EMAIL` | Obsidianアカウントのメールアドレス（news-digest） |
| `OBSIDIAN_PASSWORD` | Obsidianアカウントのパスワード（news-digest） |
| `OBSIDIAN_VAULT_NAME` | リモートvault名（news-digest） |
| `OBSIDIAN_VAULT_PASSWORD` | vaultのE2E暗号化パスワード（news-digest） |
