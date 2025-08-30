# Product Requirements Document: Image Prompt Builder

## 1. Introduction & Vision

The Image Prompt Builder is a web-based application designed to help users construct complex and effective text prompts for AI image generation models. The vision is to create a tool that is both powerful for experienced users and intuitive for newcomers, enabling the creation of high-quality, specific, and artistically-styled images.

This document outlines the requirements for the Minimum Viable Product (MVP), which focuses on prompt construction and usability, with plans for future integration with image generation services.

## 2. Project Phasing

### Phase 1: MVP (Minimum Viable Product)
The MVP will deliver a fully functional prompt-building tool. Users can construct, preview, and copy prompts for use in external image generation platforms.

### Phase 2: Full Integration
Phase 2 will expand on the MVP by integrating directly with image generation APIs. The primary target for integration will be Google's **Gemini 2.5 Flash Image model** (nano-banana) via the Google AI Studio API. This will allow users to:
*   Securely input their Google AI API key.
*   Send the constructed prompt to the Gemini API.
*   View a preview of the generated image directly within the application.

## 3. MVP Features

### 3.1. Structured & Collapsible Prompt Builder
The core of the application is a structured user interface for building prompts.

*   **Collapsible Sections:** Each prompt category will be housed in a collapsible container (`st.expander`). This keeps the UI clean and allows users to focus on one aspect of the prompt at a time.
*   **Global Controls:** "Expand All" and "Collapse All" buttons will be provided to manage all sections simultaneously.

### 3.2. Prompt Categories
The following categories will be available for prompt construction:

*   **Subject:** The main focus of the image.
*   **Action/Verb:** What the subject is doing.
*   **Style:** The artistic style (e.g., Photorealistic, Anime, Cyberpunk).
*   **Artist:** Emulate the style of a specific artist.
*   **Lighting:** Describe the lighting conditions.
*   **Color Palette:** Specify a color scheme.
*   **Composition:** Control the framing (e.g., Wide-angle, Close-up).
*   **Film Type:** A new category to mimic analog film types (e.g., Agfa 800, Kodachrome 400, Lomo, Lensbaby).
*   **Negative Prompts:** Specify elements to exclude.

### 3.3. User-Defined Keywords
*   **Custom Inputs:** Users can add their own keywords to each category.
*   **Persistence:** These custom keywords will be saved for the duration of the user's session, allowing for reuse without re-typing.

### 3.4. Real-time Prompt Preview
*   A dedicated text area at the top of the application will display the final, formatted prompt, ensuring it is always visible.
*   The preview will update in real-time as the user selects or deselects keywords.

### 3.5. Copy to Clipboard
*   A "Copy" button will be associated with the prompt preview text area.
*   On-click, the full prompt text is copied to the system clipboard.
*   A temporary success notification (e.g., "Copied to clipboard!") will be displayed to confirm the action.
*   **Clear All Button:** A "Clear All" button will be placed next to the "Copy" button. When clicked, it will reset the application to its initial state by clearing all selected keywords and removing any user-added custom keywords.

### 3.6. Inspiration & Discovery
*   **Inspiration Library:** A pre-populated gallery of example prompts, dynamically displayed in the sidebar.
*   **"Surprise Me" Button:** A function to randomly generate a complete prompt from the available keywords.

### 3.7. Prompt Expander
*   **Automated Prompt Enrichment:** A "✨ Expand Prompt" button, located next to the "Generated Prompt" header, enriches a simple prompt with additional descriptive details.
*   **Context-Aware Suggestions:** The feature analyzes the core subject of the prompt and intelligently adds relevant attributes related to setting, artistic style, composition, and lighting. The enriched prompt then replaces the previous content in the "Prompt Preview" text box.
*   **User-Friendly Design:** The button has a distinct green-to-blue gradient background to make it easily identifiable.
*   **Save Inspiration:** A "Save Inspiration" button allows users to save the currently generated prompt to the Inspiration Library. Saved prompts are persistent and will be available across application restarts.
*   **Inspiration Management:** Users can manage their saved inspirations directly in the sidebar. Each inspiration tile will include:
    *   A "Load" button to apply the prompt.
    *   A text input to rename the inspiration.
    *   A "❌" button to delete the inspiration.
    *   All changes (creations, renames, deletions) are saved to a local `inspirations.json` file, ensuring they persist.

## 4. Technical Specifications

*   **Framework:** The application will be built using **Streamlit**.
*   **Language:** **Python**. This is a critical requirement to ensure compatibility with the Streamlit framework and the Google AI Python SDK, which will be used in Phase 2.
*   **Deployment:** The app will be designed for easy deployment on the Streamlit Community Cloud service.

## 5. Security

*   **Secret Management:** For Phase 2, any necessary API keys or secrets will be managed using Streamlit's built-in secrets management (`.streamlit/secrets.toml`).
*   **`.gitignore`:** The `secrets.toml` file and other sensitive configuration will be added to the `.gitignore` file to prevent them from being committed to public version control.

## 6. Workflow Diagram (MVP)

```mermaid
graph TD
    subgraph "Image Prompt Builder (MVP)"
        A[Start] --> B{Structured Prompt Builder};
        B --> C[Expand/Collapse Categories];
        B --> D[Select/Add Keywords in Categories];
        D --> E[Real-time Prompt Preview];
        E --> F[Copy to Clipboard];
        F --> G[Notification: "Copied!"];
        A --> H["Inspiration Library"];
        H --> B;
        A --> I["Surprise Me"];
        I --> B;
    end

    subgraph "External Action"
      G --> J[User pastes prompt into Image Gen Service];
    end