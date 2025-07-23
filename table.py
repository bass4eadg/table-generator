import tkinter as tk
import re

# 新機能
#
# 自動で列数判定（cの数調整）
# 表のタイトル欄の入力が\caption{}に反映（同種の表を量産するときのタイトル手間軽減想定）
# \label{}の有無の選択
# 2セル結合したいときは右側のセルに「@」のみいれとく
#
# 数式モード
# 表の1行目の[]外に存在する半角英数字を$で囲む（物理量を斜体にする目的）
# 　a_xyz → $a_{xyz}$ 、a^234 → $a^{234}$ みたいな変換にも対応
#   a_i^2 とか a_xyz^234i とかは最初においた記号が最優先される。


def generate_table():
    data = input_text.get("1.0", "end-1c").splitlines()
    formatted_data = []
    cntmax = 0
    c = "c"

    for i, line in enumerate(data):
        formatted_line = " & ".join(line.split()) + r"\\"
        formatted_line = formatted_line.replace(",", "&")

        if i == 0 and val2.get() == 0:
            # 1行目の処理
            def replace_match(match):
                word = match.group(0)
                # 半角文字で、[]の内側にない文字列を$で囲む
                return f"${word}$"

            # 半角英数字を検出し、[]の内側にない文字列を$で囲む
            formatted_line = re.sub(
                r"(?<!\[)([a-zA-Z0-9]+)(?!\])", replace_match, formatted_line
            )

            formatted_line = formatted_line.replace("$_$", "_").replace("$^$", "^")
            formatted_line = re.sub(r"\$(.*?)_(.*?)\$", r"$\1_{\2}$", formatted_line)
            formatted_line = re.sub(r"\$(.*?)\^(.*?)\$", r"$\1^{\2}$", formatted_line)
            formatted_line = re.sub(
                r"(\S*)\s&\s\@", r"\\multicolumn{2}{c}{\1}", formatted_line
            )

        tmp = formatted_line.count("&")
        if cntmax < tmp:
            cntmax = tmp

        formatted_data.append(formatted_line)

        if i == 0:
            formatted_data.append(r"\hline\hline")

    c += "c" * cntmax
    output_text.delete("1.0", "end")
    output_text.insert("end-1c", "\\begin{table}[H]\n")
    output_text.insert("end-1c", "\centering\n")
    output_text.insert("end-1c", f"\caption{{{caption.get('1.0', 'end-1c')}}}\n")
    if val1.get():
        output_text.insert("end-1c", "\label{}\n")
    output_text.insert("5.0", f"\\begin{{tabular}}{{{c}}}\n")
    output_text.insert("end-1c", "\hline\n")
    output_text.insert("end-1c", "\n".join(formatted_data))
    output_text.insert("end-1c", "\n\hline\n")
    output_text.insert("end-1c", "\end{tabular}\n")
    output_text.insert("end-1c", "\end{table}")
    copy()


def copy():
    output_text.clipboard_clear()
    output_text.clipboard_append(output_text.get("1.0", "end-1c"))
    output_text.update()

    # テキストボックス内のテキストを削除
    input_text.delete("1.0", "end")


window_main = tk.Tk()
window_main.geometry("415x380")
window_main.title("table generator (.csv → .tex)")

caption_label = tk.Label(text="⬇caption")
caption_label.pack(pady=5)

caption = tk.Text(height=2, width=50)
caption.pack(pady=5)

input_text_label = tk.Label(text="⬇data")
input_text_label.pack(pady=5)

input_text = tk.Text(height=5, width=50)
input_text.pack(pady=10)

generate_button = tk.Button(
    text="generate & copy", command=generate_table, width=20, height=3
)
generate_button.pack(side=None, pady=5)

output_text = tk.Text(window_main, height=55, width=25)
output_text.pack(side=tk.LEFT, padx=10, pady=5)

val2 = tk.IntVar()
check2 = tk.Checkbutton(text="$...$", variable=val2, onvalue=0, offvalue=1)
check2.pack(side=tk.LEFT, padx=10, pady=None)

val1 = tk.IntVar()
check1 = tk.Checkbutton(text="lable", variable=val1, onvalue=1, offvalue=0)
check1.pack(side=tk.LEFT, padx=10, pady=None)

window_main.mainloop()
