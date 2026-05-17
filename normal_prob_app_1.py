import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Streamlit Cloud でも動く日本語フォント設定
plt.rcParams["font.family"] = ['IPAexGothic', 'Noto Sans CJK JP', 'TakaoGothic', 'sans-serif']


st.title("正規分布の確率計算アプリ")
st.write("平均 μ、標準偏差 σ、区間 a・b を指定して確率を求めます。")

# -------------------------
# サイドバー：入力
# -------------------------
st.sidebar.header("パラメータ設定")

mu = st.sidebar.number_input("平均 μ", value=50.0, step=1.0)
sigma = st.sidebar.number_input("標準偏差 σ", value=10.0, step=1.0, min_value=0.1)

mode = st.sidebar.radio(
    "求めたい確率の形式",
    ("P(X ≥ a)", "P(X ≤ b)", "P(a ≤ X ≤ b)")
)

if mode == "P(X ≥ a)":
    a = st.sidebar.number_input("a の値", value=60.0, step=1.0)
    b = None

elif mode == "P(X ≤ b)":
    b = st.sidebar.number_input("b の値", value=40.0, step=1.0)
    a = None

else:
    a = st.sidebar.number_input("a の値", value=40.0, step=1.0)
    b = st.sidebar.number_input("b の値", value=60.0, step=1.0)
    if a > b:
        st.error("エラー：a < b となるように入力してください。")

# -------------------------
# 確率計算
# -------------------------
def calc_prob(mu, sigma, a=None, b=None):
    if a is not None and b is None:
        z = (a - mu) / sigma
        return 1 - norm.cdf(z), z, None

    elif a is None and b is not None:
        z = (b - mu) / sigma
        return norm.cdf(z), z, None

    elif a is not None and b is not None:
        z1 = (a - mu) / sigma
        z2 = (b - mu) / sigma
        return norm.cdf(z2) - norm.cdf(z1), z1, z2

p, z1, z2 = calc_prob(mu, sigma, a, b)

# -------------------------
# 結果表示
# -------------------------
st.subheader("求めた確率")
st.write(f"### **{p:.4f}**")

# -------------------------
# 標準化の式を表示
# -------------------------
st.subheader("標準化の式")

if mode == "P(X ≥ a)":
    st.latex(r"Z = \frac{a - \mu}{\sigma}")
    st.write(f"Z = ({a} − {mu}) / {sigma} = **{z1:.4f}**")

elif mode == "P(X ≤ b)":
    st.latex(r"Z = \frac{b - \mu}{\sigma}")
    st.write(f"Z = ({b} − {mu}) / {sigma} = **{z1:.4f}**")

else:
    st.latex(r"Z_1 = \frac{a - \mu}{\sigma},\quad Z_2 = \frac{b - \mu}{\sigma}")
    st.write(f"Z₁ = ({a} − {mu}) / {sigma} = **{z1:.4f}**")
    st.write(f"Z₂ = ({b} − {mu}) / {sigma} = **{z2:.4f}**")

# -------------------------
# グラフ描画
# -------------------------
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 400)
y = norm.pdf(x, mu, sigma)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, label=f"N({mu}, {sigma}²)")

# 塗りつぶし
if a is not None and b is None:
    xs = np.linspace(a, mu + 4*sigma, 200)
    ys = norm.pdf(xs, mu, sigma)
    ax.fill_between(xs, ys, alpha=0.3, color="orange", label=f"X ≥ {a}")

elif a is None and b is not None:
    xs = np.linspace(mu - 4*sigma, b, 200)
    ys = norm.pdf(xs, mu, sigma)
    ax.fill_between(xs, ys, alpha=0.3, color="orange", label=f"X ≤ {b}")

elif a is not None and b is not None:
    xs = np.linspace(a, b, 200)
    ys = norm.pdf(xs, mu, sigma)
    ax.fill_between(xs, ys, alpha=0.3, color="orange", label=f"{a} ≤ X ≤ {b}")

# ★ a・b の縦線を追加
if a is not None:
    ax.axvline(a, color="blue", linestyle="--", label=f"a = {a}")

if b is not None:
    ax.axvline(b, color="red", linestyle="--", label=f"b = {b}")

ax.set_title("Kakuritukukan")
ax.set_xlabel("X")
ax.set_ylabel("Mitudo")
ax.legend()
ax.grid(True)

st.pyplot(fig)
