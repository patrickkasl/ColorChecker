import os
from PIL import Image, ImageFile
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab
from collections import Counter
from openpyxl import Workbook

### Color Detection and Labeling Script with currently a 89,5% accuracy rate

# Allow truncated image files
ImageFile.LOAD_TRUNCATED_IMAGES = True

# === CONFIGURATION ===
IMAGE_DIR = "images"
OUTPUT_FILE = "results/color_labels.xlsx"
MIN_PERCENTAGE = 0.025  # Lower threshold for detecting smaller color areas

# Allowed colors (in Dutch, keep as-is unless needed)
allowed_colors = {
    "Zwart": (0, 0, 0),
    "Paars": (128, 0, 128),
    "Geel": (255, 223, 0),
    "Roze": (255, 105, 180),
    "Oranje": (255, 140, 0),
    "Wit": (255, 255, 255),
    "Groen": (90, 160, 90),
    "Blauw": (0, 102, 204),
    "Rood": (200, 30, 30),
    "Goud": (212, 175, 55),
    "Bruin": (150, 75, 0),
}


# === COLOR CONVERSION UTILITIES ===
def rgb_to_lab(rgb):
    rgb_norm = np.array(rgb).reshape(1, 1, 3) / 255.0
    return rgb2lab(rgb_norm)[0][0]


def lab_distance(c1, c2):
    return np.linalg.norm(c1 - c2)


# === HEURISTICS ===
def is_dark_red(rgb):
    r, g, b = rgb
    if r < 100:
        return False
    red_dominance = r - max(g, b)
    gold_like = g > 100 > b and r - g < 80
    return red_dominance > 50 and not gold_like


def is_likely_yellow(rgb):
    r, g, b = rgb
    return r > 200 and g > 200 and b < 100 and abs(r - g) < 40 and b < min(r, g) - 100


def is_likely_brown(rgb):
    r, g, b = rgb
    return r > 100 > (r - g) and g > 50 > b and (g - b) > 20


def is_likely_green(rgb):
    r, g, b = rgb
    return g > 100 and g > r + 20 and g > b + 20 and abs(r - b) < 50


def is_likely_orange(rgb):
    r, g, b = rgb
    return r > 200 and 100 < g < 180 and b < 80 and (r - g) < 100 and (g - b) > 30


def is_likely_blue(rgb):
    r, g, b = rgb
    return b > 100 and b > r + 30 and b > g + 30


def is_not_silver(rgb):
    r, g, b = rgb
    if max(abs(r - g), abs(g - b), abs(r - b)) > 15:
        return True
    if min(r, g, b) < 150:
        return True
    if b > r + 10 and b > g + 10:
        return True
    return False


# === MAPPING FUNCTION ===
def map_to_allowed_color(rgb):
    if is_likely_orange(rgb):
        print(f"🟠 Orange heuristic: {rgb}")
        return "Oranje"
    if is_dark_red(rgb):
        print(f"🔴 Red heuristic: {rgb}")
        return "Rood"
    if is_likely_brown(rgb):
        print(f"🟤 Brown heuristic: {rgb}")
        return "Bruin"
    if is_likely_green(rgb):
        print(f"🟢 Green heuristic: {rgb}")
        return "Groen"
    if is_likely_yellow(rgb):
        print(f"🟡 Yellow heuristic: {rgb}")
        return "Geel"
    if is_likely_blue(rgb):
        print(f"🔵 Blue heuristic: {rgb}")
        return "Blauw"

    # Fallback to LAB color distance
    exclude_silver = is_not_silver(rgb)
    lab = rgb_to_lab(rgb)

    def distance(item):
        color_name, color_rgb = item
        if exclude_silver and color_name == "Zilver":
            return float("inf")
        return lab_distance(lab, rgb_to_lab(color_rgb))

    best_match = min(allowed_colors.items(), key=distance)
    print(f"🎨 RGB {rgb} → {best_match[0]}")
    return best_match[0]


# === MAIN COLOR DETECTION ===
def detect_dominant_colors(image_path, n_clusters=5):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((100, 100))
    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pixels)
    cluster_centers = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    print(f"\n📷 {os.path.basename(image_path)} – Detected colors:")
    for i, color in enumerate(cluster_centers, 1):
        print(f"{i}. {tuple(color)}")

    cluster_counts = Counter(labels)
    total_pixels = len(pixels)

    color_percentages = []
    for idx, count in cluster_counts.items():
        percentage = count / total_pixels
        rgb = tuple(cluster_centers[idx])
        color_name = map_to_allowed_color(rgb)
        if color_name != "Wit" and percentage >= MIN_PERCENTAGE:
            if color_name == "Zwart" and percentage < 0.08:
                continue  # Suppress black under threshold
            color_percentages.append((color_name, percentage))

    # Combine percentages of same color
    combined = {}
    for color, perc in color_percentages:
        combined[color] = combined.get(color, 0) + perc

    sorted_colors = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return [color for color, perc in sorted_colors[:3]]


# === BATCH PROCESSOR ===
def process_image_directory(image_dir, output_file):
    files = sorted(f for f in os.listdir(image_dir)
                   if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))

    wb = Workbook()
    ws = wb.active
    ws.title = "Colors"
    ws.append(["Filename", "Color 1", "Color 2", "Color 3"])

    for filename in files:
        path = os.path.join(image_dir, filename)
        try:
            colors = detect_dominant_colors(path)
            colors += [""] * (3 - len(colors))  # Fill empty cells
            ws.append([filename] + colors)
        except Exception as e:
            ws.append([filename, f"[ERROR] {e}"])
            print(f"❌ Error processing {filename}: {e}")

    wb.save(output_file)
    print(f"\n✅ Excel file saved as: {output_file}")


# === MAIN EXECUTION ===
if __name__ == "__main__":
    process_image_directory(IMAGE_DIR, OUTPUT_FILE)
