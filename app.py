import streamlit as st
import requests
import json
import pandas as pd

# URL of your FastAPI backend
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="INTUITIX", layout="wide")
st.title("INTUITIX: AI-Powered Peer Review & Plagiarism Checker")

# --- Tabs for different functions ---
tab_writeup, tab_code, tab_plagiarism, tab_code_plagiarism, tab_history = st.tabs([
    "✍️ Write-up Analysis", 
    "💻 Code Review", 
    "🔍 Text Plagiarism Check",
    "⚡ Code Plagiarism Check",
    "📜 History"
])

# --- Write-up Tab ---
with tab_writeup:
    st.header("Analyze Your Write-up")
    
    writeup_text = st.text_area("Paste your text here:", height=300, key="writeup_text")
    uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"], key="writeup_file")
    
    if uploaded_file:
        try:
            writeup_content = uploaded_file.getvalue().decode("utf-8")
            st.text_area("File Content:", value=writeup_content, height=300, disabled=True, key="writeup_file_display")
        except Exception:
            st.error("Could not read file. Make sure it's a valid .txt file.")
            writeup_content = ""
    else:
        writeup_content = writeup_text

    if st.button("Analyze Write-up"):
        if not writeup_content:
            st.warning("Please enter some text or upload a file.")
        else:
            with st.spinner("Analyzing with AI..."):
                form_data = {}
                file_upload = None

                if uploaded_file:
                    file_upload = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                else:
                    form_data = {"text": writeup_content}
                
                try:
                    resp = requests.post(f"{API_URL}/review/writeup", data=form_data, files=file_upload)
                    
                    if resp.status_code == 200:
                        data = resp.json()["feedback"]
                        
                        st.success("✅ Review Complete")
                        st.subheader("Scores")
                        cols = st.columns(3)
                        cols[0].metric("Grammar", f"{data['scores']['grammar']}/100")
                        cols[1].metric("Clarity", f"{data['scores']['clarity']}/100")
                        cols[2].metric("Structure", f"{data['scores']['structure']}/100")

                        st.subheader("Overall Feedback")
                        st.write(data["overall_feedback"])

                        # --- ERROR ANALYSIS SECTION ---
                        if "error_analysis" in data:
                            with st.expander("🔍 Detailed Error Analysis"):
                                error_data = data["error_analysis"]
        
                                if error_data.get("grammar_errors"):
                                    st.subheader("Grammar Errors")
                                    for error in error_data["grammar_errors"]:
                                        if isinstance(error, dict):
                                            st.error(f"**Error:** {error.get('error', 'Unknown')}")
                                            st.success(f"**Correction:** {error.get('correction', 'Not provided')}")
                                            st.write(f"**Severity:** {error.get('severity', 'Unknown')}")
                                            st.write("---")
        
                                if error_data.get("spelling_errors"):
                                    st.subheader("Spelling Errors")
                                    for error in error_data["spelling_errors"]:
                                        st.error(f"• {error}")
        
                                if error_data.get("article_issues"):
                                    st.subheader("Article Issues")
                                    for issue in error_data["article_issues"]:
                                        # Extract the description from the dictionary
                                        if isinstance(issue, dict):
                                            description = issue.get('description', 'No description provided')
                                            st.warning(f"• {description}")
                                        else:
                                            st.warning(f"• {issue}")
                        # --- END ERROR ANALYSIS ---

                        with st.expander("See detailed justifications"):
                            if "justifications" in data:
                                justifications = data["justifications"]
                                if isinstance(justifications, dict):
                                    for key, value in justifications.items():
                                        st.write(f"**{key.replace('_', ' ').title()}:**")
                                        st.write(value)
                                        st.write("---")
                                else:
                                    st.write(justifications)
                            else:
                                st.info("No detailed justifications provided.")
                    else:
                        st.error(f"Error: {resp.status_code} - {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {e}")

