# 🧬 Protein Visualizer

An interactive web application for visualizing and analyzing protein structures in PDB format. Built with Streamlit and py3Dmol for 3D molecular visualization.

## ✨ Features

- 📤 **Easy Upload**: Simply drag and drop your PDB files
- 🎨 **Multiple Visualization Styles**: 
  - Cartoon
  - Stick
  - Sphere
  - Surface
- 🌈 **Color Schemes**:
  - Chain-based coloring
  - Secondary structure (PyMOL style)
  - Element-based
  - Hydrophobicity
  - B-factor
  - Spectrum
  - Rainbow
- 📊 **Structural Statistics**:
  - Total atoms count
  - Number of residues
  - Chain information and lengths
  - Ligand detection
  - Water molecule count
- 🖱️ **Interactive Controls**: Rotate, zoom, and explore your protein structure in 3D

## 🚀 Demo

Try the live demo: [Protein Visualizer on Streamlit Cloud]([[https://proteinvisualizer.streamlit.app](https://proteinview.streamlit.app/)][(https://proteinview.streamlit.app/](https://proteinview.streamlit.app/)))

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/leonardstaniloiu/proteinvisualizer.git
cd proteinvisualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

- `streamlit` - Web application framework
- `py3Dmol` - 3D molecular visualization library
- `biopython` - Biological computation tools for parsing PDB files
