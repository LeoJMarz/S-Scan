import streamlit as st
import json
from model_call import grade
from logic import parse_grade

st.set_page_config(page_title="Shoe Scan AI", page_icon="👟", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    /* Better Metric Styling to prevent truncation */
    [data-testid="metric-container"] {
        background-color: #1e2130;
        padding: 5px 10px;
        border-radius: 10px;
        border: 1px solid #3e4451;
        width: fit-content;
        min-width: 100%;
    }
    [data-testid="stMetricLabel"] > div {
        font-size: 0.8rem !important;
        color: #9ea4b0 !important;
        overflow: visible !important;
        white-space: nowrap !important;
    }
    [data-testid="stMetricValue"] > div {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    .flaw-card {
        background-color: #1e2130;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        border-left: 5px solid #ff4b4b;
    }
    .upload-box {
        border: 1px dashed #3e4451;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Shoe Scan AI Analysis")
st.subheader("Footwear Assessment")

# Scan Mode Selection
scan_mode = st.radio(
    "Select Scan Mode",
    ["Quick Scan (1 Image)", "Multi-Angle Scan (4 Views)"],
    horizontal=True
)

images_to_process = []

if scan_mode == "Quick Scan (1 Image)":
    uploaded_file = st.file_uploader("Upload a shoe image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Target Image", use_container_width=True)
        images_to_process.append({
            "data": uploaded_file.getvalue(),
            "mime_type": uploaded_file.type
        })
else:
    st.info("💡 Upload 4 angles (Top, Bottom, Left, Right) for the most accurate grading.")
    col1, col2 = st.columns(2)
    
    with col1:
        top = st.file_uploader("Top View", type=["jpg", "jpeg", "png"])
        left = st.file_uploader("Left View", type=["jpg", "jpeg", "png"])
    
    with col2:
        bottom = st.file_uploader("Bottom View (Sole)", type=["jpg", "jpeg", "png"])
        right = st.file_uploader("Right View", type=["jpg", "jpeg", "png"])
    
    for img in [top, bottom, left, right]:
        if img:
            images_to_process.append({
                "data": img.getvalue(),
                "mime_type": img.type
            })

if images_to_process:
    if st.button("Start Analysis", type="primary", use_container_width=True):
        with st.spinner("🔍 Scanning materials and structural integrity..."):
            try:
                raw_response = grade(images_to_process)
                data = json.loads(raw_response)
                
                st.success("Analysis Complete!")
                
                st.markdown(f"## 🏷️ {data.get('shoe_brand', 'Unknown Brand')}")

                m1, m2, m3 = st.columns(3)
                m1.metric("Grade Score", f"{parse_grade(data['grade_score'])}/5.0")
                m2.metric("Condition Tier", data['condition_tier'])
                m3.metric("Est. Restoration", data.get('estimated_total_restoration_cost', 'N/A'))
                
                st.write(f"**Confidence Score:** {int(data['confidence_score'] * 100)}%")
                st.progress(data['confidence_score'])

                tab1, tab2, tab3 = st.tabs(["⚠️ Detected Flaws", "🧵 Material Analysis", "🛠️ Restoration Plan"])
                
                with tab1:
                    if data['visible_flaws']:
                        for flaw in data['visible_flaws']:
                            severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(flaw['severity'], "⚪")
                            st.markdown(f"""
                                <div class="flaw-card">
                                    <strong>{severity_color} {flaw['location']}:</strong> {flaw['defect_type']} ({flaw['severity']})
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No major flaws detected.")
                
                with tab2:
                    materials = data.get('detected_materials', [])
                    if materials:
                        for mat in materials:
                            st.markdown(f"""
                                <div class="flaw-card" style="border-left-color: #4caf50;">
                                    <strong>{mat['material']}</strong> ({mat['location']})<br>
                                    <small>{mat['description']}</small>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No specific materials identified.")

                with tab3:
                    repair_data = data.get('repair_recommendations', [])
                    if repair_data:
                        for repair in repair_data:
                            diff_icon = {"DIY": "👤", "Professional": "🏢", "Specialized": "🧪"}.get(repair['difficulty'], "🔧")
                            st.markdown(f"""
                                <div class="flaw-card" style="border-left-color: #4bafff;">
                                    <strong>{diff_icon} {repair['action']}</strong><br>
                                    <small>Est. Cost: {repair['estimated_cost_usd']} | Level: {repair['difficulty']}</small>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No restoration steps recommended.")
                
                st.markdown("### 📝 Expert Summary")
                st.info(data['reasoning_summary'])
                
            except Exception as e:
                st.error("Failed to parse analysis results.")
                if 'raw_response' in locals():
                    st.text_area("Raw Response Snippet (Debug)", value=raw_response[:500], height=150)
                st.exception(e)
else:
    st.warning("Please upload at least one image to begin.")
