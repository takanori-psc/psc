import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.colors as mcolors

def create_rack_secure_domain_diagram():
    fig, ax = plt.subplots(figsize=(10, 10))

    # 背景設定
    fig.patch.set_facecolor('#f9f9f9')
    ax.set_facecolor('#ffffff')
    ax.axis('off')

    # --- 定数 ---
    Y_CPU_LINE = 7.0
    Y_MEM_LINE = 5.5
    Y_BOUNDARY = 4.5
    Y_BOTTOM_LABEL = 3.0

    BOX_WIDTH = 1.0
    GAP = 0.15

    # --- ヘルパー：ラック枠描画 ---
    def draw_rack_box(x_start, y_start, label, color, border_color='#000000'):
        # 枠の描画
        rect = patches.Rectangle((x_start - 0.6, y_start - 0.8),
                                 BOX_WIDTH + 1.2, 2.0,
                                 linewidth=3, edgecolor=border_color, facecolor=color,
                                 hatch=None, transform=ax.transData)
        ax.add_patch(rect)

        # ラベル
        ax.text(x_start, y_start + 0.5, label,
                ha='center', va='center', fontsize=18, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=color, edgecolor='white', alpha=0.7))
        return rect

    # --- ヘルパー：ノード描画 ---
    def draw_node(x, y, label, font_color='black'):
        ax.text(x, y, label, ha='center', va='center', fontsize=14, fontweight='bold', color=font_color)

    # --- ヘルパー：接続線描画 ---
    def draw_line(x1, y1, x2, y2, is_dashed=False):
        ax.plot([x1, x2], [y1, y2], color='#333', linewidth=2, linestyle='solid' if not is_dashed else 'dashed')

    # ====================
    # 1. Rack A 描画
    # ====================
    draw_rack_box(-2.5, 8.5, 'Rack A', '#e0f7fa', border_color='#006064')

    # CPU Row (横直結)
    for i in range(3):
        draw_node(-2.5 + (i * (BOX_WIDTH + GAP)), Y_CPU_LINE, f'CPU{i}')
        # 横の太線 (Fast Domain)
        if i < 2:
            draw_line(-2.5 + i*(BOX_WIDTH+GAP), Y_CPU_LINE,
                      -2.5 + (i+1)*(BOX_WIDTH+GAP), Y_CPU_LINE,
                      is_dashed=False, linewidth=3)

    # Resource Row (縦接続)
    for i in range(3):
        draw_node(-2.5 + (i * (BOX_WIDTH + GAP)), Y_MEM_LINE, f'{"MEM0" if i==0 else "GPU1" if i==1 else "STO2"}')
        # 縦の線
        draw_line(-2.5 + i*(BOX_WIDTH+GAP), Y_CPU_LINE,
                  -2.5 + i*(BOX_WIDTH+GAP), Y_MEM_LINE)

    # Rack A 下部注釈
    ax.text(-2.5, 4.0, '← Rack-local Secure Fast Domain →',
            fontsize=12, fontweight='bold', color='#006064',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#e0f7fa', edgecolor='#006064', alpha=0.5))

    # 条件リスト (左下)
    ax.text(-2.8, 3.5, '※ 条件', fontsize=11, fontweight='bold', color='#555')
    ax.text(-2.8, 3.2, '- single-hop only', fontsize=10, color='#555')
    ax.text(-2.8, 2.9, '- no switch (Rack 内)', fontsize=10, color='#555')
    ax.text(-2.8, 2.6, '- no boundary node', fontsize=10, color='#555')

    # ====================
    # 2. Boundary (Switch) 描画
    # ====================
    # 赤い境界線 (Switch)
    # 幅を広くして Rack 間の隙間を埋めるように
    boundary_rect = patches.Rectangle((-3.3, 4.5),
                                       6.6, 0.1,
                                       linewidth=4, edgecolor='#c62828', facecolor='#ffebee',
                                       hatch='///', transform=ax.transData) # 点線風またはハッチで表現
    ax.add_patch(boundary_rect)

    # 赤い四角（Switch 本体）
    ax.add_patch(patches.Rectangle((-3.0, 4.5), 0.1, 0.1, color='#c62828'))
    ax.add_patch(patches.Rectangle((2.8, 4.5), 0.1, 0.1, color='#c62828'))

    ax.text(0, 5.0, 'Boundary (Switch)',
            fontsize=14, fontweight='bold', color='#c62828',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffebee', edgecolor='#c62828', alpha=0.8))

    # 警告注釈
    ax.text(-1.5, 2.5, '※ Rack 間通信：必ず PSC 通常制御（Fast Mode 禁止）',
            fontsize=11, color='#c62828', fontweight='bold')

    # ====================
    # 3. Rack B 描画
    # ====================
    draw_rack_box(2.5, 8.5, 'Rack B', '#e0f7fa', border_color='#006064')

    # CPU Row (横直結) - 2 つのみ
    for i in range(2):
        draw_node(2.5 + (i * (BOX_WIDTH + GAP)), Y_CPU_LINE, f'CPU{3+i}')
        # 横の太線 (Fast Domain)
        if i < 1:
            draw_line(2.5 + i*(BOX_WIDTH+GAP), Y_CPU_LINE,
                      2.5 + (i+1)*(BOX_WIDTH+GAP), Y_CPU_LINE,
                      is_dashed=False, linewidth=3)

    # Resource Row (縦接続)
    for i in range(2):
        draw_node(2.5 + (i * (BOX_WIDTH + GAP)), Y_MEM_LINE, f'{"MEM3" if i==0 else "GPU4"}')
        # 縦の線
        draw_line(2.5 + i*(BOX_WIDTH+GAP), Y_CPU_LINE,
                  2.5 + i*(BOX_WIDTH+GAP), Y_MEM_LINE)

    # ====================
    # 4. 全体注釈と凡例
    # ====================
    ax.text(7, 5, '■ 図のポイント', fontsize=14, fontweight='bold')
    ax.text(7, 4.5, '- 横：CPU 直結（Fast Domain）', fontsize=11)
    ax.text(7, 4.2, '- 縦：リソース接続', fontsize=11)
    ax.text(7, 3.9, '- 下：Boundary で完全分離', fontsize=11)
    ax.text(7, 3.6, '- Rack 間：絶対に Fast 禁止', fontsize=11)

    ax.text(7, 3.2, '■ 色ルール', fontsize=12, fontweight='bold')
    ax.text(7, 2.9, '- CALM/Fast: 青/緑', fontsize=10)
    ax.text(7, 2.7, '- EMERGENCY/Boundary: 赤', fontsize=10)

    # 凡例ボックス
    ax.text(-3.3, -0.2, '■ 凡例', fontsize=12, fontweight='bold', transform=ax.transData)
    ax.text(-3.0, -0.5, '■ 太線 (Solid): Fast Domain (Rack 内)', fontsize=10, transform=ax.transData)
    ax.text(-2.6, -0.8, '■ 点線/ハッチ: Boundary (Switch)', fontsize=10, transform=ax.transData)
    ax.text(-2.2, -1.1, '■ 青/緑: 安定領域', fontsize=10, transform=ax.transData)
    ax.text(-1.8, -1.4, '■ 赤: 制御・分離境界', fontsize=10, transform=ax.transData)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    create_rack_secure_domain_diagram()
