import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

def draw_box(ax, x, y, w, h, text, color='#4A90D9', textcolor='white', fontsize=9):
    box = mpatches.FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.1", linewidth=1.5,
        edgecolor='#2c3e50', facecolor=color)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color=textcolor, fontweight='bold')

def draw_arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.1, my, label, fontsize=7, color='#e74c3c', fontweight='bold')

draw_box(ax, 5.5, 8.5, 3, 0.7, 'Customer Query', '#2c3e50')
draw_box(ax, 5.5, 7.2, 3, 0.7, 'Intent Classification', '#8e44ad')
draw_box(ax, 0.2, 5.5, 2.2, 0.7, 'Sales Agent', '#27ae60')
draw_box(ax, 2.6, 5.5, 2.2, 0.7, 'Technical Agent', '#27ae60')
draw_box(ax, 5.0, 5.5, 2.2, 0.7, 'Billing Agent', '#27ae60')
draw_box(ax, 7.4, 5.5, 2.2, 0.7, 'Account Agent', '#27ae60')
draw_box(ax, 9.8, 5.5, 2.2, 0.7, 'Memory Agent', '#16a085')
draw_box(ax, 5.5, 4.0, 3, 0.7, 'Human Approval\n(High Risk Only)', '#e74c3c')
draw_box(ax, 5.5, 2.7, 3, 0.7, 'Supervisor Agent', '#d35400')
draw_box(ax, 5.5, 1.4, 3, 0.7, 'Final Response', '#2980b9')
draw_box(ax, 5.5, 0.2, 3, 0.7, 'SQLite Memory Storage', '#7f8c8d')

draw_arrow(ax, 7, 8.5, 7, 7.9)
draw_arrow(ax, 6.5, 7.2, 1.3, 6.2, 'Sales')
draw_arrow(ax, 6.8, 7.2, 3.7, 6.2, 'Tech')
draw_arrow(ax, 7.0, 7.2, 6.1, 6.2, 'Billing')
draw_arrow(ax, 7.2, 7.2, 8.5, 6.2, 'Account')
draw_arrow(ax, 7.5, 7.2, 10.9, 6.2, 'Memory')
draw_arrow(ax, 6.1, 5.5, 6.5, 4.7, 'Refund/Cancel')
draw_arrow(ax, 1.3, 5.5, 6.0, 4.7)
draw_arrow(ax, 3.7, 5.5, 6.2, 4.7)
draw_arrow(ax, 8.5, 5.5, 7.8, 4.7)
draw_arrow(ax, 7, 4.0, 7, 3.4)
draw_arrow(ax, 10.9, 5.5, 8.5, 3.4)
draw_arrow(ax, 7, 2.7, 7, 2.1)
draw_arrow(ax, 7, 1.4, 7, 0.9)

ax.set_title('LangGraph Customer Support Automation - Workflow Diagram',
             fontsize=13, fontweight='bold', color='#2c3e50', pad=15)

plt.tight_layout()
plt.savefig('workflow_diagram.png', dpi=150, bbox_inches='tight')
print("Diagram saved as workflow_diagram.png!")
plt.show()