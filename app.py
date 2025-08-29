import streamlit as st
import random
from streamlit_copy_to_clipboard import st_copy_to_clipboard

# --- Page Configuration ---
st.set_page_config(
    page_title="Image Prompt Builder",
    page_icon="🎨",
    layout="wide",
)

# --- App Title ---
st.title("🎨 Image Prompt Builder")
st.write("Construct detailed and effective prompts for AI image generation.")


# --- Prompt Categories Data ---
prompt_categories = {
    "Subject": ["A majestic lion", "A futuristic cityscape", "A quiet, enchanted forest", "A bustling market in Marrakech", "A lone astronaut on Mars"],
    "Action/Verb": ["sleeping", "running", "glowing", "exploding", "melting", "flying"],
    "Style": ["Photorealistic", "Impressionistic", "Anime", "Cyberpunk", "Art Nouveau", "Steampunk", "Minimalist"],
    "Artist": ["in the style of Van Gogh", "inspired by Hayao Miyazaki", "in the style of Salvador Dali", "in the style of Frida Kahlo"],
    "Lighting": ["Dramatic lighting", "Soft morning light", "Neon glow", "Backlit", "Golden hour"],
    "Color Palette": ["Vibrant and saturated", "Monochromatic blue", "Pastel colors", "Earthy tones", "Black and white"],
    "Composition": ["Wide-angle shot", "Close-up portrait", "From a bird's-eye view", "Dutch angle", "Symmetrical"],
    "Film Type": ["Agfa 800", "Kodachrome 400", "Lomography", "Lensbaby", "Ilford HP5", "Polaroid"],
    "Negative Prompts": ["ugly", "blurry", "disfigured", "poorly drawn", "extra limbs", "watermark", "text"],
}

# --- Initialize Session State for Custom Keywords ---
if 'custom_keywords' not in st.session_state:
    st.session_state.custom_keywords = {category: [] for category in prompt_categories}

# --- "Surprise Me" Button ---
if st.button("🎲 Surprise Me!"):
    for category, keywords in prompt_categories.items():
        # Ensure the category has keywords to choose from
        all_options = keywords + st.session_state.custom_keywords.get(category, [])
        if all_options:
            # Exclude Negative Prompts from random selection
            if category != "Negative Prompts":
                random_keyword = random.choice(all_options)
                st.session_state[f"{category}_multiselect"] = [random_keyword]
            else:
                # Clear negative prompts when surprising
                st.session_state[f"{category}_multiselect"] = []
    st.rerun()

# --- UI for Collapsible Sections ---
st.header("Prompt Categories")

for category, keywords in prompt_categories.items():
    with st.expander(f"**{category}**"):
        # Combine predefined and custom keywords
        all_options = keywords + st.session_state.custom_keywords.get(category, [])
        
        selected_keywords = st.multiselect(
            f"Select {category}",
            options=all_options,
            key=f"{category}_multiselect"
        )

        # Add new keyword functionality
        new_keyword = st.text_input(f"Add a new keyword to {category}", key=f"new_keyword_{category}")
        if st.button(f"Add Keyword to {category}", key=f"add_button_{category}"):
            if new_keyword and new_keyword not in all_options:
                st.session_state.custom_keywords[category].append(new_keyword)
                st.rerun()


# --- Real-time Prompt Preview ---
st.header("Generated Prompt")

# Collect all selected keywords from session state
all_selected_keywords = []
for category in prompt_categories:
    key = f"{category}_multiselect"
    if key in st.session_state:
        all_selected_keywords.extend(st.session_state[key])

# Join keywords into a single string
prompt_text = ", ".join(all_selected_keywords)

# Display the generated prompt
st.text_area("Prompt Preview", prompt_text, height=150, key="prompt_preview")

st_copy_to_clipboard(prompt_text, "Copy to Clipboard", "Copied!")
