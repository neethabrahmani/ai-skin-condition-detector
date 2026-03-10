import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import base64
from groq import Groq
from PIL import Image
import io
import re

# Configure Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Page setup
st.set_page_config(page_title="AI Skin Condition Detector", page_icon="🧴", layout="wide")

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main {background-color: #FFF9F5;}
    .title {
        text-align: center;
        color: #E75480;
        font-size: 3em;
        font-weight: bold;
        padding: 20px;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .section-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #E75480;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .section-title {
        color: #E75480;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .badge-mild {
        background: #90EE90;
        color: #006400;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: bold;
    }
    .badge-moderate {
        background: #FFD700;
        color: #7B6200;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: bold;
    }
    .badge-severe {
        background: #FFB6C1;
        color: #8B0000;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: bold;
    }
    .tip-box {
        background: #FFF0F5;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        border-left: 4px solid #FFB6C1;
    }
    .warning-box {
        background: #FFF3CD;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #FFC107;
        margin: 10px 0;
    }
    .success-box {
        background: #D4EDDA;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #28A745;
        margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #E75480, #FF8C94);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 40px;
        font-size: 1.1em;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #C0392B, #E75480);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">🧴 AI Skin Condition Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your skin photo and get a complete professional analysis powered by AI</div>', unsafe_allow_html=True)

# Warning
st.markdown("""
<div class="warning-box">
⚠️ <b>Disclaimer:</b> This tool is for educational purposes only and does not replace professional medical advice. Always consult a dermatologist for proper diagnosis.
</div>
""", unsafe_allow_html=True)

st.divider()

# Upload section
col1, col2, col3 = st.columns([1,2,1])
with col2:
    uploaded_file = st.file_uploader("📸 Choose a clear skin image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Your Uploaded Image", use_container_width=True)
        
        # Image info
        st.markdown(f"""
        <div class="tip-box">
        📁 <b>File:</b> {uploaded_file.name}<br>
        📐 <b>Size:</b> {image.size[0]} x {image.size[1]} pixels
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-card">
        <div class="section-title">💡 Tips for Best Results</div>
        ✅ Use a well-lit photo<br><br>
        ✅ Take photo in natural light<br><br>
        ✅ Make sure skin is clearly visible<br><br>
        ✅ Avoid heavy filters on photo<br><br>
        ✅ Close-up photos work best
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    if st.button("🔍 Analyze My Skin Now"):
        with st.spinner("🔬 AI is carefully analyzing your skin... This may take 10-20 seconds..."):

            # Convert image to base64
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

            # Ask Groq AI
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": """You are a world-class expert dermatologist AI with 20 years of experience.
Analyze this skin image with EXTREME detail and accuracy.
Format your response in clear sections with emojis and simple language.
Avoid medical jargon - make it easy for anyone to understand.

COMPLETE SKIN ANALYSIS REPORT
==================================

1. DETECTED SKIN CONDITIONS (Check ALL of these carefully):
   - Acne (comedonal/inflammatory/cystic/nodular)
   - Blackheads and Whiteheads
   - Post Acne Dark Marks (PIH)
   - Hyperpigmentation
   - Melasma
   - Dark circles
   - Uneven skin tone
   - Oiliness or Shine
   - Dryness or Flakiness
   - Redness or Rosacea
   - Enlarged pores
   - Fine lines or Wrinkles
   - Sun damage or Tan
   - Fungal infections
   - Eczema or Dermatitis
   - Dark spots or Age spots
   - Skin texture issues
   - Dehydration
   - Sensitivity or Irritation
   For each detected condition write:
   - Location on skin
   - How severe it is
   - How long it may have been present

2. SEVERITY ASSESSMENT
   - Rate each condition: Mild/Moderate/Severe
   - Overall skin health score out of 10
   - Priority order of which to treat first

3. SKIN TYPE
   - Exact skin type with explanation
   - T-zone analysis
   - Moisture level assessment

4. ROOT CAUSES ANALYSIS
   - Possible reasons WHY these conditions exist
   - Internal factors (hormones, diet, stress)
   - External factors (pollution, sun, products)

5. HOME REMEDIES (minimum 7)
   For each remedy:
   - Exact ingredients needed
   - Step by step preparation
   - How to apply
   - How often to use
   - Expected results timeline

6. COMPLETE INGREDIENT GUIDE
   MUST USE ingredients:
   - Name, function, recommended concentration
   MUST AVOID ingredients:
   - Name, why it is harmful for this skin

7. MORNING SKINCARE ROUTINE
   Step 1: Cleanser (type and why)
   Step 2: Toner (type and why)
   Step 3: Serum (type and why)
   Step 4: Moisturizer (type and why)
   Step 5: Sunscreen (SPF and why)

8. NIGHT SKINCARE ROUTINE
   Step 1: Double cleanse (how)
   Step 2: Treatment (type and why)
   Step 3: Serum (type and why)
   Step 4: Moisturizer (type and why)
   Step 5: Spot treatment if needed

9. WEEKLY TREATMENTS
   - Exfoliation (how often and method)
   - Face mask (type and recipe)
   - Special treatments needed

10. DIET AND LIFESTYLE PLAN
    Foods TO EAT for skin healing with reasons
    Foods TO AVOID with reasons
    Lifestyle changes including sleep, water, stress, exercise tips

11. PRODUCT RECOMMENDATIONS
    - Type of cleanser to buy
    - Type of moisturizer to buy
    - Type of sunscreen to buy
    - Type of treatment to buy
    Do not recommend specific brands, just types

12. WARNING SIGNS - See a doctor if:
    - List specific signs
    - Which specialist to visit
    - Tests that might be needed

13. RECOVERY TIMELINE
    Week 1-2: What to expect
    Month 1: What to expect
    Month 2-3: What to expect
    Long term: Maintenance plan

14. MENTAL WELLNESS NOTE
    - Encouraging message about skin journey
    - Self care tips

Be extremely thorough, accurate, compassionate and helpful.
Use simple language with emojis to make it engaging and easy to read.
Educational purposes only."""
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )

        # Store result
        result_text = response.choices[0].message.content
        st.session_state['result'] = result_text

        # Show results beautifully
        st.markdown("""
        <div class="success-box">
        ✅ <b>Analysis Complete!</b> Scroll down to see your complete skin report 👇
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
        <div class="section-title">📋 Your Complete Skin Analysis Report</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(result_text)

        # Disclaimer
        st.divider()
        st.markdown("""
        <div class="warning-box">
        🏥 <b>IMPORTANT DISCLAIMER:</b> This AI analysis is for educational purposes only. 
        Always consult a qualified dermatologist for proper diagnosis and treatment. 
        Do not use this as a substitute for professional medical advice.
        </div>
        """, unsafe_allow_html=True)
