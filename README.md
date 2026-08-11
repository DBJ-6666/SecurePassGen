# SecurePassGen

A single-file, zero-dependency desktop password tool.

- **Cryptographically secure** password generation (Python `secrets` module)
- **Password strength checker** (length, character variety, common pattern detection)
- **One-click copy** to clipboard
- **Clean GUI** built with tkinter
- **Batch generation** — 1–50 passwords at once

## Quick Start

```bash
git clone https://github.com/DBJ-6666/SecurePassGen.git
cd SecurePassGen
python3 main.py
```

Requires **Python 3.6+**. No external dependencies.

> **Linux users:** if tkinter is missing, run `sudo apt install python3-tk`.

## Screenshot

```
+--------------------------------------------------+
|  SecurePassGen - Password Generator & Checker     |
|  +-- Generate ---+--- Check -------------------+  |
|  |  Length: [16]                               |  |
|  |  [x] Uppercase (A-Z)                        |  |
|  |  [x] Lowercase (a-z)                        |  |
|  |  [x] Digits (0-9)                           |  |
|  |  [x] Symbols (!@#$...)                      |  |
|  |  Count: [1]                                 |  |
|  |  [Generate]                                 |  |
|  |  +--------------------------------------+   |  |
|  |  | kK9#mPx2@vL5nQr8                     |   |  |
|  |  +--------------------------------------+   |  |
|  |  [Copy All to Clipboard]                    |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
```

## Features

### Password Generator

| Option | Default | Range |
|--------|---------|-------|
| Length | 16 | 4–128 |
| Uppercase (A-Z) | On | toggle |
| Lowercase (a-z) | On | toggle |
| Digits (0-9) | On | toggle |
| Symbols (!@#$...) | On | toggle |
| Batch count | 1 | 1–50 |

### Strength Checker

Scoring rules:

| Rule | Score |
|------|-------|
| Length ≥ 16 | +3 |
| Length ≥ 12 | +2 |
| Length ≥ 8 | +1 |
| All 4 char types | +3 |
| 3 char types | +2 |
| 2 char types | +1 |
| Common patterns (password, qwerty, 12345, etc.) | -2 |
| Repeated characters (aaa, 111) | -1 |

| Score | Rating | Color |
|-------|--------|-------|
| ≥5 | Excellent | Dark green |
| 3–4 | Strong | Green |
| 1–2 | Medium | Orange |
| ≤0 | Weak | Red |

## Dependencies

**Zero external dependencies.** Uses only Python standard library:

- `tkinter` — GUI toolkit (bundled with macOS/Windows Python)
- `secrets` — cryptographically secure random number generation
- `re`, `string` — regex and string utilities

## Project Structure

```
SecurePassGen/
├── main.py       # Main program (single file)
├── README.md     # This file
├── .gitignore
└── LICENSE       # MIT
```

## License

MIT — see [LICENSE](LICENSE)

---

# SecurePassGen — 安全密码生成与强度检测工具

单文件、零依赖的桌面密码工具。

- **密码学安全**的随机密码生成（Python `secrets` 模块）
- **密码强度检测**（长度、字符多样性、常见模式识别）
- **一键复制**到剪贴板
- **图形界面**（tkinter），简洁直观
- **批量生成**，一次 1–50 个

## 快速开始

```bash
git clone https://github.com/DBJ-6666/SecurePassGen.git
cd SecurePassGen
python3 main.py
```

需要 **Python 3.6+**，零外部依赖。Linux 如缺 tkinter：`sudo apt install python3-tk`。

## 功能

### 密码生成

| 参数 | 默认值 | 范围 |
|------|--------|------|
| 长度 | 16 | 4–128 |
| 大写字母 | ✅ | 开关 |
| 小写字母 | ✅ | 开关 |
| 数字 | ✅ | 开关 |
| 符号 | ✅ | 开关 |
| 批量数量 | 1 | 1–50 |

### 强度检测

| 规则 | 分数 |
|------|------|
| 长度 ≥ 16 | +3 |
| 长度 ≥ 12 | +2 |
| 长度 ≥ 8 | +1 |
| 4 类字符齐全 | +3 |
| 3 类字符 | +2 |
| 2 类字符 | +1 |
| 常见弱密码模式 | -2 |
| 重复字符 (aaa, 111) | -1 |

| 分数 | 评级 | 颜色 |
|------|------|------|
| ≥5 | 极强 | 深绿 |
| 3–4 | 强 | 绿色 |
| 1–2 | 中等 | 橙色 |
| ≤0 | 弱 | 红色 |

## 许可证

MIT — 详见 [LICENSE](LICENSE)
