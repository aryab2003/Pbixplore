import streamlit as st
import json

# Load the parsed layout file
with open("C:/Users/admin/Desktop/Pbixplore/jsonformatter.txt", "r", encoding="utf-8") as f:
    layout_data = json.load(f)

st.title("📊 Power BI Report Details Viewer")

# --- Report-level details ---
config_json = json.loads(layout_data.get("config", "{}"))
base_theme = config_json.get("themeCollection", {}).get("baseTheme", {}).get("name", "Unknown")
version = config_json.get("version", "Unknown")

st.header("📁 Report Metadata")
st.markdown(f"- **Report Theme:** `{base_theme}`")
st.markdown(f"- **Report Version:** `{version}`")

# --- Pages and Visuals ---
sections = layout_data.get("sections", [])
st.header(f"📄 Report Pages: {len(sections)} page(s)")

for i, page in enumerate(sections):
    page_name = page.get("displayName", f"Page {i+1}")
    st.subheader(f"📘 Page {i+1}: {page_name}")
    
    visuals = page.get("visualContainers", [])
    st.markdown(f"- **Visuals on this page:** {len(visuals)}")

    for j, visual in enumerate(visuals):
        st.markdown(f"#### 🔲 Visual {j+1}")

        # Extract layout position
        x = visual.get("x")
        y = visual.get("y")
        width = visual.get("width")
        height = visual.get("height")
        st.markdown(f"- 📐 **Position:** (x: `{x}`, y: `{y}`), **Size:** `{width} x {height}`")

        # Extract visual type and config details
        config_str = visual.get("config", "{}")
        try:
            config = json.loads(config_str)
            visual_type = config.get("singleVisual", {}).get("visualType", "Unknown")
            st.markdown(f"- 📊 **Visual Type:** `{visual_type}`")

            # Extract projections (fields/columns used)
            projections = config.get("singleVisual", {}).get("projections", {})
            for role, items in projections.items():
                field_names = [item.get("queryRef", "Unknown") for item in items]
                st.markdown(f"  - 🎯 **{role} Fields:** {', '.join(field_names)}")
        except Exception as e:
            st.markdown(f"- ⚠️ Could not parse config: {e}")

        # Extract query columns (optional)
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
                        select_fields.append(sel["Name"])
                if select_fields:
                    st.markdown(f"- 🧮 **Query Fields:** {', '.join(select_fields)}")
        except:
            pass

        st.markdown("---")