# --- Code Review Tab ---
with tab_code:
    st.header("Review Your Code")
    
    code_text = st.text_area("Paste your code here:", height=300, key="code_text")
    code_file = st.file_uploader("Or upload a code file", type=None, key="code_file")
    
    language = st.selectbox("Select Language:", 
                            ("Python", "JavaScript", "Java", "C++", "HTML", "CSS", "SQL", "Other"), 
                            key="code_lang")

    if code_file:
        try:
            code_content = code_file.getvalue().decode("utf-8")
            st.text_area("File Content:", value=code_content, height=300, disabled=True, key="code_file_display")
        except Exception:
            st.error("Could not read file. Make sure it's a text-based file.")
            code_content = ""
    else:
        code_content = code_text

    if st.button("Review Code"):
        if not code_content:
            st.warning("Please paste your code or upload a file.")
        else:
            with st.spinner("Reviewing code..."):
                form_data = {"language": language}
                file_upload = None
                
                if code_file:
                    file_upload = {"file": (code_file.name, code_file.getvalue(), code_file.type or "application/octet-stream")}
                else:
                    form_data["code"] = code_content

                try:
                    resp = requests.post(f"{API_URL}/review/code", data=form_data, files=file_upload)
                    
                    if resp.status_code == 200:
                        data = resp.json()["feedback"]
                        st.success("✅ Code Review Complete")
                        st.subheader("Feedback")
                        if isinstance(data, dict) and "feedback" in data:
                            st.markdown(data["feedback"])
                        else:
                            st.markdown(data)
                    else:
                        st.error(f"Error: {resp.status_code} - {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {e}")

# --- Text Plagiarism Check Tab ---
with tab_plagiarism:
    st.header("Check for Text Plagiarism")
    
    plagiarism_text = st.text_area("Paste text here to check for plagiarism:", height=300, key="plagiarism_text")

    if st.button("Check for Text Plagiarism"):
        if plagiarism_text:
            with st.spinner("Analyzing text for plagiarism..."):
                payload = {"text": plagiarism_text, "filename": "text_plagiarism_check"}
                try:
                    resp = requests.post(f"{API_URL}/review/plagiarism", json=payload)
                    if resp.status_code == 200:
                        data = resp.json()["feedback"]
                        st.success("✅ Text Plagiarism Check Complete")
                        
                        # Plagiarism Score
                        st.subheader("Plagiarism Score")
                        score = data.get("plagiarism_score", 0)
                        confidence = data.get("confidence", "Unknown")
                        
                        cols = st.columns(3)
                        cols[0].metric("Plagiarism Score", f"{score}/100")
                        cols[1].metric("Confidence", confidence)
                        cols[2].metric("Risk Level", 
                                     "High" if score > 70 else "Medium" if score > 40 else "Low")
                        
                        st.subheader("Analysis Summary")
                        st.write(data["summary"])
                        
                        # Potential Sources
                        st.subheader("🔍 Potential Sources")
                        if data.get("sources"):
                            for source in data["sources"]:
                                with st.expander(f"📚 {source.get('title', 'Unknown Source')} - Similarity: {source.get('similarity', 'N/A')}"):
                                    st.write(f"**URL:** {source.get('uri', 'N/A')}")
                                    if source.get('matched_phrases'):
                                        st.write("**Matched Phrases:**")
                                        for phrase in source['matched_phrases']:
                                            st.write(f"• {phrase}")
                        else:
                            st.info("No potential sources identified")
                            
                        # Matched Phrases
                        if data.get("matched_phrases"):
                            st.subheader("📋 Matched Phrases")
                            for phrase in data["matched_phrases"]:
                                st.write(f"• `{phrase}`")
                        
                        # Recommendations
                        if data.get("recommendations"):
                            st.subheader("💡 Recommendations")
                            for rec in data["recommendations"]:
                                st.write(f"• {rec}")
                                
                    else:
                        st.error(f"Error: {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {e}")
        else:
            st.warning("Please paste your text.")

