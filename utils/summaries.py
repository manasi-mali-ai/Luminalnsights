import pandas as pd
from groq import Groq  # type: ignore
from PIL import Image
import base64
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()



GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set up Groq API key
groq_client = Groq(api_key=GROQ_API_KEY)


def process_query(query):
    system_message = (
        "You are an expert data analyst and academic writer. Your job is to analyze statistical summaries and provide:\n"
        "- A **technical explanation** using correct terminology, statistics, and analytical thinking expected in academic or professional settings.\n"
        "- A **non-technical explanation** that conveys the same insights in plain, accessible language ideal for explaining to non-experts like students or professors reviewing general understanding.\n"
        "Be thoughtful, precise, and insightful."
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )

    return response.choices[0].message.content

def summarize_data_file(uploaded_file):
    try:
        filename = uploaded_file.name
        ext = os.path.splitext(filename)[-1].lower()

        if ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif ext == ".json":
            df = pd.read_json(uploaded_file)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(uploaded_file)
        elif ext == ".parquet":
            df = pd.read_parquet(uploaded_file)
        elif ext == ".txt":
            df = pd.read_csv(uploaded_file, delimiter="\t")
        else:
            return None, None, "Unsupported file format. Supported formats are: CSV, Excel, JSON, Parquet, and TXT.", ""

        # Summary with all statistics
        # tech_summary_df = df.describe(include='all', datetime_is_numeric=True)
        tech_summary_df = df.describe(include='all')


        llm_query = (
            "You are given a statistical summary of a dataset. Your task is to write two summaries:\n\n"
            "1. **Technical summary** (for an academic/professor audience):\n"
            "- Use correct statistical language (e.g., skewness, standard deviation, outliers).\n"
            "- Highlight key patterns, relationships, and anomalies.\n"
            "- Suggest hypotheses or interpretations.\n\n"
            "2. **Non-technical summary** (for general understanding):\n"
            "- Explain trends and findings clearly and simply.\n"
            "- Avoid jargon and make it intuitive.\n\n"
            f"Dataset summary:\n\n{tech_summary_df.to_string()}"
        )

        summary = process_query(llm_query)

        return df, tech_summary_df, None, summary

    except Exception as e:
        return None, None, f"Error processing file: {str(e)}", ""

def summarize_image_file(uploaded_image):
    try:
        # Handle all common image types
        ext = os.path.splitext(uploaded_image.name)[-1].lower()
        if ext not in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            return None, "Unsupported image format. Please upload PNG, JPG, JPEG, BMP, or TIFF images."

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(uploaded_image.read())
            tmp_path = tmp.name

        image = Image.open(tmp_path)

        # Convert image to base64
        image_base64 = base64.b64encode(open(tmp_path, 'rb').read()).decode()
        image_url = f"data:image/{ext.strip('.')};base64,{image_base64}"

        # Structured message with detailed instruction
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert data analyst and academic explainer. You analyze images that include charts, infographics, data tables, and visual summaries. "
                    "Your goal is to extract information and communicate insights clearly and rigorously."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "This image may contain charts, diagrams, statistics, or visual data.\n\n"
                            "**Please provide the following:**\n"
                            "1. A **technical interpretation** – include descriptions of any data elements (axes, trends, values, distributions, labels), and any relevant analytical insights.\n"
                            "2. A **non-technical explanation** – summarize what the image shows in plain, accessible language as if explaining to a student or professor evaluating for clarity and comprehension.\n"
                            "3. Identify the **likely purpose** of the visual and what a viewer should take away from it.\n"
                            "Be precise, clear, and insightful."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]

        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages
        )

        return image, response.choices[0].message.content

    except Exception as e:
        return None, f"Error analyzing image: {e}"