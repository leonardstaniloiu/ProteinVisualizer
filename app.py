import streamlit as st
import py3Dmol
from Bio.PDB import PDBParser
from io import StringIO

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

st.title("Protein Visualizer")
st.header("Upload a Protein Structure File")
st.info("Supported formats: PDB")

uploaded_file = st.file_uploader("Choose a PDB file", type=["pdb"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")

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

