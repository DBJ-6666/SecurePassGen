#!/usr/bin/env python3
"""
SecurePassGen - 安全密码生成器（单文件 GUI 版本）
双击即可运行，无需安装任何依赖。

功能：
  - 生成单个或批量密码，自定义长度和字符类型
  - 检测密码强度（弱/中等/强/极强）
  - 一键复制到剪贴板
  - 保存密码到用户指定位置
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import re
from typing import List, Tuple


# ============================================================
# 核心逻辑
# ============================================================

class PasswordGenerator:
    """生成密码学安全的随机密码"""

    def __init__(
        self,
        length: int = 16,
        use_upper: bool = True,
        use_lower: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
    ):
        if length < 4:
            raise ValueError("密码长度至少为 4")
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_symbols = use_symbols

    def _build_charset(self) -> str:
        charset = ""
        if self.use_lower:
            charset += string.ascii_lowercase
        if self.use_upper:
            charset += string.ascii_uppercase
        if self.use_digits:
            charset += string.digits
        if self.use_symbols:
            charset += "!@#$%^&*()-_=+[]{}|;:,.<>?"
        if not charset:
            raise ValueError("至少选择一种字符类型")
        return charset

    def generate(self) -> str:
        charset = self._build_charset()
        password_chars = []

        if self.use_lower:
            password_chars.append(secrets.choice(string.ascii_lowercase))
        if self.use_upper:
            password_chars.append(secrets.choice(string.ascii_uppercase))
        if self.use_digits:
            password_chars.append(secrets.choice(string.digits))
        if self.use_symbols:
            password_chars.append(
                secrets.choice("!@#$%^&*()-_=+[]{}|;:,.<>?")
            )

        remaining = self.length - len(password_chars)
        password_chars.extend(secrets.choice(charset) for _ in range(remaining))

        shuffled = list(password_chars)
        secrets.SystemRandom().shuffle(shuffled)
        return "".join(shuffled)

    def generate_batch(self, count: int) -> List[str]:
        return [self.generate() for _ in range(count)]


class PasswordStrengthChecker:
    """检测密码强度"""

    @staticmethod
    def check(password: str) -> Tuple[str, str]:
        if not password:
            return "弱", "密码为空。"

        score = 0
        feedback = []

        # 长度检查
        length = len(password)
        if length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        else:
            feedback.append("密码太短（建议至少 8 位）。")

        # 字符类型检查
        has_lower = bool(re.search(r"[a-z]", password))
        has_upper = bool(re.search(r"[A-Z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

        variety = sum([has_lower, has_upper, has_digit, has_symbol])
        if variety >= 4:
            score += 3
        elif variety == 3:
            score += 2
        elif variety == 2:
            score += 1
        else:
            feedback.append("建议包含大小写字母、数字和符号。")

        # 常见模式检查
        common_patterns = [
            r"12345", r"qwerty", r"password", r"admin",
            r"abc123", r"letmein", r"welcome",
        ]
        lower_pass = password.lower()
        if any(pattern in lower_pass for pattern in common_patterns):
            score -= 2
            feedback.append("避免使用常见单词或序列（如 password、qwerty）。")

        # 重复字符检查
        if re.search(r"(.)\1{2,}", password):
            score -= 1
            feedback.append("避免重复字符（如 aaa）。")

        # 判定强度等级
        if score >= 5:
            label = "极强"
        elif score >= 3:
            label = "强"
        elif score >= 1:
            label = "中等"
        else:
            label = "弱"

        message = " ".join(feedback) if feedback else "密码习惯良好。"
        return label, message


# ============================================================
# 图形界面
# ============================================================

class SecurePassGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecurePassGen - 密码生成与强度检测")
        self.root.geometry("620x560")
        self.root.resizable(True, True)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 标签页
        self.gen_frame = ttk.Frame(self.notebook)
        self.check_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.gen_frame, text="生成密码")
        self.notebook.add(self.check_frame, text="检测强度")

        self._build_generate_tab()
        self._build_check_tab()

    # ===================== 生成密码标签页 =====================

    def _build_generate_tab(self):
        # 长度
        row1 = ttk.Frame(self.gen_frame)
        row1.pack(fill="x", padx=10, pady=(10, 5))
        ttk.Label(row1, text="密码长度:").pack(side="left")
        self.length_var = tk.IntVar(value=16)
        ttk.Spinbox(row1, from_=4, to=128, textvariable=self.length_var, width=5).pack(
            side="left", padx=5
        )

        # 字符类型
        char_frame = ttk.LabelFrame(self.gen_frame, text="包含字符类型")
        char_frame.pack(fill="x", padx=10, pady=5)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(char_frame, text="大写字母 (A-Z)", variable=self.upper_var).pack(
            anchor="w", padx=10, pady=2
        )
        ttk.Checkbutton(char_frame, text="小写字母 (a-z)", variable=self.lower_var).pack(
            anchor="w", padx=10, pady=2
        )
        ttk.Checkbutton(char_frame, text="数字 (0-9)", variable=self.digits_var).pack(
            anchor="w", padx=10, pady=2
        )
        ttk.Checkbutton(
            char_frame, text="特殊符号 (!@#$...)", variable=self.symbols_var
        ).pack(anchor="w", padx=10, pady=2)

        # 数量
        row2 = ttk.Frame(self.gen_frame)
        row2.pack(fill="x", padx=10, pady=5)
        ttk.Label(row2, text="生成数量:").pack(side="left")
        self.count_var = tk.IntVar(value=1)
        ttk.Spinbox(row2, from_=1, to=50, textvariable=self.count_var, width=5).pack(
            side="left", padx=5
        )
        ttk.Label(row2, text="(1 = 单个，>1 = 批量)").pack(side="left")

        # 按钮行
        btn_frame = ttk.Frame(self.gen_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(btn_frame, text="生成密码", command=self._generate).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="复制到剪贴板", command=self._copy).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="保存到文件", command=self._save).pack(
            side="left", padx=5
        )

        # 结果显示
        result_frame = ttk.LabelFrame(self.gen_frame, text="生成结果")
        result_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.result_text = tk.Text(
            result_frame, height=10, wrap="word", state="disabled"
        )
        scrollbar = ttk.Scrollbar(
            result_frame, orient="vertical", command=self.result_text.yview
        )
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

    def _generate(self):
        length = self.length_var.get()
        count = self.count_var.get()

        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()

        if not any([use_upper, use_lower, use_digits, use_symbols]):
            messagebox.showerror("错误", "请至少选择一种字符类型。")
            return

        try:
            gen = PasswordGenerator(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
            )
            passwords = (
                [gen.generate()] if count == 1 else gen.generate_batch(count)
            )

            self.result_text.configure(state="normal")
            self.result_text.delete("1.0", tk.END)

            for i, pwd in enumerate(passwords, 1):
                line = f"{i}: {pwd}\n" if count > 1 else f"{pwd}\n"
                self.result_text.insert(tk.END, line)

            self.result_text.configure(state="disabled")
            self._last_results = passwords

        except Exception as e:
            messagebox.showerror("生成失败", str(e))

    def _copy(self):
        if not hasattr(self, "_last_results") or not self._last_results:
            messagebox.showwarning("无内容", "请先生成密码。")
            return

        text = "\n".join(self._last_results)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("已复制", "密码已复制到剪贴板。")

    def _save(self):
        if not hasattr(self, "_last_results") or not self._last_results:
            messagebox.showwarning("无内容", "请先生成密码。")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="保存密码到...",
        )
        if not file_path:
            return

        try:
            count = self.count_var.get()
            with open(file_path, "w", encoding="utf-8") as f:
                if count == 1:
                    f.write(self._last_results[0])
                else:
                    for i, pwd in enumerate(self._last_results, 1):
                        f.write(f"{i}: {pwd}\n")
            messagebox.showinfo("保存成功", f"密码已保存到：\n{file_path}")
        except Exception as e:
            messagebox.showerror("保存失败", f"无法保存文件：\n{e}")

    # ===================== 强度检测标签页 =====================

    def _build_check_tab(self):
        row1 = ttk.Frame(self.check_frame)
        row1.pack(fill="x", padx=10, pady=10)
        ttk.Label(row1, text="输入密码:").pack(side="left")

        self.pwd_entry = ttk.Entry(row1, width=30, show="*")
        self.pwd_entry.pack(side="left", padx=5)

        self.show_pwd_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            row1, text="显示", variable=self.show_pwd_var,
            command=self._toggle_show
        ).pack(side="left")

        ttk.Button(self.check_frame, text="检测强度", command=self._check).pack(pady=5)

        self.strength_label = ttk.Label(
            self.check_frame, text="", font=("Arial", 14, "bold")
        )
        self.strength_label.pack(pady=5)

        self.feedback_label = ttk.Label(
            self.check_frame, text="", wraplength=400
        )
        self.feedback_label.pack(pady=5)

    def _toggle_show(self):
        show = "" if self.show_pwd_var.get() else "*"
        self.pwd_entry.configure(show=show)

    def _check(self):
        password = self.pwd_entry.get()
        if not password:
            messagebox.showwarning("提示", "请输入要检测的密码。")
            return

        label, msg = PasswordStrengthChecker.check(password)

        color_map = {
            "弱": "red",
            "中等": "orange",
            "强": "green",
            "极强": "dark green",
        }
        self.strength_label.configure(
            text=f"强度：{label}",
            foreground=color_map.get(label, "black"),
        )
        self.feedback_label.configure(text=f"反馈：{msg}")


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurePassGenApp(root)
    root.mainloop()
