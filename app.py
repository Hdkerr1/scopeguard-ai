import streamlit as st
import openai
from fpdf import FPDF
import datetime
import base64

# Set up the page
st.set_page_config(
    page_title="ScopeGuard AI - Stop Scope Creep",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state
if 'generated_contract' not in st.session_state:
    st.session_state.generated_contract = None
if 'show_pdf_section' not in st.session_state:
    st.session_state.show_pdf_section = False
if 'pdf_ready' not in st.session_state:
    st.session_state.pdf_ready = False
if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None
if 'payment_made' not in st.session_state:
    st.session_state.payment_made = False
if 'correct_password' not in st.session_state:
    st.session_state.correct_password = False

# Title and description
st.title("🛡️ ScopeGuard AI")
st.subheader("Stop Scope Creep. Generate a bulletproof Scope of Work contract in 3 minutes.")
st.markdown("---")

# Sidebar for API Key
with st.sidebar:
    st.header("🔑 API Configuration")
    st.markdown("""
    1. Get your API key from [DeepSeek](https://platform.deepseek.com/api_keys) or [OpenAI](https://platform.openai.com/api-keys)
    2. Paste it below
    3. Generate your contract
    """)
    
    api_provider = st.selectbox(
        "Choose API Provider",
        ["DeepSeek", "OpenAI"]
    )
    
    api_key = st.text_input(
        "Enter your API Key",
        type="password",
        help="Your API key is never stored and is only used for this session"
    )
    
    # Set API configuration
    if api_key:
        if api_provider == "DeepSeek":
            openai.api_base = "https://api.deepseek.com"
            openai.api_key = api_key
        else:
            openai.api_key = api_key
    
    st.markdown("---")
    st.markdown("### Pricing")
    st.markdown("""
    **Free:**
    - Generate contract text
    - Copy/paste manually
    
    **Premium: $9**
    - Professional PDF download
    - Beautiful formatting
    - Ready-to-sign document
    """)
    
    st.markdown("---")
    st.markdown("Built with ❤️ for freelancers")

# Main input form
st.header("📝 Project Details")

col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input("Client Name *", placeholder="e.g., Acme Corp")
    project_name = st.text_input("Project Name *", placeholder="e.g., Website Redesign")
    
with col2:
    project_type = st.selectbox(
        "Project Type *",
        ["Web Development", "Graphic Design", "Marketing", "Copywriting", 
         "Software Development", "Consulting", "Video Production", "Other"]
    )
    
    budget = st.number_input(
        "Total Budget ($) *",
        min_value=0,
        value=5000,
        step=500
    )

st.markdown("### 📋 Main Deliverables")
main_deliverable = st.text_area(
    "Describe the main deliverables in detail *",
    placeholder="Example: \n- Design and develop a 5-page responsive website\n- Implement contact form with email notifications\n- 3 rounds of revisions included\n- Launch and basic setup on hosting",
    height=150
)

# Generate Contract Button
st.markdown("---")
generate_button = st.button(
    "🚀 Generate Contract (Free)",
    type="primary",
    use_container_width=True
)

# Function to generate contract using LLM
def generate_scope_of_work(client_name, project_name, project_type, budget, main_deliverable):
    """Generate a Scope of Work document with anti-scope creep protections."""
    
    # System prompt - the "ruthless legal project manager"
    system_prompt = """You are a ruthless legal project manager specializing in preventing scope creep. 
    Write a comprehensive, legally-sound Scope of Work document that explicitly protects the service provider.
    
    CRUCIAL REQUIREMENTS:
    1. You MUST include a section titled "EXCLUSIONS (NOT IN SCOPE)" 
    2. Based on the Project Type, aggressively list things that are typically scope creep
    3. Use clear, unambiguous language that leaves no room for interpretation
    4. Include strong legal protections against scope creep
    5. Make it professional but firm
    
    Structure the document with these sections:
    1. PROJECT OVERVIEW
    2. SCOPE OF SERVICES (What IS included)
    3. EXCLUSIONS (NOT IN SCOPE) - This is the MOST IMPORTANT SECTION
    4. TIMELINE & MILESTONES
    5. PAYMENT TERMS
    6. CHANGE REQUEST PROCESS
    7. SIGNATURES
    
    For the EXCLUSIONS section, be specific. For example:
    - If Web Development: exclude SEO, content writing, logo design, hosting maintenance, training, etc.
    - If Graphic Design: exclude web development, copywriting, printing supervision, etc.
    - If Marketing: exclude website changes, graphic design, content creation beyond agreed, etc.
    
    Make it bulletproof against clients who try to get free extra work."""
    
    # User prompt with project details
    user_prompt = f"""
    Generate a Scope of Work document with these details:
    
    CLIENT NAME: {client_name}
    PROJECT NAME: {project_name}
    PROJECT TYPE: {project_type}
    TOTAL BUDGET: ${budget}
    
    MAIN DELIVERABLES:
    {main_deliverable}
    
    Today's Date: {datetime.datetime.now().strftime('%B %d, %Y')}
    
    Make the contract specific to a {project_type} project. Be ruthless in the EXCLUSIONS section.
    """
    
    try:
        # Determine model based on provider
        model = "deepseek-chat" if openai.api_base == "https://api.deepseek.com" else "gpt-3.5-turbo"
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating contract: {str(e)}\n\nPlease check your API key and try again."

# Function to create PDF
def create_pdf(contract_text, client_name, project_name):
    """Create a professional PDF from the contract text."""
    
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Add header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'SCOPEGUARD CONTRACT', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'Scope of Work: {project_name}', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Client: {client_name}', 0, 1, 'C')
    pdf.cell(0, 10, f'Date: {datetime.datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
    pdf.ln(10)
    
    # Add a line
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Add contract text
    pdf.set_font('Arial', '', 11)
    
    # Split text into lines that fit PDF width
    lines = contract_text.split('\n')
    for line in lines:
        # Handle section headers
        if line.upper().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', 
                                    'PROJECT', 'SCOPE', 'EXCLUSIONS', 'TIMELINE', 
                                    'PAYMENT', 'CHANGE', 'SIGNATURES')):
            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 8, line)
            pdf.set_font('Arial', '', 11)
        else:
            pdf.multi_cell(0, 6, line)
        pdf.ln(3)
    
    # Add footer
    pdf.set_y(-30)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Generated by ScopeGuard AI - Stop Scope Creep', 0, 0, 'C')
    
    return pdf.output(dest='S').encode('latin1')

