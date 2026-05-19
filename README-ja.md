<div align="center">

# SuperClaude for Codex

### **OpenAI Codex のための構造化開発ワークフロー**

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Codex-only-green" alt="Codex Only">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/commands-30-orange" alt="30 Commands">
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="README-zh.md">中文</a> •
  <a href="README-ja.md">日本語</a>
</p>

</div>

---

## 概要

SuperClaude for Codex は OpenAI Codex に **30 個の `/sc:*` コマンド** と **20 個のスペシャリストエージェント** を提供します。Codex で `/sc:brainstorm`、`/sc:implement`、`/sc:test` と入力するだけで、構造化されたワークフローが起動します。

**重要**: これは **Codex 専用** プロジェクトです。`~/.claude` を読み書きしません。すべて `~/.codex/` にインストールされます。

---

## クイックスタート

```bash
git clone https://github.com/yjwu-leadstec/SuperClaude_for_Codex.git
cd SuperClaude_for_Codex
./install-codex.sh
```

インストール後、Codex で入力:

```
/sc:brainstorm "ユーザー管理 API を設計"
/sc:implement "認証ミドルウェアを追加"
/sc:test
/sc                    # 全30コマンドを表示
```

### インストール確認

```bash
superclaude-codex doctor
```

### アンインストール

```bash
superclaude-codex uninstall
```

---

## ドキュメント

| ドキュメント | 説明 |
|-------------|------|
| [Installation Guide](docs/codex/installation.md) | インストール手順 |
| [Command Reference](docs/codex/commands.md) | 全30コマンド |
| [Troubleshooting](docs/codex/troubleshooting.md) | よくある問題と FAQ |

---

## ライセンス

MIT License — [LICENSE](LICENSE) を参照。
