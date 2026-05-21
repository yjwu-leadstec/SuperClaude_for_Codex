<div align="center">

# SuperClaude for Codex

### **OpenAI Codex를 위한 구조화된 개발 워크플로우**

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

## 개요

SuperClaude for Codex는 OpenAI Codex에 **30개의 `/sc-*` 명령어**와 **20개의 전문 에이전트**를 제공합니다. Codex에서 `/sc-brainstorm`, `/sc-implement`, `/sc-test`를 입력하면 구조화된 워크플로우가 활성화됩니다.

**중요**: 이 프로젝트는 **Codex 전용**입니다. `~/.claude`를 읽거나 쓰지 않습니다. 모든 설치는 `~/.codex/`에 이루어집니다.

**명령 구문**: 초기 릴리스에서는 원본 SuperClaude에서 쉽게 이전할 수 있도록 `/sc:*` 형식을 사용했습니다. 이제 권장되는 Codex 친화 구문은 `/sc-*`이며, `/sc:implement` 같은 기존 별칭도 계속 지원됩니다.

**네이티브 Codex 플러그인**: 설치 과정은 이제 SuperClaude for Codex를 로컬 Codex 플러그인으로 등록하고 네이티브 명령 파일을 생성합니다. Codex를 다시 시작하면 `/sc-*` 명령이 slash command 자동 완성에 표시됩니다.

---

## 빠른 시작

```bash
git clone https://github.com/yjwu-leadstec/SuperClaude_for_Codex.git
cd SuperClaude_for_Codex
./install-codex.sh
```

설치 후 Codex에서 입력:

```
/sc-brainstorm "사용자 관리 API 설계"
/sc-implement "인증 미들웨어 추가"
/sc-test
/sc                    # 전체 30개 명령어 표시
```

### 설치 확인

```bash
superclaude-codex doctor
```

### 제거

```bash
superclaude-codex uninstall
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [Installation Guide](docs/codex/installation.md) | 설치 가이드 |
| [Command Reference](docs/codex/commands.md) | 전체 30개 명령어 |
| [Troubleshooting](docs/codex/troubleshooting.md) | FAQ 및 문제 해결 |

---

## 라이선스

MIT License — [LICENSE](LICENSE) 참조.
