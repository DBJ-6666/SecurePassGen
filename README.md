# SecurePassGen — 安全密码生成与强度检测工具

**SecurePassGen** 是一款单文件、零依赖的桌面密码工具，支持：
- 密码学安全的随机密码生成（使用 Python `secrets` 模块）
- 密码强度检测（长度、字符多样性、常见模式识别）
- 一键复制到剪贴板
- 图形界面（tkinter），简洁直观
- 批量生成，一次可生成 1-50 个密码
- 中英双语界面

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/你的用户名/SecurePassGen.git
cd SecurePassGen

# 直接运行（需要 Python 3.6+）
python3 main.py
```

## 依赖

**零外部依赖** — 仅使用 Python 标准库：
- `tkinter` — 图形界面（macOS/Windows 自带，Linux 需 `sudo apt install python3-tk`）
- `secrets` — 密码学安全随机数生成
- `re`, `string` — 正则与字符串处理

## 功能

### 密码生成
- 长度：4-128 位可调（默认 16）
- 字符类型：大写/小写/数字/符号，可自由组合
- 批量：一次生成 1-50 个密码

### 强度检测
- 长度评分：≥16 位 +3 分，≥12 位 +2 分，≥8 位 +1 分
- 字符多样性：4 类齐全 +3 分，3 类 +2 分，2 类 +1 分
- 常见模式扣分：识别 password、qwerty、12345 等弱密码
- 重复字符扣分：连续重复 3 次以上扣分

| 总分 | 评级 | 颜色 |
|------|------|------|
| ≥5 | 极强 | 深绿 |
| 3-4 | 强 | 绿色 |
| 1-2 | 中等 | 橙色 |
| ≤0 | 弱 | 红色 |

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
