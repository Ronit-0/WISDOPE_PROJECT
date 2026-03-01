import streamlit as st
import os
from PIL import Image
import requests
import base64
import pandas as pd
from streamlit_gsheets import GSheetsConnection


# 1. Force Dark Mode & Page Config
st.set_page_config(page_title="Wisdope Academy", page_icon="🔬", layout="wide")

def set_custom_style():
    bg_image_url = "https://raw.githubusercontent.com/Ronit-0/WISDOPE_PROJECT/main/images/IMG_8098.PNG"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rakkas&display=swap');

        /* 1. Remove the Top Header (GitHub menu, Fork, etc.) */
        header {{visibility: hidden;}}
        
        /* 2. Remove the Bottom Footer (Made with Streamlit) */
        footer {{visibility: hidden;}}
        
        /* 3. Remove the padding at the top of the page */
        .block-container {{
            padding-top: 2rem;
        }}

        /* 4. FIX: Force Primary (Yellow) Buttons to have Black Text */
        [kind="primary"] p, 
        [kind="primary"] span, 
        [kind="primary"] div {{
            color: black !important;
            font-weight: 800 !important;
        }}

        /* Existing background and font styles */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                        url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        .wisdope-brand {{
            font-family: 'Rakkas', serif;
            font-display: swap; 
            font-size: 72px !important;
            color: white;
            margin-bottom: -10px;
        }}
        </style>
    """, unsafe_allow_html=True)

    
# Call the style function (No longer needs the file path as an argument)
set_custom_style()

# 2. Header Section
st.markdown('<p class="wisdope-brand">WISDOPE</p>', unsafe_allow_html=True)
st.write(" ")
st.markdown('<p class="mentor-name">By Rishav Karar</p>', unsafe_allow_html=True)
st.write("**MSc. (Biotech), R.A. (Pharmacognosy)**")
st.write("Coaching Classes for Maths, Physics, Chemistry & Biology")
st.write("---")

# 3. Main Features & Navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Why Join Us?", "Course Details", "Gallery", "Contact & Location", "Join Wisdope" , "Student Login"])

with tab1:
    st.header("Why join WISDOPE?")
    features = [
        "Theoretical explanations with experimentations.",
        "Hands-on laboratory training and theory classes for VIII-X & XI-XII.",
        "Comprehensive coaching with specialized NEET (UG) preparation.",
        "Special exams conducted for all Boards (I.C.S.E., C.B.S.E. & W.B.).",
        "Study mats for all classes.",
        "Two times lab research field visits in a year.",
        "One-on-one doubt clearing classes.",
        "6+ years teaching experience associated with Bose Informatics."
    ]
    for feature in features:
        st.write(f"✅ {feature}")

with tab2:
    col_x, col_y = st.columns(2)
    with col_x:
        st.header("Class Details")
        st.write("**Subjects Offered:**")
        st.write("* **Classes VIII-X:** Physics, Chemistry, and Biology (Theory and Practical)")
        st.write("* **Classes XI-XII:** Chemistry and Biology (Theory and Practical), and Physics (Practical only)")
# --- TAB 3: GALLERY ---
with tab3:
    st.header("📸 Some Glimpses of Our Coaching Institute")
    st.write("---")
    
    try:
        from streamlit_gsheets import GSheetsConnection
        import pandas as pd
        import streamlit.components.v1 as components
        
        # 1. Read images from the database
        conn = st.connection("gsheets", type=GSheetsConnection)
        gallery_df = conn.read(worksheet="Gallery", usecols=[0], ttl=0)
        gallery_images = gallery_df["Image_URL"].dropna().tolist()
        
        if len(gallery_images) == 0:
            st.info("No photos uploaded yet. Check back soon!")
        else:
            # 2. Package the images into HTML format
            slides_html = ""
            for i, img_url in enumerate(gallery_images):
                slides_html += f'''
                <div class="mySlides fade">
                    <img src="{img_url}" style="width:100%; max-height: 500px; object-fit: contain; border-radius: 8px;">
                    <div class="numbertext" style="color: white; padding: 8px; position: absolute; top: 0; background: rgba(0,0,0,0.5); border-radius: 8px;">{i+1} / {len(gallery_images)}</div>
                </div>
                '''
            
            # 3. The Smart HTML/JS Carousel Code
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
            * {{box-sizing: border-box; font-family: sans-serif;}}
            body {{ margin: 0; background-color: transparent; }}
            .slideshow-container {{ max-width: 1000px; position: relative; margin: auto; }}
            .mySlides {{ display: none; text-align: center; }}
            .prev, .next {{ cursor: pointer; position: absolute; top: 50%; width: auto; padding: 16px; margin-top: -22px; color: white; font-weight: bold; font-size: 24px; transition: 0.3s ease; border-radius: 0 3px 3px 0; user-select: none; background-color: rgba(0,0,0,0.6); text-decoration: none;}}
            .next {{ right: 0; border-radius: 3px 0 0 3px; }}
            .prev {{ left: 0; }}
            .prev:hover, .next:hover {{ background-color: rgba(0,0,0,0.9); }}
            .fade {{ animation-name: fade; animation-duration: 1.5s; }}
            @keyframes fade {{ from {{opacity: .4}} to {{opacity: 1}} }}
            </style>
            </head>
            <body>
            
            <div class="slideshow-container">
              {slides_html}
              <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
              <a class="next" onclick="plusSlides(1)">&#10095;</a>
            </div>
            
            <script>
            let slideIndex = 1;
            let timer;
            showSlides(slideIndex);
            
            function plusSlides(n) {{
              clearTimeout(timer); // Reset the timer if user manually clicks
              showSlides(slideIndex += n);
            }}
            
            function showSlides(n) {{
              let i;
              let slides = document.getElementsByClassName("mySlides");
              if (!slides.length) return;
              if (n > slides.length) {{slideIndex = 1}}    
              if (n < 1) {{slideIndex = slides.length}}
              for (i = 0; i < slides.length; i++) {{
                slides[i].style.display = "none";  
              }}
              slides[slideIndex-1].style.display = "block";  
              timer = setTimeout(() => plusSlides(1), 10000); // Auto-slide every 10 seconds
            }}
            </script>
            
            </body>
            </html>
            """
            
            # 4. Render the carousel into Streamlit
            components.html(full_html, height=550)
            
    except Exception as e:
        img_path = "images/IMG_8148.PNG"
        import os
        from PIL import Image
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption="Students during theory and practical session", use_container_width=True)

