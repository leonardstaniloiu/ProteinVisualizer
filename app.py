import streamlit as st
import py3Dmol
from Bio.PDB import PDBParser
from io import StringIO

def load_example(path):
    with open(path, "r") as f:
        return f.read()
    

def view_function(file_content, style="cartoon", color_scheme="chain"):
    viewer = py3Dmol.view(width=800, height=600)
    viewer.addModel(file_content, "pdb")

    if style == "cartoon":
        viewer.setStyle({"cartoon": {"colorscheme": color_scheme}})
    elif style == "stick":
        viewer.setStyle({"stick": {"colorscheme": color_scheme}})
    elif style == "sphere":
        viewer.setStyle({"sphere": {"colorscheme": color_scheme}})
    viewer.zoomTo()
    st.components.v1.html(viewer._make_html(), height=600)


def get_basic_stats(pdb_content: str):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", StringIO(pdb_content))

    atoms = 0
    residues = 0
    chains = set()
    ligands = set()
    waters = 0

    for model in structure:
        for chain in model:
            chains.add(chain.id)
            for residue in chain:
                resname = residue.get_resname()

                if resname == "HOH":
                    waters += 1
                    continue

                if residue.id[0] != " ":
                    ligands.add(resname)
                else:
                    residues += 1

                atoms += len(residue)

    chain_lengths = {}
    for model in structure:
        for chain in model:
            chain_lengths[chain.id] = sum(
                1 for r in chain if r.id[0] == " "
            )

    return {
        "atoms": atoms,
        "residues": residues,
        "chains": sorted(chains),
        "nr_chains": len(chains),
        "chain_lengths": chain_lengths,
        "ligands": sorted(ligands),
        "nr_ligands": len(ligands),
        "waters": waters,
        "models": len(structure)
    }

st.set_page_config(
    page_title="Protein Visualizer",
    page_icon="🧬",
    layout="centered"
)

color_options = [
    "chain",
    "ssPyMol",
    "element",
    "hydrophobicity",
    "bfactor",
    "spectrum",
    "rainbow"
]

style_options = [
    "cartoon",
    "stick",
    "sphere",
    "surface"
]

# Styling
st.markdown("""<style>
    .title-gradient {            
        background: radial-gradient(circle, #ff6b6b 0%, #feca57 33%, #48dbfb 66%, #1dd1a1 100%);
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-fill-color: transparent;
        font-size: 42px;
        font-weight: 900;
        font-family: Arial, sans-serif;
      
    }
    """, unsafe_allow_html=True)
#  End styling

st.html(
    "<h1 class='title-gradient'>Protein Structure Visualizer</h1>"
    "<br><br>"
)
st.info("Supported formats: PDB")

uploaded_file = st.file_uploader("Choose a PDB file", type=["pdb"])
if st.button("Load an example structure (1BNA)"):
    try:
        file_content = load_example("1BNA.pdb")
        st.session_state.example_loaded = True
        st.session_state.file_content = file_content
    except FileNotFoundError:
        st.error("File 1BNA.pdb not found.")


file_content = None
if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
elif "file_content" in st.session_state and st.session_state.get("example_loaded"):
    file_content = st.session_state.file_content

if file_content is not None:

    selected_style = st.selectbox("Select visualization style", style_options)
    selected_color = st.selectbox("Select color scheme", color_options)

    st.info(
        "Use mouse left button to rotate and mouse right button or scroll to zoom."
    )

    view_function(file_content, style=selected_style, color_scheme=selected_color)

    stats = get_basic_stats(file_content)
    st.subheader("Protein Structure Statistics")
    st.markdown(f"**Number of Atoms:** {stats['atoms']}")
    st.markdown(f"**Number of Residues:** {stats['residues']}")
    st.markdown(f"**Number of Chains:** {stats['nr_chains']}")
    for chain_id, length in stats['chain_lengths'].items():
        st.markdown(f"  - Chain {chain_id}: {length} residues")
    st.markdown(f"**Number of Ligands:** {stats['nr_ligands']}")
    if stats['nr_ligands'] > 0:
        st.markdown(f"  - Ligands: {', '.join(stats['ligands'])}")
    st.markdown(f"**Number of Water Molecules:** {stats['waters']}")

