import os
import pandas as pd
import streamlit as st # type: ignore 
import pandas as pd
import os
from utils.summaries import summarize_data_file, summarize_image_file

st.set_page_config(page_title="Luminalnsights", layout="wide")

st.title("📊 Luminalnsights")
st.markdown(
    "Use this tool to automatically generate **technical and non-technical summaries** "
    "for your **data files or visual images (charts/diagrams)**."
)

tabs = st.tabs(["📁 File Summary", "🖼️ Image Summary"])

# ---------------- Tab 1: File Summary ----------------
with tabs[0]:
    st.header("📁 Upload CSV, JSON, Excel, Parquet, or TXT")

    uploaded_file = st.file_uploader(
        "Upload a structured data file",
        type=["csv", "json", "xlsx", "xls", "parquet", "txt"]
    )

    if uploaded_file:
        st.success("✅ File uploaded successfully")
        dataset, tech_summary_df, error_message, final_summary = summarize_data_file(uploaded_file)

        if error_message:
            st.error(f"❌ {error_message}")
        else:
            st.subheader("📊 Technical Summary")
            st.dataframe(tech_summary_df)

            st.markdown("### 🧾 Dataset Snapshot")
            st.dataframe(dataset.head())

            with st.expander("🔍 View Detailed Data Insights"):
                insight_tabs = st.tabs([
                    "🧼 Null Values",
                    "🔢 Unique Values",
                    "📋 Duplicate Records",
                    "📐 Descriptive Stats",
                    "📈 Numeric Summary"
                ])

                with insight_tabs[0]:
                    null_counts = dataset.isnull().sum()
                    st.dataframe(null_counts.to_frame(name="Null Count"))
                    st.markdown(f"**Total Null Values:** `{null_counts.sum()}`")

                with insight_tabs[1]:
                    unique_counts = pd.DataFrame({
                        "Column": dataset.columns,
                        "Unique Count": [dataset[col].nunique() for col in dataset.columns]
                    })
                    st.dataframe(unique_counts)

                with insight_tabs[2]:
                    duplicate_count = dataset.duplicated().sum()
                    st.markdown(f"**Total Duplicate Records:** `{duplicate_count}`")

                with insight_tabs[3]:
                    st.dataframe(dataset.describe(include='all'))

                with insight_tabs[4]:
                    numeric_columns = dataset.select_dtypes(include="number")
                    if not numeric_columns.empty:
                        numeric_summary = numeric_columns.describe().T
                        st.dataframe(numeric_summary)
                    else:
                        st.warning("No numeric columns found.")

            st.subheader("📝 Human-Friendly Summary")
            st.markdown("""
                <style>
                pre code {
                    white-space: pre-wrap !important;       /* wrap code lines */
                    word-break: break-word !important;      /* break long words */
                }
                </style>
            """, unsafe_allow_html=True)

            # Then render your code block
            st.markdown(f"```text\n{final_summary}\n```")

# ---------------- Tab 2: Image Summary ----------------
with tabs[1]:
    st.header("🖼️ Upload an Image (Chart, Diagram, Infographic)")

    uploaded_image = st.file_uploader(
        "Upload a PNG, JPG, or JPEG image",
        type=["png", "jpg", "jpeg", "bmp", "tiff"]
    )

    if uploaded_image:
        st.success("✅ Image uploaded successfully")
        image, image_summary = summarize_image_file(uploaded_image)

        if image:
            st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)
            st.subheader("🔎 AI-Powered Image Summary")
            st.markdown("""
                <style>
                pre code {
                    white-space: pre-wrap !important;       /* wrap code lines */
                    word-break: break-word !important;      /* break long words */
                }
                </style>
            """, unsafe_allow_html=True)

            # Then render your code block
            st.markdown(f"```text\n{final_summary}\n```")
        else:
            st.error(f"❌ {image_summary}")
