#!/usr/bin/env python3
"""
SecurePassGen - 安全密码生成器（单文件 GUI 版本）
双击即可运行，无需安装任何依赖。

功能：
  - 生成单个或批量密码，自定义长度和字符类型
  - 检测密码强度（弱/中等/强/极强）
  - 一键复制到剪贴板
  - 保存密码到用户指定位置
  - 中英文界面切换
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import re
from typing import List, Tuple


# ============================================================
# 多语言文本字典
# ============================================================

LANGS = {
    "zh": {
        "title": "SecurePassGen - 密码生成与强度检测",
        "tab_generate": "生成密码",
        "tab_check": "检测强度",
        "length_label": "密码长度:",
        "char_types_frame": "包含字符类型",
        "upper": "大写字母 (A-Z)",
        "lower": "小写字母 (a-z)",
        "digits": "数字 (0-9)",
        "symbols": "特殊符号 (!@#$...)",
        "count_label": "生成数量:",
        "count_hint": "(1 = 单个，>1 = 批量)",
        "btn_generate": "生成密码",
        "btn_copy": "复制到剪贴板",
        "btn_save": "保存到文件",
        "result_frame": "生成结果",
        "input_label": "输入密码:",
        "show_pwd": "显示",
        "btn_check": "检测强度",
        "strength_prefix": "强度：",
        "feedback_prefix": "反馈：",
        "msg_select_charset": "请至少选择一种字符类型。",
        "msg_error": "错误",
        "msg_generate_fail": "生成失败",
        "msg_no_content": "无内容",
        "msg_generate_first": "请先生成密码。",
        "msg_copied": "已复制",
        "msg_copied_text": "密码已复制到剪贴板。",
        "msg_save_title": "保存密码到...",
        "msg_save_success": "保存成功",
        "msg_save_fail": "保存失败",
        "msg_saved": "密码已保存到：",
        "msg_save_error": "无法保存文件：",
        "msg_empty_pwd": "提示",
        "msg_enter_pwd": "请输入要检测的密码。",
        "strength_weak": "弱",
        "strength_moderate": "中等",
        "strength_strong": "强",
        "strength_very_strong": "极强",
        "feedback_empty": "密码为空。",
        "feedback_short": "密码太短（建议至少 8 位）。",
        "feedback_variety": "建议包含大小写字母、数字和符号。",
        "feedback_common": "避免使用常见单词或序列（如 password、qwerty）。",
        "feedback_repeat": "避免重复字符（如 aaa）。",
        "feedback_good": "密码习惯良好。",
        "lang_btn": "English",
    },
    "en": {
        "title": "SecurePassGen - Password Generator & Strength Checker",
        "tab_generate": "Generate",
        "tab_check": "Check",
        "length_label": "Length:",
        "char_types_frame": "Character Types",
        "upper": "Uppercase (A-Z)",
        "lower": "Lowercase (a-z)",
        "digits": "Digits (0-9)",
        "symbols": "Symbols (!@#$...)",
        "count_label": "Count:",
        "count_hint": "(1 = single, >1 = batch)",
        "btn_generate": "Generate",
        "btn_copy": "Copy to Clipboard",
        "btn_save": "Save to File",
        "result_frame": "Results",
        "input_label": "Enter password:",
        "show_pwd": "Show",
        "btn_check": "Check Strength",
        "strength_prefix": "Strength: ",
        "feedback_prefix": "Feedback: ",
        "msg_select_charset": "Please select at least one character type.",
        "msg_error": "Error",
        "msg_generate_fail": "Generation Failed",
        "msg_no_content": "No Content",
        "msg_generate_first": "Please generate a password first.",
        "msg_copied": "Copied",
        "msg_copied_text": "Passwords copied to clipboard.",
        "msg_save_title": "Save passwords as...",
        "msg_save_success": "Save Successful",
        "msg_save_fail": "Save Failed",
        "msg_saved": "Saved to: ",
        "msg_save_error": "Unable to save file: ",
        "msg_empty_pwd": "Warning",
        "msg_enter_pwd": "Please enter a password to check.",
        "strength_weak": "Weak",
        "strength_moderate": "Moderate",
        "strength_strong": "Strong",
        "strength_very_strong": "Very Strong",
        "feedback_empty": "Password is empty.",
        "feedback_short": "Password is too short (minimum 8 recommended).",
        "feedback_variety": "Use a mix of uppercase, lowercase, digits, and symbols.",
        "feedback_common": "Avoid common words or sequences (e.g., password, qwerty).",
        "feedback_repeat": "Avoid repeating characters (e.g., aaa).",
        "feedback_good": "Good password hygiene.",
        "lang_btn": "中文",
    },
}


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
    """检测密码强度（返回英文标签，由界面翻译）"""

    @staticmethod
    def check(password: str) -> Tuple[str, str]:
        """returns (strength_key, feedback_key)"""
        if not password:
            return "weak", "empty"

        score = 0
        feedback = []

        length = len(password)
        if length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        else:
            feedback.append("short")

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
            feedback.append("variety")

        common_patterns = [
            r"12345", r"qwerty", r"password", r"admin",
            r"abc123", r"letmein", r"welcome",
        ]
        lower_pass = password.lower()
        if any(pattern in lower_pass for pattern in common_patterns):
            score -= 2
            feedback.append("common")

        if re.search(r"(.)\1{2,}", password):
            score -= 1
            feedback.append("repeat")

        if score >= 5:
            label = "very_strong"
        elif score >= 3:
            label = "strong"
        elif score >= 1:
            label = "moderate"
        else:
            label = "weak"

        if not feedback:
            feedback.append("good")
        return label, feedback


# ============================================================
# 图形界面
# ============================================================

class SecurePassGenApp:
    def __init__(self, root):
        self.root = root
        self.lang = "zh"  # 默认中文
        self.root.title(self.t("title"))
        self.root.geometry("620x560")
        self.root.resizable(True, True)

        # 语言切换按钮（放在顶部）
        self.lang_btn = ttk.Button(root, text=self.t("lang_btn"), command=self.switch_lang)
        self.lang_btn.pack(anchor="ne", padx=10, pady=5)

        # 标签容器
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._last_results = None
        self._build_ui()

    def t(self, key):
        """获取当前语言的文本"""
        return LANGS[self.lang][key]

    def switch_lang(self):
        """切换语言并重建界面"""
        self.lang = "en" if self.lang == "zh" else "zh"
        self._last_results = None
        self._rebuild_ui()

    def _rebuild_ui(self):
        """销毁现有控件并重新创建"""
        # 销毁语言按钮以外的所有控件（保留 notebook 和内部框架）
        for widget in self.root.winfo_children():
            if widget is self.lang_btn:
                continue
            widget.destroy()

        # 重新创建 notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._build_ui()

        # 更新窗口标题和语言按钮文字
        self.root.title(self.t("title"))
        self.lang_btn.config(text=self.t("lang_btn"))

    def _build_ui(self):
        """构建两个标签页"""
        self.gen_frame = ttk.Frame(self.notebook)
        self.check_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.gen_frame, text=self.t("tab_generate"))
        self.notebook.add(self.check_frame, text=self.t("tab_check"))

        self._build_generate_tab()
        self._build_check_tab()

    # ===================== 生成密码标签页 =====================

    def _build_generate_tab(self):
        # 长度
        row1 = ttk.Frame(self.gen_frame)
        row1.pack(fill="x", padx=10, pady=(10, 5))
        ttk.Label(row1, text=self.t("length_label")).pack(side="left")
        self.length_var = tk.IntVar(value=16)
        ttk.Spinbox(row1, from_=4, to=128, textvariable=self.length_var, width=5).pack(
            side="left", padx=5
        )

        # 字符类型
        char_frame = ttk.LabelFrame(self.gen_frame, text=self.t("char_types_frame"))
        char_frame.pack(fill="x", padx=10, pady=5)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(char_frame, text=self.t("upper"), variable=self.upper_var).pack(
            anchor="w", padx=10, pady=2
        )
        ttk.Checkbutton(char_frame, text=self.t("lower"), variable=self.lower_var).pack(
            anchor="w", padx=10, pady=2
        )
        ttk.Checkbutton(char_frame, text=self.t("digits"), variable=self.digits_var).pack(
            anchor="w", padx=10, pady=2
        )
        ttk.Checkbutton(char_frame, text=self.t("symbols"), variable=self.symbols_var).pack(
            anchor="w", padx=10, pady=2
        )

        # 数量
        row2 = ttk.Frame(self.gen_frame)
        row2.pack(fill="x", padx=10, pady=5)
        ttk.Label(row2, text=self.t("count_label")).pack(side="left")
        self.count_var = tk.IntVar(value=1)
        ttk.Spinbox(row2, from_=1, to=50, textvariable=self.count_var, width=5).pack(
            side="left", padx=5
        )
        ttk.Label(row2, text=self.t("count_hint")).pack(side="left")

        # 按钮行
        btn_frame = ttk.Frame(self.gen_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(btn_frame, text=self.t("btn_generate"), command=self._generate).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text=self.t("btn_copy"), command=self._copy).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text=self.t("btn_save"), command=self._save).pack(
            side="left", padx=5
        )

        # 结果显示
        result_frame = ttk.LabelFrame(self.gen_frame, text=self.t("result_frame"))
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
            messagebox.showerror(self.t("msg_error"), self.t("msg_select_charset"))
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
            messagebox.showerror(self.t("msg_generate_fail"), str(e))

    def _copy(self):
        if not self._last_results:
            messagebox.showwarning(self.t("msg_no_content"), self.t("msg_generate_first"))
            return

        text = "\n".join(self._last_results)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo(self.t("msg_copied"), self.t("msg_copied_text"))

    def _save(self):
        if not self._last_results:
            messagebox.showwarning(self.t("msg_no_content"), self.t("msg_generate_first"))
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title=self.t("msg_save_title"),
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
            messagebox.showinfo(self.t("msg_save_success"), f"{self.t('msg_saved')}\n{file_path}")
        except Exception as e:
            messagebox.showerror(self.t("msg_save_fail"), f"{self.t('msg_save_error')}\n{e}")

    # ===================== 强度检测标签页 =====================

    def _build_check_tab(self):
        row1 = ttk.Frame(self.check_frame)
        row1.pack(fill="x", padx=10, pady=10)
        ttk.Label(row1, text=self.t("input_label")).pack(side="left")

        self.pwd_entry = ttk.Entry(row1, width=30, show="*")
        self.pwd_entry.pack(side="left", padx=5)

        self.show_pwd_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            row1, text=self.t("show_pwd"), variable=self.show_pwd_var,
            command=self._toggle_show
        ).pack(side="left")

        ttk.Button(self.check_frame, text=self.t("btn_check"), command=self._check).pack(pady=5)

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
            messagebox.showwarning(self.t("msg_empty_pwd"), self.t("msg_enter_pwd"))
            return

        strength_key, feedback_keys = PasswordStrengthChecker.check(password)

        # 强度映射
        strength_map = {
            "weak": self.t("strength_weak"),
            "moderate": self.t("strength_moderate"),
            "strong": self.t("strength_strong"),
            "very_strong": self.t("strength_very_strong"),
        }
        # 反馈映射
        feedback_map = {
            "empty": self.t("feedback_empty"),
            "short": self.t("feedback_short"),
            "variety": self.t("feedback_variety"),
            "common": self.t("feedback_common"),
            "repeat": self.t("feedback_repeat"),
            "good": self.t("feedback_good"),
        }

        strength_text = strength_map.get(strength_key, strength_key)
        feedback_texts = [feedback_map.get(k, k) for k in feedback_keys]

        color_map = {
            "弱": "red", "Weak": "red",
            "中等": "orange", "Moderate": "orange",
            "强": "green", "Strong": "green",
            "极强": "dark green", "Very Strong": "dark green",
        }

        self.strength_label.configure(
            text=f"{self.t('strength_prefix')}{strength_text}",
            foreground=color_map.get(strength_text, "black"),
        )
        self.feedback_label.configure(
            text=f"{self.t('feedback_prefix')}{' '.join(feedback_texts)}"
        )


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurePassGenApp(root)
    root.mainloop()