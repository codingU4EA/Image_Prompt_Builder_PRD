import streamlit as st
import random
import pyperclip
import json
import os

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

# --- Constants ---
INSPIRATIONS_FILE = "inspirations.json"

# --- Persistence Functions ---
def load_inspirations_from_file():
    """Loads inspiration prompts from a JSON file."""
    if os.path.exists(INSPIRATIONS_FILE):
        try:
            with open(INSPIRATIONS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or not found, return default
            pass
    return {
        "Cyberpunk City": "A futuristic cityscape, Cyberpunk, Neon glow, Wide-angle shot, in the style of Syd Mead",
        "Enchanted Forest": "A quiet, enchanted forest, glowing, Art Nouveau, Soft morning light, inspired by Hayao Miyazaki",
        "Surreal Portrait": "A lone astronaut on Mars, melting, in the style of Salvador Dali, Dramatic lighting, Close-up portrait",
    }

def save_inspirations_to_file(inspirations):
    """Saves inspiration prompts to a JSON file."""
    with open(INSPIRATIONS_FILE, "w") as f:
        json.dump(inspirations, f, indent=4)

# --- Initialize Session State ---
if 'custom_keywords' not in st.session_state:
    st.session_state.custom_keywords = {category: [] for category in prompt_categories}

if 'expander_states' not in st.session_state:
    st.session_state.expander_states = {category: True for category in prompt_categories}

if 'inspiration_prompts' not in st.session_state:
    st.session_state.inspiration_prompts = load_inspirations_from_file()

# --- Helper Functions ---
def create_category_ui(category, keywords):
    all_options = keywords + st.session_state.custom_keywords.get(category, [])
    
    selected_keywords = st.multiselect(
        f"Select {category}",
        options=all_options,
        key=f"{category}_multiselect"
    )

    new_keyword = st.text_input(f"Add a new keyword to {category}", key=f"new_keyword_{category}")
    if st.button(f"Add Keyword to {category}", key=f"add_button_{category}"):
        if new_keyword and new_keyword not in all_options:
            st.session_state.custom_keywords[category].append(new_keyword)
            st.rerun()

def generate_prompt():
    all_selected_keywords = []
    for category in prompt_categories:
        key = f"{category}_multiselect"
        if key in st.session_state:
            all_selected_keywords.extend(st.session_state[key])
    return ", ".join(all_selected_keywords)

def surprise_me():
    for category, keywords in prompt_categories.items():
        all_options = keywords + st.session_state.custom_keywords.get(category, [])
        if all_options:
            if category != "Negative Prompts":
                random_keyword = random.choice(all_options)
                st.session_state[f"{category}_multiselect"] = [random_keyword]
            else:
                st.session_state[f"{category}_multiselect"] = []

def load_inspiration(prompt_name):
    prompt = st.session_state.inspiration_prompts[prompt_name]
    # Clear existing selections
    for category in prompt_categories:
        st.session_state[f"{category}_multiselect"] = []
    
    # Select keywords from the inspiration prompt
    for keyword in prompt.split(", "):
        for category, keywords in prompt_categories.items():
            all_options = keywords + st.session_state.custom_keywords.get(category, [])
            if keyword in all_options:
                st.session_state[f"{category}_multiselect"].append(keyword)
    st.rerun()

def clear_all():
    for category in prompt_categories:
        st.session_state[f"{category}_multiselect"] = []
    st.session_state.custom_keywords = {category: [] for category in prompt_categories}
    st.rerun()

def prompt_expander():
    """Enriches the current prompt with additional details."""
    current_prompt_text = st.session_state.get("prompt_preview", "")
    if not current_prompt_text:
        st.warning("Please generate a prompt before expanding.")
        return

    # --- A more sophisticated expansion logic ---
    # This is still a simplified example. A real-world implementation
    # would likely involve a more complex NLP model or a larger ruleset.

    # Get all currently selected keywords to avoid duplicates
    all_selected = [kw.lower() for kw in current_prompt_text.split(", ")]

    # Define potential additions for different themes
    expansion_map = {
        "dog": {"Style": "Photorealistic", "Lighting": "Soft morning light", "Action/Verb": "playing fetch"},
        "cat": {"Style": "Impressionistic", "Color Palette": "Pastel colors", "Action/Verb": "napping in a sunbeam"},
        "city": {"Style": "Cyberpunk", "Lighting": "Neon glow", "Composition": "Wide-angle shot"},
        "forest": {"Style": "Art Nouveau", "Lighting": "Dappled sunlight", "Color Palette": "Earthy tones"},
        "beach": {"Style": "Photorealistic", "Lighting": "Golden hour", "Composition": "Wide-angle shot"},
        "astronaut": {"Style": "Sci-Fi", "Lighting": "Cinematic lighting", "Composition": "Close-up portrait"},
    }

    # Find a matching theme from the prompt
    theme_found = None
    for theme in expansion_map:
        if theme in current_prompt_text.lower():
            theme_found = theme
            break
    
    if not theme_found:
        st.warning("Could not determine a clear theme to expand upon. Try a more specific subject.")
        return

    # Apply the additions from the matched theme
    additions = expansion_map[theme_found]
    newly_added_keywords = []

    for category, keyword in additions.items():
        if keyword.lower() not in all_selected:
            # Add to the multiselect session state
            st.session_state[f"{category}_multiselect"].append(keyword)
            newly_added_keywords.append(keyword)

    if not newly_added_keywords:
        st.info("Prompt is already well-detailed!")
    
    st.rerun()

# --- Main App ---
def main():
    # --- Custom CSS for the Prompt Expander button ---
    st.markdown("""
    <style>
    .expand-button .stButton > button:first-child {
        background: linear-gradient(to bottom right, #28a745, #007bff);
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    </style>""", unsafe_allow_html=True)
    # --- Sidebar for Inspiration ---
    with st.sidebar:
        st.header("Inspiration")
        # Use a copy of keys to allow for deletion/renaming during iteration
        inspiration_keys = list(st.session_state.inspiration_prompts.keys())
        for name in inspiration_keys:
            # Ensure the prompt still exists before trying to render it
            if name not in st.session_state.inspiration_prompts:
                continue

            st.markdown(f"**{name}**")
            col1, col2 = st.columns([4, 1])
            with col1:
                # Button to load the inspiration prompt
                if st.button("Load", key=f"load_{name}"):
                    load_inspiration(name)
            with col2:
                # Button to delete the inspiration prompt
                if st.button("❌", key=f"delete_{name}"):
                    del st.session_state.inspiration_prompts[name]
                    save_inspirations_to_file(st.session_state.inspiration_prompts)
                    st.rerun()

            # Text input for renaming the inspiration prompt
            new_name = st.text_input(
                "Rename prompt",
                value=name,
                key=f"rename_{name}",
                label_visibility="collapsed"
            )

            # Rename logic: executes if the text input value changes
            if new_name != name:
                if new_name and new_name not in st.session_state.inspiration_prompts:
                    # To rename a dict key, pop the old item and add it back with the new key
                    st.session_state.inspiration_prompts[new_name] = st.session_state.inspiration_prompts.pop(name)
                    save_inspirations_to_file(st.session_state.inspiration_prompts)
                    st.rerun()
            st.divider()

    # --- Real-time Prompt Preview ---
    # --- Real-time Prompt Preview ---
    st.header("Generated Prompt")
    
    # --- Prompt Expander Button ---
    # Wrap the button in a div with a custom class to target it with CSS
    st.markdown('<div class="expand-button">', unsafe_allow_html=True)
    if st.button("✨ Expand Prompt"):
        prompt_expander()
    st.markdown('</div>', unsafe_allow_html=True)
            
    prompt_text = generate_prompt()
    st.text_area("Prompt Preview", prompt_text, height=150, key="prompt_preview")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Copy to Clipboard"):
            pyperclip.copy(prompt_text)
            st.success("Copied to clipboard!")
    with col2:
        if st.button("Clear All"):
            clear_all()
    with col3:
        if st.button("Save Inspiration"):
            if prompt_text:
                count = len(st.session_state.inspiration_prompts)
                name = f"My Inspiration {count + 1}"
                st.session_state.inspiration_prompts[name] = prompt_text
                save_inspirations_to_file(st.session_state.inspiration_prompts)
                st.success(f"Saved '{name}' to inspirations!")
                st.rerun()
            else:
                st.warning("Generate a prompt before saving.")

    # --- Global Controls ---
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Expand All"):
            for category in prompt_categories:
                st.session_state.expander_states[category] = True
            st.rerun()
    with col2:
        if st.button("Collapse All"):
            for category in prompt_categories:
                st.session_state.expander_states[category] = False
            st.rerun()
    with col3:
        if st.button("🎲 Surprise Me!"):
            surprise_me()
            st.rerun()

    # --- Prompt Builder UI ---
    st.header("Prompt Categories")
    for category, keywords in prompt_categories.items():
        with st.expander(f"**{category}**", expanded=st.session_state.expander_states.get(category, True)):
            create_category_ui(category, keywords)


if __name__ == "__main__":
    main()
