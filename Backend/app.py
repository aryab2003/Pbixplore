import streamlit as st
import zipfile
import json
import io
from Model import process_json_data  # Ensure you have this function implemented

pages_data = []

def extract_layout_from_pbix(pbix_bytes):
    with zipfile.ZipFile(io.BytesIO(pbix_bytes)) as z:
        try:
            with z.open('Report/Layout') as layout_file:
                layout_bytes = layout_file.read()
                layout_json_str = layout_bytes.decode('utf-16')
                layout_json = json.loads(layout_json_str)
                return layout_json
        except KeyError:
            st.error("Layout file not found inside PBIX.")
            return None

st.title("📊 Power BI Report Details Viewer")

uploaded_file = st.file_uploader("Upload a PBIX file", type=["pbix"])

if uploaded_file:
    pbix_bytes = uploaded_file.read()
    layout_data = extract_layout_from_pbix(pbix_bytes)

    if layout_data:
        config_json = json.loads(layout_data.get("config", "{}"))
        base_theme = config_json.get("themeCollection", {}).get("baseTheme", {}).get("name", "Unknown")
        version = config_json.get("version", "Unknown")

        st.header("📁 Report Metadata")
        st.markdown(f"- **Report Theme:** `{base_theme}`")
        st.markdown(f"- **Report Version:** `{version}`")

        sections = layout_data.get("sections", [])
        st.header(f"📄 Report Pages: {len(sections)} page(s)")

        page_names = [f"Page {i+1}: {page.get('displayName', f'Page {i+1}')}" for i, page in enumerate(sections)]
        selected_page = st.selectbox("📄 Select a Page to Analyze", page_names)

        # Extract selected page index and data
        selected_index = page_names.index(selected_page)
        page = sections[selected_index]

        st.subheader(f"📘 {selected_page}")

        page_data = {
            "page_number": selected_index + 1,
            "page_name": page.get("displayName", f"Page {selected_index+1}"),
            "visuals": []
        }

        visuals = page.get("visualContainers", [])
        st.markdown(f"- **Visuals on this page:** {len(visuals)}")

        for j, visual in enumerate(visuals):
            st.markdown(f"#### 🔲 Visual {j+1}")

            visual_data = {
                "visual_number": j + 1,
                "position": {
                    "x": visual.get("x"),
                    "y": visual.get("y"),
                    "width": visual.get("width"),
                    "height": visual.get("height")
                },
                "visual_type": "Unknown",
                "projections": {},
                "query_fields": []
            }

            x = visual.get("x")
            y = visual.get("y")
            width = visual.get("width")
            height = visual.get("height")
            st.markdown(f"- 📐 **Position:** (x: `{x}`, y: `{y}`), **Size:** `{width} x {height}`")

            config_str = visual.get("config", "{}")
            try:
                config = json.loads(config_str)
                visual_data["visual_type"] = config.get("singleVisual", {}).get("visualType", "Unknown")
                projections = config.get("singleVisual", {}).get("projections", {})
                for role, items in projections.items():
                    visual_data["projections"][role] = [item.get("queryRef", "Unknown") for item in items]
                visual_type = config.get("singleVisual", {}).get("visualType", "Unknown")
                st.markdown(f"- 📊 **Visual Type:** `{visual_type}`")

                for role, items in projections.items():
                    field_names = [item.get("queryRef", "Unknown") for item in items]
                    st.markdown(f"  - 🎯 **{role} Fields:** {', '.join(field_names)}")
            except Exception as e:
                st.markdown(f"- ⚠️ Could not parse config: {e}")

            query_str = visual.get("query", "{}")
            try:
                query = json.loads(query_str)
                commands = query.get("Commands", [])
                for cmd in commands:
                    sem_query = cmd.get("SemanticQueryDataShapeCommand", {}).get("Query", {})
                    selects = sem_query.get("Select", [])
                    select_fields = []
                    for sel in selects:
                        if "Name" in sel:
                            visual_data["query_fields"].append(sel["Name"])
                            select_fields.append(sel["Name"])
                    if select_fields:
                        st.markdown(f"- 🧮 **Query Fields:** {', '.join(select_fields)}")
            except:
                pass

            page_data["visuals"].append(visual_data)

        pages_data.append(page_data)
        process_json_data(pages_data)  # You can adapt this to only save/export selected page if needed