# --- TAB 4: CONTACT & LOCATION ---
with tab4:
    st.header("📍 Visit or Contact Us")
    
    # ==========================================
    #           1. VISIT US SECTION
    # ==========================================
    st.write("**Address:** 37, Dinu Lane, Kadamtala, Howrah-01")
    st.write("**Landmark:** Opp. Kadamtala Bus Stand near S.B. Jewellers")
    
    # Responsive Google Map iframe
    map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3684.348398031383!2d88.30456187515153!3d22.56608553322049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a02794eb0f59967%3A0x111e1f2a32657579!2sKadamtala%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1708000000000!5m2!1sen!2sin"
    st.markdown(
        f'''
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <iframe src="{map_embed_url}" style="width: 100%; max-width: 800px; height: 350px; border:none; border-radius: 8px;" allowfullscreen="" loading="lazy"></iframe>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    
    st.link_button("🌐 Open in Google Maps", "https://maps.google.com/?cid=4692063799864552313&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNl", use_container_width=True)
    
    st.write("---")
    
    # ==========================================
    #         2. QUICK CONNECT SECTION
    # ==========================================
    st.write("### 📞 Quick Connect")
    
    st.write("9051965176 (Call Only)")
    st.link_button("📞 Call Rishav Sir", "tel:+919051965176", use_container_width=True)
    
    st.write("") # Add some spacing
    
    st.write("7044443309 (Whatsapp Only)")
    whatsapp_url = "https://wa.me/917044443309?text=Hello!%20I%20am%20interested%20in%20joining%20Wisdope%20Academy."
    st.link_button("💬 WhatsApp Message", whatsapp_url, use_container_width=True)
    
    st.write("**Email Us:**")
    st.markdown('<div style="background-color:rgba(0,0,0,0.5); padding:10px; border-radius:5px;">📧 <a href="mailto:rishav9101999@gmail.com" style="color: white; text-decoration: none;">rishav9101999@gmail.com</a></div>', unsafe_allow_html=True)

    st.write("---")
    
    # ==========================================
    #          3. BATCH TIMINGS SECTION
    # ==========================================
    st.write("### ⏳ Batch Timings")
    st.write("🌅 **Morning:** 7:00 AM - 10:00 AM")
    st.write("🌆 **Evening:** 5:00 PM - 10:00 PM")
# --- TAB 5: JOIN WISDOPE (REGISTRATION) ---
with tab5:
    st.header("📝 Student Registration")
    st.write("Ready to start your journey with Wisdope Academy? Please fill out the form below to secure your seat.")
    
    st.write("") # Adds a little breathing room
    
    st.write("""
    **What happens next?**
    1. After you submit the form, Rishav Sir will review your details.
    2. You will receive a call or WhatsApp message within 24 hours.
    3. We will discuss batch availability and the start date.
    """)
    
    st.write("") # Adds a little breathing room before the button
    
    # Your actual Google Form link
    google_form_url = "https://forms.gle/ksZPZTy19kCnuPZg7"
    
    # --- REGISTRATION BUTTON ---
    # use_container_width=True makes it span nicely, type="primary" makes it stand out
    st.link_button("🚀 Open Registration Form", google_form_url, type="primary", use_container_width=True)
    
    # --- THE DIVIDER ---
    st.write("---")
    
    # --- NEED HELP SECTION (Centered for Desktop) ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### Need Help?")
        st.write("If you face any issues while filling the form, contact us directly:")
        # Uses your existing whatsapp_url variable
        st.link_button("💬 WhatsApp Support", whatsapp_url, use_container_width=True)

# --- TAB 6: STUDENT PORTAL ---
with tab6:
    st.header("🔐 Wisdope Portal")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.info("Log in to access your study materials or the Admin Dashboard.")
        
        with st.form("login_form"):
            login_email = st.text_input("Registered Email Address").strip().lower()
            login_pass = st.text_input("Password", type="password").strip()
            submit_button = st.form_submit_button("Access Portal")
            
            if submit_button:
                if login_email and login_pass:
                    if login_email == st.secrets["admin"]["email"] and login_pass == st.secrets["admin"]["password"]:
                        st.session_state.logged_in = True
                        st.session_state.user_name = "Rishav Sir"
                        st.session_state.user_class = "ADMIN"
                        st.rerun()
                    else:
                        try:
                            from streamlit_gsheets import GSheetsConnection
                            import pandas as pd
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            
                            df = conn.read(worksheet="Students", ttl=0) 
                            df.columns = df.columns.str.strip()
                            
                            sheet_emails = df['Email Address'].astype(str).str.strip().str.lower()
                            sheet_passwords = df['Password'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
                            user_match = df[(sheet_emails == login_email) & (sheet_passwords == login_pass)]
                            
                            if not user_match.empty:
                                st.session_state.logged_in = True
                                st.session_state.user_name = user_match.iloc[0]["Student Name"]
                                st.session_state.user_class = user_match.iloc[0]["Class"]
                                
                                # --- NEW: Capture the Date of Birth for the Birthday Feature ---
                                if "Date of Birth" in df.columns:
                                    st.session_state.user_dob = str(user_match.iloc[0]["Date of Birth"]).strip()
                                else:
                                    st.session_state.user_dob = ""
                                    
                                st.rerun()
                            else:
                                st.error("Invalid email or password.")
                        except Exception as e:
                            st.error(f"Login Error (Make sure 'Students' tab exists): {str(e)}")
                else:
                    st.warning("Please enter both fields.")

    else:
        if st.session_state.user_class == "ADMIN":
            st.success("Welcome to the Admin Dashboard, Rishav Sir!")
            admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📚 Study Materials", "📸 Photo Gallery", "💬 Student Directory"])

            # ==========================================
            #      ADMIN: STUDY MATERIALS
            # ==========================================
            with admin_tab1:
                st.write("Add new subjects, chapters, and PDF/Video links here.")
                if "publish_msg" in st.session_state:
                    st.success(st.session_state.publish_msg)
                    del st.session_state.publish_msg 
                if "reset_key" not in st.session_state:
                    st.session_state.reset_key = 0
                
                import pandas as pd
                try:
                    from streamlit_gsheets import GSheetsConnection
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_mat = conn.read(worksheet="Materials", ttl=0) 
                    if 'Chapter' not in df_mat.columns:
                        df_mat['Chapter'] = "General"
                except Exception:
                    df_mat = pd.DataFrame(columns=["Class", "Subject", "Chapter", "Link"])

                default_classes = ["XII", "XI", "X", "IX", "VIII"]
                db_classes = df_mat["Class"].dropna().unique().tolist() if not df_mat.empty else []
                admin_class_options = sorted(list(set(default_classes + db_classes))) + ["+ Add New Class"]
                selected_class = st.selectbox("1. Target Class", admin_class_options, key=f"c_drop_{st.session_state.reset_key}")
                final_class = st.text_input("Enter New Class", key=f"c_t_{st.session_state.reset_key}").strip() if selected_class == "+ Add New Class" else selected_class
                
                default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Science", "English"]
                db_subjects = df_mat["Subject"].dropna().unique().tolist() if not df_mat.empty else []
                admin_subject_options = sorted(list(set(default_subjects + db_subjects))) + ["+ Add New Subject"]
                selected_subject = st.selectbox("2. Subject Name", admin_subject_options, key=f"s_drop_{st.session_state.reset_key}")
                final_subject = st.text_input("Enter New Subject", key=f"s_t_{st.session_state.reset_key}").strip() if selected_subject == "+ Add New Subject" else selected_subject
                
                db_chapters = df_mat[(df_mat["Class"] == final_class) & (df_mat["Subject"] == final_subject)]["Chapter"].dropna().unique().tolist() if not df_mat.empty else []
                admin_chapter_options = sorted(list(set(db_chapters))) + ["+ Add New Chapter"]
                selected_chapter = st.selectbox("3. Chapter / Topic Name", admin_chapter_options, key=f"ch_drop_{st.session_state.reset_key}")
                final_chapter = st.text_input("Enter New Chapter Name", key=f"ch_t_{st.session_state.reset_key}").strip() if selected_chapter == "+ Add New Chapter" else selected_chapter
                
                raw_link = st.text_input("4. Google Drive Share Link", key=f"l_{st.session_state.reset_key}").strip()
                final_link = raw_link.replace("/view", "/preview").replace("/edit", "/preview") if raw_link else "Pending"

                if st.button("Publish Material", type="primary"):
                    if final_class and final_subject and final_chapter:
                        try:
                            mask = (df_mat["Class"].astype(str).str.strip() == final_class) & (df_mat["Subject"].astype(str).str.strip() == final_subject) & (df_mat["Chapter"].astype(str).str.strip() == final_chapter)
                            if mask.any():
                                idx = df_mat[mask].index[0]
                                df_mat.at[idx, "Link"] = final_link
                                conn.update(worksheet="Materials", data=df_mat)
                            else:
                                new_data = pd.DataFrame([{"Class": final_class, "Subject": final_subject, "Chapter": final_chapter, "Link": final_link}])
                                updated_df = pd.concat([df_mat, new_data], ignore_index=True)
                                conn.update(worksheet="Materials", data=updated_df)
                            st.session_state.publish_msg = f"✅ Published {final_chapter}!"
                            st.session_state.reset_key += 1 
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.warning("Please fill out Class, Subject, and Chapter.")

            # ==========================================
            #      ADMIN: PHOTO GALLERY
            # ==========================================
            with admin_tab2:
                st.subheader("Add Photos to Gallery")
                uploaded_photos = st.file_uploader("Select Photos (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
                compress_image = st.checkbox("Compress photos for faster loading? (Uncheck if images are already small)", value=True)
                
                if st.button("Publish to Gallery", type="primary") and uploaded_photos:
                    with st.spinner(f"Processing and Uploading {len(uploaded_photos)} photo(s)..."):
                        try:
                            import requests, base64, io
                            from PIL import Image
                            
                            new_urls = []
                            for photo in uploaded_photos:
                                if compress_image:
                                    img = Image.open(photo)
                                    if img.mode != 'RGB': img = img.convert('RGB')
                                    img.thumbnail((800, 800))
                                    buffer = io.BytesIO()
                                    img.save(buffer, format="JPEG", quality=70, optimize=True)
                                    final_bytes = buffer.getvalue()
                                else:
                                    final_bytes = photo.getvalue()

                                payload = {
                                    "key": st.secrets["IMGBB_API_KEY"],
                                    "image": base64.b64encode(final_bytes).decode('utf-8')
                                }
                                res = requests.post("https://api.imgbb.com/1/upload", data=payload)
                                if res.status_code == 200:
                                    new_urls.append({"Image_URL": res.json()["data"]["url"]})
                            
                            if new_urls:
                                conn = st.connection("gsheets", type=GSheetsConnection)
                                gallery_df = conn.read(worksheet="Gallery", usecols=[0], ttl=0)
                                updated_df = pd.concat([gallery_df, pd.DataFrame(new_urls)], ignore_index=True)
                                conn.update(worksheet="Gallery", data=updated_df)
                                st.success(f"✅ Successfully published {len(new_urls)} photo(s)!")
                            else:
                                st.error("Upload failed for all images.")
                        except Exception as e:
                            st.error(f"Error: {e}")

            # ==========================================
            #      ADMIN: STUDENT DIRECTORY (WHATSAPP)
            # ==========================================
            with admin_tab3:
                st.subheader("👥 Active Student Directory")
                st.write("Click the button next to their name to automatically send their monthly password via WhatsApp.")
                
                try:
                    from streamlit_gsheets import GSheetsConnection
                    import urllib.parse
                    
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    reg_df = conn.read(worksheet="Students", ttl=0)
                    reg_df.columns = reg_df.columns.str.strip()
                    
                    required_cols = ["Student Name", "WhatsApp Number", "Password"]
                    if all(col in reg_df.columns for col in required_cols):
                        
                        display_df = reg_df.dropna(subset=["Student Name"]).copy()
                        
                        whatsapp_links = []
                        for index, row in display_df.iterrows():
                            student_name = str(row["Student Name"]).strip()
                            student_pass = str(row["Password"]).replace(".0", "").strip()
                            
                            raw_number = str(row["WhatsApp Number"]).strip()
                            if raw_number.endswith(".0"): raw_number = raw_number[:-2]
                            clean_number = ''.join(filter(str.isdigit, raw_number))
                            
                            if len(clean_number) == 10: clean_number = "91" + clean_number
                            elif len(clean_number) == 11 and clean_number.startswith("0"): clean_number = "91" + clean_number[1:]
                            elif len(clean_number) == 12 and clean_number.startswith("91"): pass
                                
                            msg = f"Hello {student_name}, your Wisdope Academy fee is received. Your password for this month is: {student_pass}"
                            encoded_msg = urllib.parse.quote(msg)
                            link = f"https://wa.me/{clean_number}?text={encoded_msg}"
                            whatsapp_links.append(link)
                            
                        display_df["Action"] = whatsapp_links
                        st.dataframe(
                            display_df,
                            column_config={
                                "Action": st.column_config.LinkColumn(
                                    "Send Password",
                                    display_text="📲 Send WhatsApp"
                                )
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.warning("Missing required columns. Ensure your 'Students' tab has exactly: Student Name, WhatsApp Number, and Password.")
                        
                except Exception as e:
                    st.error(f"Error loading directory: {str(e)}")

        # ==========================================
        #          THE STUDENT DASHBOARD
        # ==========================================
        else:
            st.success(f"Welcome, {st.session_state.user_name}!")
            st.write(f"🎓 **Batch:** {st.session_state.user_class}")
            
            # --- THE NEW BIRTHDAY SURPRISE FEATURE ---
            if st.session_state.get("user_dob") and st.session_state.user_dob.lower() not in ["nan", "none", ""]:
                try:
                    import pandas as pd
                    from datetime import datetime, timedelta
                    
                    # Convert the Google Sheet date string into a real Date
                    dob_dt = pd.to_datetime(st.session_state.user_dob, dayfirst=True)
                    
                    # Get exact current time in India (UTC + 5:30)
                    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                    
                    # Check if the Day and Month match today!
                    if dob_dt.month == ist_now.month and dob_dt.day == ist_now.day:
                        # Make sure balloons only play once so it doesn't get annoying
                        if "bday_celebrated" not in st.session_state:
                            st.balloons()
                            st.session_state.bday_celebrated = True
                        
                        # The beautiful gold Birthday Message box
                        st.markdown(f"""
                        <div style="background-color: rgba(255, 215, 0, 0.15); padding: 15px; border-radius: 10px; border: 2px solid gold; text-align: center; margin-bottom: 20px;">
                            <h2 style="color: gold; margin-top: 0px;">🎉 Happy Birthday, {st.session_state.user_name}! 🎂</h2>
                            <p style="font-size: 16px; margin-bottom: 0px;">Wishing you a fantastic day and a wonderful year ahead! Keep shining and keep learning.<br><b>- Rishav Sir & The Wisdope Team</b></p>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    pass # Fails silently if the date format was typed incorrectly in the sheet
            
            st.write("---")
            
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                m_df = conn.read(worksheet="Materials", ttl=0) 
                if 'Chapter' not in m_df.columns:
                    m_df['Chapter'] = "General"
                    
                c_mat = m_df[m_df["Class"].astype(str).str.strip() == str(st.session_state.user_class).strip()]
                student_subs = sorted(list(set(c_mat["Subject"].tolist() if not c_mat.empty else [])))
                
                if not student_subs:
                    st.info("No materials available for your class yet.")
                else:
                    sel_sub = st.selectbox("1. Choose a subject:", student_subs)
                    if sel_sub:
                        sub_match = c_mat[c_mat["Subject"] == sel_sub]
                        chapter_list = sorted(list(set(sub_match["Chapter"].tolist() if not sub_match.empty else [])))
                        
                        sel_chap = st.selectbox("2. Choose a chapter/topic:", chapter_list)
                        
                        if sel_chap:
                            final_match = sub_match[sub_match["Chapter"] == sel_chap]
                            if not final_match.empty and str(final_match.iloc[0]["Link"]).startswith("http"):
                                st.markdown(f'<iframe src="{final_match.iloc[0]["Link"]}" style="width: 100%; height: 700px; border:none; border-radius: 8px;"></iframe>', unsafe_allow_html=True)
                            else:
                                st.info("Materials for this chapter are coming soon!")
            except Exception as e:
                st.error("Database Error. Please contact Rishav Sir.")
            
            st.write("---")
            st.subheader("📢 Notice Board")
            
            notice_url = st.secrets["admin"]["notice_board"]
            st.markdown(
                f'''
                <style>
                .notice-wrapper {{
                    display: flex; justify-content: center; width: 100%; margin-bottom: 20px;
                }}
                .notice-iframe {{
                    width: 100%; max-width: 700px; height: 250px; 
                    border: 2px solid rgba(255,255,255,0.1); border-radius: 12px; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.5); background-color: #595959; 
                    overflow-y: scroll !important; -webkit-overflow-scrolling: touch !important; overscroll-behavior: contain;
                }}
                @media (min-width: 768px) {{ .notice-iframe {{ height: 380px; }} }}
                </style>
                <div class="notice-wrapper">
                    <iframe class="notice-iframe" src="{notice_url}" scrolling="yes"></iframe>
                </div>
                ''', 
                unsafe_allow_html=True
            )

        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()
                        
            
st.divider()
# ==========================================
#               GLOBAL FOOTER
# ==========================================
# Shrunk icons to 40px, reduced gap to 10px, and forced 'nowrap' so it stays on one line!
st.write("### Follow Us On:")
st.markdown(
    """
    <div style="display: flex; justify-content: center; flex-wrap: nowrap; gap: 10px; margin-bottom: 20px;">
        <a href="https://www.facebook.com/profile.php?id=61573780375951" target="_blank">
            <img src="https://img.icons8.com/color/48/facebook-new.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.instagram.com/rishavkarar.09?igsh=MXFmazF1d2xzc3Bhcg==" target="_blank">
            <img src="https://img.icons8.com/color/48/instagram-new.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.threads.net/@rishavkarar.09" target="_blank">
            <img src="https://img.icons8.com/ios-filled/48/ffffff/threads.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://wa.me/917044443309" target="_blank">
            <img src="https://img.icons8.com/color/48/whatsapp.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.linkedin.com/in/rishav-karar-56849b3b4?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank">
            <img src="https://img.icons8.com/color/48/linkedin.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://youtube.com/@rishavkarar7470?si=2vuwFkzjAvltMOeW" target="_blank">
            <img src="https://img.icons8.com/color/48/youtube-play.png" width="40" style="transition: transform 0.2s;">
        </a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write("---")
# If your copyright text isn't centered yet, you can replace it with this to match!
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>© 2026 Wisdope Academy | Associated with Bose Informatics</p>", 
    unsafe_allow_html=True
)