# --- Code Plagiarism Check Tab ---
with tab_code_plagiarism:
    st.header("Check for Code Plagiarism")
    
    st.info("Detect if code was potentially copied from online sources or other submissions")
    
    code_plagiarism_text = st.text_area("Paste code here to check for plagiarism:", height=300, key="code_plagiarism_text")
    code_plagiarism_file = st.file_uploader("Or upload a code file", type=None, key="code_plagiarism_file")
    
    code_plagiarism_language = st.selectbox("Select Language:", 
                                           ("Python", "JavaScript", "Java", "C++", "HTML", "CSS", "SQL", "Other"), 
                                           key="code_plagiarism_lang")

    if code_plagiarism_file:
        try:
            code_plagiarism_content = code_plagiarism_file.getvalue().decode("utf-8")
            st.text_area("File Content:", value=code_plagiarism_content, height=300, disabled=True, key="code_plagiarism_file_display")
        except Exception:
            st.error("Could not read file. Make sure it's a text-based file.")
            code_plagiarism_content = ""
    else:
        code_plagiarism_content = code_plagiarism_text

    if st.button("Check for Code Plagiarism"):
        if not code_plagiarism_content:
            st.warning("Please paste your code or upload a file.")
        else:
            with st.spinner("Analyzing code for plagiarism..."):
                payload = {
                    "text": code_plagiarism_content, 
                    "filename": f"code_plagiarism_{code_plagiarism_language}",
                    "language": code_plagiarism_language
                }
                try:
                    resp = requests.post(f"{API_URL}/review/code_plagiarism", json=payload)
                    if resp.status_code == 200:
                        data = resp.json()["feedback"]
                        st.success("✅ Code Plagiarism Check Complete")
                        
                        # Plagiarism Score
                        st.subheader("Plagiarism Score")
                        score = data.get("plagiarism_score", 0)
                        confidence = data.get("confidence", "Unknown")
                        
                        cols = st.columns(3)
                        cols[0].metric("Plagiarism Score", f"{score}/100")
                        cols[1].metric("Confidence", confidence)
                        cols[2].metric("Risk Level", 
                                     "High" if score > 70 else "Medium" if score > 40 else "Low")
                        
                        st.subheader("Analysis Summary")
                        st.write(data["summary"])
                        
                        # Potential Sources
                        st.subheader("🔍 Potential Sources")
                        if data.get("sources"):
                            for source in data["sources"]:
                                with st.expander(f"💻 {source.get('title', 'Unknown Source')} - Similarity: {source.get('similarity', 'N/A')}"):
                                    st.write(f"**URL:** {source.get('uri', 'N/A')}")
                                    if source.get('matched_patterns'):
                                        st.write("**Matched Patterns:**")
                                        for pattern in source['matched_patterns']:
                                            st.write(f"• {pattern}")
                        else:
                            st.info("No potential sources identified")
                        
                        # Similarity Indicators
                        st.subheader("⚠️ Similarity Indicators")
                        if "indicators" in data:
                            for indicator in data["indicators"]:
                                if isinstance(indicator, dict):
                                    pattern = indicator.get('pattern', 'Unknown Pattern')
                                    description = indicator.get('description', 'No description')
                                    severity = indicator.get('severity', 'Unknown')
                                    st.write(f"**• {pattern}** ({severity}): {description}")
                                else:
                                    st.write(f"• {indicator}")
                        else:
                            st.info("No specific indicators found")
                        
                        # Recommendations
                        st.subheader("💡 Recommendations")
                        if data.get("recommendations"):
                            for rec in data["recommendations"]:
                                st.write(f"• {rec}")
                        else:
                            st.info("No specific recommendations")
                                
                    else:
                        st.error(f"Error: {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to connect to API: {e}")

# --- History Tab ---
with tab_history:
    st.header("Past Reviews")
    
    if st.button("Refresh History"):
        st.rerun()

    try:
        resp = requests.get(f"{API_URL}/history")
        if resp.status_code == 200:
            df = pd.DataFrame(resp.json())
            if not df.empty:
                df["scores_dict"] = df["scores"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
                
                display_df = df[["filename", "review_type", "feedback", "created_at"]].copy()
                display_df["scores"] = df["scores_dict"].apply(lambda x: ", ".join([f"{k}: {v}" for k, v in x.items()]) if x else "N/A")
                
                st.dataframe(display_df, use_container_width=True)
                
                with st.expander("See Raw Data"):
                    st.json(resp.json())
            else:
                st.info("No reviews yet.")
        else:
            st.error(f"Error: {resp.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")