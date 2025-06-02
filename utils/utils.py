

# Now let's add the **"Export to PDF"** functionality for both:

# 1. **Data Summary (Tab 1)** – Exports technical summary, data insights, and human-readable summary.
# 2. **Image Summary (Tab 2)** – Exports the AI-generated interpretation of the uploaded image.

# ---

# ### ✅ **What You’ll Use**

# * [`fpdf`](https://py-pdf.github.io/fpdf2/) (or `reportlab`) – for simple PDF creation.
# * `st.download_button` – to let users download the generated summary.

# ---

# ### 🛠️ **Install Dependency**

# If you haven't already, install `fpdf`:

# ```bash
# pip install fpdf
# ```

# ---

# ### 🧩 **Add PDF Export Utility**

# Create this utility function:

# ```python
# from fpdf import FPDF
# import io

# def generate_pdf(title, content):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, title, ln=True)

#     pdf.set_font("Arial", "", 12)
#     for paragraph in content.split("\n"):
#         pdf.multi_cell(0, 10, paragraph)

#     pdf_output = io.BytesIO()
#     pdf.output(pdf_output)
#     pdf_output.seek(0)
#     return pdf_output
# ```

# ---

# ### 🧾 **Add to File Summary Tab**

# Below the final summary in **Tab 1**, add:

# ```python
#             st.subheader("📥 Download Summary as PDF")
#             if st.button("Generate PDF Summary"):
#                 pdf_content = f"{title}\n\nTechnical Summary:\n{tech_summary_df.to_string()}\n\nHuman-Friendly Summary:\n{final_summary}"
#                 pdf_file = generate_pdf("Data Summary Report", pdf_content)
#                 st.download_button("📄 Download PDF", data=pdf_file, file_name="data_summary.pdf", mime="application/pdf")
# ```

# ---

# ### 🖼️ **Add to Image Summary Tab**

# After showing `image_summary` in **Tab 2**, add:

# ```python
#             st.subheader("📥 Download Image Summary as PDF")
#             if st.button("Generate Image Summary PDF"):
#                 pdf_file = generate_pdf("Image Analysis Summary", image_summary)
#                 st.download_button("📄 Download PDF", data=pdf_file, file_name="image_summary.pdf", mime="application/pdf")
# ```

# ---

# ### ✅ **Summary**

# Now your Streamlit app supports:

# * 📤 Uploading files/images
# * 📈 Generating smart summaries
# * 🧠 Professor-level human + technical interpretation
# * 📄 Downloading them as well-formatted PDFs

# Would you like to style the PDF with logos, data tables, or charts next?