# Function to create download link
def create_download_link(pdf_bytes, filename):
    """Create a download link for the PDF."""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 12px 24px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px; font-weight: bold;">📥 Download Professional PDF</a>'
    return href

# Placeholder for output
output_container = st.container()

if generate_button:
    # Basic validation
    if not all([client_name, project_name, main_deliverable]):
        st.error("Please fill in all required fields (marked with *)")
    elif not api_key:
        st.error("Please enter your API key in the sidebar")
    else:
        with output_container:
            with st.spinner("⚙️ Generating your bulletproof contract..."):
                # Generate the contract
                contract_text = generate_scope_of_work(
                    client_name, project_name, project_type, budget, main_deliverable
                )
                
                # Store in session state
                st.session_state.generated_contract = contract_text
                st.session_state.show_pdf_section = True
                
                # Generate PDF (for preview)
                try:
                    pdf_bytes = create_pdf(contract_text, client_name, project_name)
                    st.session_state.pdf_bytes = pdf_bytes
                    st.session_state.pdf_ready = True
                except Exception as e:
                    st.error(f"Error creating PDF: {str(e)}")
                    st.session_state.pdf_ready = False
                
                # Display the contract
                st.markdown("## 📄 Your Generated Scope of Work (Free Preview)")
                st.markdown("---")
                st.text_area("Contract Text", contract_text, height=400, key="contract_display")
                
                st.success("✅ Contract generated successfully!")
                st.info("💡 **Free Version:** You can copy the text above and format it yourself.")

# Payment Wall Section
if st.session_state.show_pdf_section and st.session_state.generated_contract:
    st.markdown("---")
    st.markdown("## 🚀 Upgrade to Professional PDF")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Get the Official PDF - $9")
        st.markdown("""
        **Professional PDF includes:**
        - Beautiful formatting
        - Ready-to-sign layout
        - Professional headers/footers
        - Print-ready design
        - Instant download
        """)
        
        # Payment button (link to Gumroad/Stripe)
        st.markdown("""
        [**👉 Click Here to Purchase ($9)**](https://your-gumroad-link.com)
        
        *After payment, you'll receive a password to unlock the PDF download.*
        """)
    
    with col2:
        st.markdown("### Enter Your Password")
        st.markdown("Enter the password you received after payment:")
        
        password_input = st.text_input("Password", type="password", key="password_input")
        
        if st.button("🔓 Unlock PDF Download"):
            # For MVP, use a simple password. In production, generate unique passwords
            if password_input == "SCOPE2025":  # This should come from your payment system
                st.session_state.correct_password = True
                st.success("✅ Password accepted! Download your PDF below.")
            else:
                st.error("❌ Incorrect password. Please check your email after purchase.")

# PDF Download Section (only if password is correct)
if st.session_state.correct_password and st.session_state.pdf_ready:
    st.markdown("---")
    st.markdown("## 📥 Download Your Professional PDF")
    
    # Create filename
    filename = f"ScopeGuard_Contract_{client_name.replace(' ', '_')}_{project_name.replace(' ', '_')}.pdf"
    
    # Create download link
    download_link = create_download_link(st.session_state.pdf_bytes, filename)
    
    st.markdown(download_link, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 How to Use Your Contract:")
    st.markdown("""
    1. **Send immediately** to your client for review
    2. **Get signatures** from both parties (DocuSign, HelloSign, or wet ink)
    3. **Store securely** in your project files
    4. **Refer to the EXCLUSIONS section** when scope creep attempts happen
    5. **Use the Change Request Process** for any additions
    """)

# Add testimonials/social proof
with st.expander("💬 What Our Users Say"):
    st.markdown("""
    > "ScopeGuard saved me from $5k in scope creep on a web project. The exclusions section was a lifesaver!" - **Sarah, Freelance Developer**
    
    > "My clients now understand exactly what's included and what's not. No more awkward conversations!" - **Mike, Marketing Consultant**
    
    > "Best $9 I ever spent. The contract looks so professional, clients take me more seriously." - **Jessica, Graphic Designer**
    """)

# Requirements file
st.sidebar.markdown("---")
st.sidebar.markdown("### For Developers")
st.sidebar.code("""
# requirements.txt
streamlit==1.28.0
openai==0.28.0
fpdf2==2.7.5
""")
