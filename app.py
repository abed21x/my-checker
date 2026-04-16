import streamlit as st
import pandas as pd
import csv
import io

st.set_page_config(page_title="Account Processor", layout="wide")

st.title("🛠 Account Management Tool")
tab1, tab2 = st.tabs(["📄 Rec All Acc", "✅ Check OK Acc"])

# --- প্রথম টুল: Rec All Acc ---
with tab1:
    st.header("Receive & Process All Accounts")
    input_text = st.text_area("Input Raw Data Here:", height=250, key="rec_input")
    
    if st.button("Process & Separate"):
        if input_text:
            processed_rows = []
            lines = input_text.strip().split('\n')
            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    parts = clean_line.split(None, 2)
                    if len(parts) == 3:
                        processed_rows.append(parts)
                    elif len(parts) == 2:
                        processed_rows.append([parts[0], parts[1], ""])
                    else:
                        processed_rows.append([parts[0], "", ""])
            
            if processed_rows:
                df_output = pd.DataFrame(processed_rows, columns=["UID/ID", "Password", "2FA/Code"])
                st.subheader("Output Result:")
                st.dataframe(df_output, use_container_width=True)
                csv_data = df_output.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Download CSV", csv_data, "processed_accounts.csv", "text/csv")
        else:
            st.warning("আগে কিছু ডেটা পেস্ট করুন!")

# --- দ্বিতীয় টুল: Check OK Acc ---
with tab2:
    st.header("Check OK Accounts per Worker")
    col1, col2 = st.columns(2)
    with col1:
        raw_worker_data = st.text_area("Paste Raw Worker Data (with quotes):", height=200)
    with col2:
        ok_uid_data = st.text_area("Paste OK UIDs Here:", height=200)
        
    if st.button("Check & Count Matches"):
        if raw_worker_data and ok_uid_data:
            ok_uids = set([x.strip() for x in ok_uid_data.split('\n') if x.strip()])
            results = []
            f = io.StringIO(raw_worker_data)
            reader = csv.reader(f, quotechar='"', skipinitialspace=True)
            for row in reader:
                for worker_file in row:
                    if not worker_file.strip():
                        continue
                    lines = worker_file.strip().split('\n')
                    match_count = 0
                    for line in lines:
                        parts = line.split()
                        if parts:
                            uid = parts[0].strip()
                            if uid in ok_uids:
                                match_count += 1
                    results.append(str(match_count))
            st.subheader("Match Counts (Serial):")
            st.code("\n".join(results), language="text")
        else:
            st.warning("দয়া করে উভয় বক্সে ডেটা পেস্ট করুন!")
