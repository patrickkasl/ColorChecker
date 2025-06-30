# ColorChecker 🎨

An advanced Python tool for automatic color detection and classification in images with 89.5% accuracy.

## 📋 Overview

ColorChecker is an intelligent system that detects and classifies dominant colors in images according to a predefined color set. It uses machine learning (K-means clustering) combined with heuristic rules for optimal color recognition.

## ✨ Features

- **Automatic color detection**: Identifies the 3 dominant colors in each image
- **High accuracy**: 89.5% accurate color classification
- **Batch processing**: Processes multiple images simultaneously
- **Excel export**: Generates structured results in Excel format
- **Intelligent heuristics**: Advanced rules for color distinction
- **LAB color space**: Uses LAB color space for better color comparison

## 🎯 Supported Colors

The system recognizes the following colors (in Dutch):
- **Zwart** (Black) - (0, 0, 0)
- **Paars** (Purple) - (128, 0, 128)
- **Geel** (Yellow) - (255, 223, 0)
- **Roze** (Pink) - (255, 105, 180)
- **Oranje** (Orange) - (255, 140, 0)
- **Wit** (White) - (255, 255, 255)
- **Groen** (Green) - (90, 160, 90)
- **Blauw** (Blue) - (0, 102, 204)
- **Rood** (Red) - (200, 30, 30)
- **Goud** (Gold) - (212, 175, 55)
- **Bruin** (Brown) - (150, 75, 0)

## 🚀 Installation

### Requirements
- Python 3.7+
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/[username]/ColorChecker.git
   cd ColorChecker
   ```

2. **Create and activate virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**
   ```bash
   mkdir images
   mkdir results
   ```

## 📦 Dependencies

The project uses only essential packages for optimal performance:

```
Pillow==11.2.1        # Image processing
numpy==2.3.1          # Numerical computations
scikit-learn==1.7.0   # K-means clustering
scikit-image==0.25.2  # LAB color space conversion
openpyxl==3.1.5       # Excel file generation
```

## 🖼️ Usage

### Basic Usage

1. **Place images** in the `images/` directory
   - Supported formats: JPG, JPEG, PNG, WebP

2. **Start color detection**
   ```bash
   python main.py
   ```

3. **View results** in `results/color_labels.xlsx`

### Configuration

Adjust the following parameters in `main.py`:

```python
IMAGE_DIR = "images"                    # Input directory
OUTPUT_FILE = "results/color_labels.xlsx"  # Output file
MIN_PERCENTAGE = 0.025                  # Minimum color percentage (2.5%)
```

## 🔧 Technical Details

### Algorithm

1. **Image Preprocessing**: Images are scaled to 100x100 pixels for consistent processing
2. **K-means Clustering**: Divides pixels into 5 color clusters
3. **Heuristic Rules**: Specific rules for color distinction
4. **LAB Color Space**: Accurate color comparison in LAB space
5. **Percentage Calculation**: Calculates color percentages per cluster

### Heuristic Rules

The system uses advanced heuristics for:
- **Red detection**: Distinguishes dark red from other colors
- **Yellow detection**: Recognizes yellow tints with RGB analysis
- **Brown detection**: Identifies brown tints
- **Green detection**: Distinguishes green from other colors
- **Orange detection**: Recognizes orange tints
- **Blue detection**: Identifies blue tints

## 📊 Output Format

The system generates an Excel file with the following columns:
- **Filename**: Name of the image
- **Color 1**: Dominant color (highest percentage)
- **Color 2**: Second dominant color
- **Color 3**: Third dominant color

## 📁 Project Structure

```
ColorChecker/
├── main.py              # Main script
├── images/              # Input images
├── results/             # Output files
│   └── color_labels.xlsx
├── requirements.txt     # Minimal dependencies
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Reporting Issues

If you encounter bugs or have suggestions, please open an [issue](https://github.com/patrickkasl/ColorChecker/issues) on GitHub.

## 📈 Performance

- **Accuracy**: 89.5%
- **Processing speed**: ~1-2 seconds per image (depending on size)
- **Supported formats**: JPG, JPEG, PNG, WebP
- **Maximum image size**: No limit (automatic scaling)
- **Memory efficient**: Minimal dependencies for fast installation

---

**Made with by Patrick Kasl** 