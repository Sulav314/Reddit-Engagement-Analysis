"""Re-makes Figures 1 to 5 from the CSV files in data/.
Run it from anywhere: analysis.py/all_figures_data_to_figure
The files are saved in the figures/ folder."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

# Same colors in Figure 1 and Figure 2
COLORS = {
    "General Art": "#6b7280",  # dark grey
    "Fandom": "#d97706",  # gold
    "Regional/cultural": "#059669",  # green
    "Data/chart": "#2563eb",  # blue
    "Other": "#9ca3af",  # light grey
}
LEGEND = {
    "General Art": "General Art subs",
    "Fandom": "Fandom subs",
    "Regional/cultural": "Regional/cultural subs",
    "Data/chart": "Data/chart subs",
    "Other": "Other",
}

with open(DATA / "posts_24h.csv", newline="", encoding="utf-8") as f:
    posts = list(csv.DictReader(f))
with open(DATA / "readings_over_time.csv", newline="", encoding="utf-8") as f:
    readings = list(csv.DictReader(f))


def series(post, sub, metric, max_hours=None):
    """(hours, value) pairs for one post and one metric, in time order."""
    pts = [
        (float(r["hours"]), float(r["value"]))
        for r in readings
        if r["post"] == post and r["subreddit"] == sub and r["metric"] == metric
    ]
    if max_hours is not None:
        pts = [p for p in pts if p[0] <= max_hours]
    return sorted(pts)


def clean(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


# Figures 1 and 2: one bar per post
def bar_figure(column, xlabel, title, xmax, ticks, filename):
    fig, ax = plt.subplots(figsize=(10, 8.5))
    ys = list(range(len(posts)))
    values = [float(p[column]) for p in posts]
    colors = [COLORS[p["community_type"]] for p in posts]
    ax.barh(ys, [min(v, xmax) for v in values], color=colors, height=0.72)
    for y, v in zip(ys, values):
        if v > xmax:  # the bar is cut off
            for dx in (1.6, 0.9):
                ax.plot([xmax - dx, xmax - dx + 0.5], [y + 0.3, y - 0.3], color="white", lw=2)
            ax.text(xmax + 0.3, y, f"{v:.1f} (cut off)", va="center", fontsize=8)
        else:
            ax.text(v + 0.3, y, f"{v:.1f}", va="center", fontsize=8)
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{p['post']} · {p['subreddit']}" for p in posts], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, xmax * 1.18)
    ax.set_xticks(ticks)
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left", fontweight="bold", fontsize=11)
    ax.grid(axis="x", color="#e5e7eb")
    ax.set_axisbelow(True)
    clean(ax)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COLORS.values()]
    ax.legend(handles, LEGEND.values(), loc="lower right", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=150)
    plt.close(fig)


# Figure 3: The r/ClashRoyale post
def figure3():
    post, sub = "Clash Royale audio meme", "r/ClashRoyale"
    views, ups, coms = (series(post, sub, m) for m in ("views", "upvotes", "comments"))
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax2 = ax.twinx()
    ax.plot([h for h, _ in views], [v / 1000 for _, v in views], "-o", ms=3, lw=2,
            color="#2563eb", label="Views (left axis, thousands)")
    ax2.plot([h for h, _ in ups], [v for _, v in ups], "-o", ms=3, lw=2,
             color="#d97706", label="Upvotes (right axis)")
    ax2.plot([h for h, _ in coms], [v for _, v in coms], "-o", ms=3, lw=2,
             color="#059669", label="Comments (right axis)")
    ax.set_ylim(0, 35)
    ax2.set_ylim(0, 210)
    ax.set_xlim(0, 28)
    ax.set_xticks(range(0, 29, 4))
    ax.set_xlabel("Hours since posting")
    ax.set_ylabel("Views (thousands)", color="#2563eb")
    ax2.set_ylabel("Upvotes and comments")
    ax.grid(axis="y", color="#e5e7eb")
    ax.set_axisbelow(True)
    ax.set_title("r/ClashRoyale post: views, upvotes and comments over 28 hours",
                 loc="left", fontweight="bold", fontsize=11)
    lines = ax.get_lines() + ax2.get_lines()
    ax.legend(lines, [l.get_label() for l in lines], loc="upper left", frameon=False)
    ax2.spines["top"].set_visible(False)
    ax.spines["top"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_clash_royale_growth.png", dpi=150)
    plt.close(fig)


# Figure 4: views of 11 posts
FIG4 = [
    ("Childhood Pokémon drawings", "r/pokemon", "#e4572e"),
    ("Mini Pekka sketch", "r/NepalSocial", "#17a398"),
    ("Dexter sketch (Jan 16)", "r/Dexter", "#9b5de5"),
    ("Angel Batista sketch", "r/Dexter", "#f2a900"),
    ("Technoblade drawings", "r/Minecraft", "#2d7dd2"),
    ("Clash Royale audio meme", "r/ClashRoyale", "#d81159"),
    ("Willem Dafoe sketch", "r/learntodraw", "#6a994e"),
    ("Willem Dafoe sketch", "r/sketches", "#8c5e3c"),
    ("Willem Dafoe sketch", "r/Sketch", "#00b4d8"),
    ("Brian Moser sketch", "r/Dexter", "#e07be0"),
    ("Dexter sketch (Jan 15)", "r/Dexter", "#8d99ae"),
]


def figure4():
    fig, ax = plt.subplots(figsize=(11, 6))
    for post, sub, color in FIG4:
        pts = [(0.0, 0.0)] + series(post, sub, "views", max_hours=28)  # every line starts at 0
        ax.plot([h for h, _ in pts], [v / 1000 for _, v in pts], "-o", ms=3, lw=1.8,
                color=color, label=f"{post} ({sub})")
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 35)
    ax.set_xticks(range(0, 29, 4))
    ax.set_xlabel("Hours since posting")
    ax.set_ylabel("Views (thousands)")
    ax.grid(axis="y", color="#e5e7eb")
    ax.set_axisbelow(True)
    clean(ax)
    ax.set_title("Views of 11 posts, from the time of posting to the reading closest to 24 hours",
                 loc="left", fontweight="bold", fontsize=11)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig4_views_of_11_posts.png", dpi=150)
    plt.close(fig)


# Figure 5:The Batista sketch through 5 days
def figure5():
    post, sub = "Angel Batista sketch", "r/Dexter"
    views = series(post, sub, "views")
    ups = series(post, sub, "upvotes")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax2 = ax.twinx()
    ax.plot([h / 24 for h, _ in views], [v / 1000 for _, v in views], "-o", ms=4, lw=2.2, color="#2563eb")
    ax2.plot([h / 24 for h, _ in ups], [v for _, v in ups], "-o", ms=4, lw=2.2, color="#dc2626")
    ax.set_ylim(0, 35)
    ax2.set_ylim(0, 1050)
    ax.set_xlim(0, 5)
    ax.set_xlabel("Days since posting (the readings on day 5 have no recorded time; drawn at 5 days)")
    ax.set_ylabel("Views (thousands)", color="#2563eb")
    ax2.set_ylabel("Upvotes", color="#dc2626")
    ax.grid(axis="y", color="#e5e7eb")
    ax.set_axisbelow(True)
    ax.set_title("Angel Batista sketch on r/Dexter: views and upvotes through 5 days",
                 loc="left", fontweight="bold", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig5_batista_five_days.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    bar_figure("upvotes_per_1000_views", "Upvotes per 1,000 views (reading closest to 24 hours)",
               "Upvotes per 1,000 views, by post and subreddit", 30, range(0, 31, 5),
               "fig1_upvotes_per_1000_views.png")
    bar_figure("comments_per_1000_views", "Comments per 1,000 views (reading closest to 24 hours)",
               "Comments per 1,000 views, by post and subreddit", 18, range(0, 19, 3),
               "fig2_comments_per_1000_views.png")
    figure3()
    figure4()
    figure5()
    print("Figures saved in", OUT)
