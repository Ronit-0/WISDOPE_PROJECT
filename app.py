import streamlit as st
import os
from PIL import Image

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

with tab3:
    st.header("Some Glimpses of Our Coaching Institute")
    img_path = "images/IMG_8148.PNG"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, caption="Students during theory and practical session", use_container_width=True)
    else:
        st.error("Error: Image not found.")

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
                    # --- SECURE ADMIN LOGIN ---
                    if login_email == st.secrets["admin"]["email"] and login_pass == st.secrets["admin"]["password"]:
                        st.session_state.logged_in = True
                        st.session_state.user_name = "Rishav Sir"
                        st.session_state.user_class = "ADMIN"
                        st.rerun()
                    
                    # --- NORMAL STUDENT LOGIN ---
                    else:
                        try:
                            from streamlit_gsheets import GSheetsConnection
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            df = conn.read(worksheet="Registration", ttl=0) 
                            
                            df.columns = df.columns.str.strip()
                            df.columns = [f"{col}_{i}" if list(df.columns).count(col) > 1 else col for i, col in enumerate(df.columns)]
                            
                            sheet_emails = df['Email Address'].astype(str).str.strip().str.lower()
                            sheet_passwords = df['Password'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
                            
                            user_match = df[(sheet_emails == login_email) & (sheet_passwords == login_pass)]
                            
                            if not user_match.empty:
                                st.session_state.logged_in = True
                                st.session_state.user_name = user_match.iloc[0]["Student's Full Name"]
                                st.session_state.user_class = user_match.iloc[0]["Current Class/Grade Level"]
                                st.rerun()
                            else:
                                st.error("Invalid email or password.")
                        except Exception as e:
                            st.error(f"Debug Error: {str(e)}")
                else:
                    st.warning("Please enter both fields.")

    else:
        # ==========================================
        #           THE ADMIN DASHBOARD
        # ==========================================
        if st.session_state.user_class == "ADMIN":
            st.success("Welcome to the Admin Dashboard, Rishav Sir!")
            
            if "publish_msg" in st.session_state:
                st.success(st.session_state.publish_msg)
                del st.session_state.publish_msg 

            if "reset_key" not in st.session_state:
                st.session_state.reset_key = 0

            st.write("Add new subjects and PDF/Video links to the database here.")
            
            import pandas as pd
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_mat = conn.read(worksheet="Materials", ttl=0) 
            except Exception:
                df_mat = pd.DataFrame(columns=["Class", "Subject", "Link"])

            default_classes = ["XII", "XI", "X", "IX", "VIII"]
            db_classes = df_mat["Class"].dropna().astype(str).str.strip().unique().tolist() if not df_mat.empty else []
            admin_class_options = []
            for c in default_classes + db_classes:
                if c and c not in admin_class_options:
                    admin_class_options.append(c)
            admin_class_options.append("+ Add New Class")

            default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Science", "English"]
            db_subjects = df_mat["Subject"].dropna().astype(str).str.strip().unique().tolist() if not df_mat.empty else []
            admin_subject_options = []
            for s in default_subjects + db_subjects:
                if s and s not in admin_subject_options:
                    admin_subject_options.append(s)
            admin_subject_options.append("+ Add New Subject")

            col1, col2 = st.columns(2)
            with col1:
                selected_class = st.selectbox("Target Class", admin_class_options, key=f"c_drop_{st.session_state.reset_key}")
                
                if selected_class == "+ Add New Class":
                    final_class = st.text_input("Enter New Class Name", key=f"c_text_{st.session_state.reset_key}").strip()
                else:
                    final_class = selected_class
                    
            with col2:
                selected_subject = st.selectbox("Subject Name", admin_subject_options, key=f"s_drop_{st.session_state.reset_key}")
                
                if selected_subject == "+ Add New Subject":
                    final_subject = st.text_input("Enter New Subject Name", key=f"s_text_{st.session_state.reset_key}").strip()
                else:
                    final_subject = selected_subject
                
            raw_link = st.text_input("Google Drive Share Link (Leave blank if not ready yet)", key=f"link_{st.session_state.reset_key}").strip()
            
            if raw_link:
                final_link = raw_link
                if "/view" in raw_link:
                    final_link = raw_link.split("/view")[0] + "/preview"
                elif "/edit" in raw_link:
                    final_link = raw_link.split("/edit")[0] + "/preview"
            else:
                final_link = "Pending"

            already_exists = False
            needs_confirm = False
            
            if final_class and final_subject and not df_mat.empty:
                mask = (df_mat["Class"].astype(str).str.strip() == final_class) & (df_mat["Subject"].astype(str).str.strip() == final_subject)
                if mask.any():
                    already_exists = True
                    existing_link = str(df_mat.loc[mask, "Link"].iloc[0]).strip()
                    if existing_link.startswith("http"):
                        needs_confirm = True

            confirm_overwrite = True
            if needs_confirm:
                st.warning(f"⚠️ A material link already exists for {final_class} - {final_subject}.")
                confirm_overwrite = st.checkbox("I confirm I want to overwrite the old link with this new one.")

            if st.button("Publish Material to Students", type="primary"):
                if final_class and final_subject:
                    if needs_confirm and not confirm_overwrite:
                        st.error("Please check the confirmation box above to safely overwrite the existing material.")
                    else:
                        try:
                            if already_exists:
                                idx = df_mat[mask].index[0]
                                df_mat.at[idx, "Link"] = final_link
                                conn.update(worksheet="Materials", data=df_mat)
                            else:
                                new_data = pd.DataFrame([{"Class": final_class, "Subject": final_subject, "Link": final_link}])
                                updated_df = pd.concat([df_mat, new_data], ignore_index=True)
                                conn.update(worksheet="Materials", data=updated_df)
                            
                            st.session_state.publish_msg = f"✅ Successfully published **{final_subject}** for **Class {final_class}**!"
                            st.session_state.reset_key += 1 
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Failed to publish: {str(e)}")
                else:
                    st.warning("Please enter a Class and Subject before publishing.")
            
            st.write("---")
            if st.button("Log Out"):
                st.session_state.logged_in = False
                st.rerun()

        # ==========================================
        #          THE STUDENT DASHBOARD
        # ==========================================
        else:
            st.success(f"Welcome back to Wisdope Academy, {st.session_state.user_name}!")
            current_class = st.session_state.user_class
            st.write(f"**Batch:** {current_class}")
            st.write("---")
            
            st.subheader("📚 Select Your Subject")
            
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                materials_df = conn.read(worksheet="Materials", ttl=0) 
                
                default_subs = ["Mathematics", "Physics", "Chemistry", "Biology", "Science", "English"]
                class_db = materials_df[materials_df["Class"].astype(str).str.strip() == str(current_class).strip()]
                db_subs = class_db["Subject"].tolist() if not class_db.empty else []
                
                all_subs = []
                for sub in default_subs + db_subs:
                    if sub not in all_subs:
                        all_subs.append(sub)
                
                selected_subject_student = st.selectbox("Choose a subject:", all_subs)
                
                if selected_subject_student:
                    st.write(f"### 📖 {selected_subject_student} Materials")
                    
                    subject_match = class_db[class_db["Subject"].astype(str).str.strip() == selected_subject_student]
                    
                    if not subject_match.empty:
                        embed_url = str(subject_match.iloc[0]["Link"]).strip()
                        if embed_url.startswith("http"):
                            st.caption("These materials are view-only and cannot be downloaded.")
                            
                            # --- RESPONSIVE PDF FIX ---
                            # display: flex + justify-content centers it on desktop
                            # max-width: 1000px keeps it from getting too wide
                            st.markdown(
                                f'''
                                <div style="display: flex; justify-content: center;">
                                    <iframe src="{embed_url}" style="width: 100%; max-width: 1000px; height: 700px; border:none; border-radius: 8px;"></iframe>
                                </div>
                                ''',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.info(f"⏳ The study materials for **{selected_subject_student}** will be updated or uploaded soon. Stay tuned!")
                    else:
                        st.info(f"⏳ The study materials for **{selected_subject_student}** will be updated or uploaded soon. Stay tuned!")
            
            except Exception as e:
                st.error("Could not load study materials database. Please contact Rishav Sir.")
            
            st.write("---")
            st.subheader("📢 Notice Board")
            st.caption("Latest updates and announcements from Rishav Sir.")
            
            # --- RESPONSIVE NOTICE BOARD FIX ---
            notice_url = st.secrets["admin"]["notice_board"]
            st.markdown(
                f'''
                <div style="display: flex; justify-content: center;">
                    <iframe src="{notice_url}" style="width: 100%; max-width: 800px; height: 700px; border:none; border-radius: 8px;"></iframe>
                </div>
                ''',
                unsafe_allow_html=True,
            )
            
            st.write("---")
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
        <a href="instagram://user?username=rishavkarar.09" target="_blank">
            <img src="https://img.icons8.com/color/48/instagram-new.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.threads.net/@rishavkarar.09" target="_blank">
            <img src="https://img.icons8.com/ios-filled/48/ffffff/threads.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://wa.me/917044443309" target="_blank">
            <img src="https://img.icons8.com/color/48/whatsapp.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://linkedin.com" target="_blank">
            <img src="https://img.icons8.com/color/48/linkedin.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://youtube.com" target="_blank">
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
