import streamlit as st

st.set_page_config(page_title="BMI Calculator", layout="centered")

LB_PER_KG = 2.20462

# ---------- Session defaults (shared across all pages) ----------
defaults = {
    "units": "kg",
    "language": "English",
    "start_weight": 0.0,    # always stored in kg internally
    "current_weight": 0.0,  # always stored in kg internally
    "target_weight": 0.0,   # always stored in kg internally
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Translations (basic) ----------
TRANSLATIONS = {
    "English": {
        "menu": "Menu", "go_to": "Go to",
        "home": "Home", "goals": "Goals", "settings": "Settings",
        "app_title": "BMI Calculator",
        "app_caption": "Calculate your Body Mass Index (BMI) and track your goals.",
        "age": "Age (years)", "weight": "Weight", "height": "Height (cm)",
        "height_ft": "Height (ft)", "height_in": "Inches",
        "calculate": "Calculate BMI",
        "enter_warning": "Please enter a weight and height.",
        "your_result": "Your Result", "your_bmi": "Your BMI", "category": "Category",
        "age_note": "Age plays a big part in determining how serious your condition is.",
        "cat_under": "Underweight", "cat_normal": "Normal",
        "cat_over": "Overweight", "cat_obese": "Obese",
        "rep_under": "Your BMI indicates that you are underweight. Consider consulting a doctor about a better nutritional diet.",
        "rep_normal": "Your BMI is within the normal range. Keep up the good work maintaining a healthy lifestyle!",
        "rep_over": "Your BMI indicates that you are overweight. A balanced diet and regular exercise may help.",
        "rep_obese": "Your BMI indicates that you are obese. Please consult a healthcare professional to plan improvements.",
        "goals_title": "Your Goals",
        "goals_intro": "Set your weights below to track your progress.",
        "start_w": "Starting weight", "current_w": "Current weight", "target_w": "Target weight",
        "save_goals": "Save goals", "goals_saved": "Goals saved!",
        "progress_label": "Progress to your goal",
        "snapshot": "Goal Snapshot",
        "no_goals": "Set your starting and target weight on the Goals page to see your progress here.",
        "goal_reached": "🎉 You've reached your goal! Amazing work!",
        "keep_going": "Keep going — you've got this! 💪",
        "settings_title": "Settings",
        "language_label": "Language", "units_label": "Weight units",
        "settings_note": "Settings apply across all pages.",
    },
    "Spanish": {
        "menu": "Menú", "go_to": "Ir a",
        "home": "Inicio", "goals": "Objetivos", "settings": "Ajustes",
        "app_title": "Calculadora de IMC",
        "app_caption": "Calcula tu Índice de Masa Corporal (IMC) y sigue tus objetivos.",
        "age": "Edad (años)", "weight": "Peso", "height": "Altura (cm)",
        "height_ft": "Altura (ft)", "height_in": "Pulgadas",
        "calculate": "Calcular IMC",
        "enter_warning": "Por favor, introduce un peso y una altura.",
        "your_result": "Tu Resultado", "your_bmi": "Tu IMC", "category": "Categoría",
        "age_note": "La edad influye mucho en la gravedad de tu situación.",
        "cat_under": "Bajo peso", "cat_normal": "Normal",
        "cat_over": "Sobrepeso", "cat_obese": "Obesidad",
        "rep_under": "Tu IMC indica que tienes bajo peso. Considera consultar a un médico sobre una mejor dieta nutricional.",
        "rep_normal": "Tu IMC está dentro del rango normal. ¡Sigue así manteniendo un estilo de vida saludable!",
        "rep_over": "Tu IMC indica sobrepeso. Una dieta equilibrada y ejercicio regular pueden ayudar.",
        "rep_obese": "Tu IMC indica obesidad. Consulta a un profesional de la salud para planear mejoras.",
        "goals_title": "Tus Objetivos",
        "goals_intro": "Introduce tus pesos abajo para seguir tu progreso.",
        "start_w": "Peso inicial", "current_w": "Peso actual", "target_w": "Peso objetivo",
        "save_goals": "Guardar objetivos", "goals_saved": "¡Objetivos guardados!",
        "progress_label": "Progreso hacia tu objetivo",
        "snapshot": "Resumen de Objetivos",
        "no_goals": "Configura tu peso inicial y objetivo en la página de Objetivos para ver tu progreso aquí.",
        "goal_reached": "🎉 ¡Has alcanzado tu objetivo! ¡Increíble trabajo!",
        "keep_going": "¡Sigue así, tú puedes! 💪",
        "settings_title": "Ajustes",
        "language_label": "Idioma", "units_label": "Unidades de peso",
        "settings_note": "Los ajustes se aplican en todas las páginas.",
    },
}


def t(key):
    """Look up a label in the current language, falling back to English."""
    lang = st.session_state.language
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"].get(key, key))


# ---------- Unit helpers (kg <-> display units) ----------
def to_display(kg):
    return kg * LB_PER_KG if st.session_state.units == "lb" else kg


def to_kg(value):
    return value / LB_PER_KG if st.session_state.units == "lb" else value


def compute_progress():
    """Fraction (0..1) of the way from starting weight to target. None if not set."""
    start = st.session_state.start_weight
    target = st.session_state.target_weight
    current = st.session_state.current_weight or start
    if start > 0 and target > 0 and start != target:
        p = (start - current) / (start - target)
        return max(0.0, min(1.0, p))
    return None


# ---------- Sidebar navigation ----------
st.sidebar.title(t("menu"))
page = st.sidebar.radio(t("go_to"), ["home", "goals", "settings"], format_func=t)


# ======================= HOME PAGE =======================
if page == "home":
    st.title(t("app_title"))
    st.caption(t("app_caption"))
    st.divider()

    units = st.session_state.units
    col1, col2 = st.columns(2)
    age = col1.number_input(t("age"), min_value=2, max_value=120, step=1)
    weight = col2.number_input(f"{t('weight')} ({units})", min_value=1.0, max_value=1100.0, step=0.5)

    if units == "lb":  # imperial: height in feet + inches
        hcol1, hcol2 = st.columns(2)
        feet = hcol1.number_input(t("height_ft"), min_value=1, max_value=8, step=1)
        inches = hcol2.number_input(t("height_in"), min_value=0.0, max_value=11.5, step=0.5)
        height = (feet * 12 + inches) * 2.54  # convert to cm internally
    else:  # metric: height in cm
        height = st.number_input(t("height"), min_value=30.0, max_value=270.0, step=0.5)

    if st.button(t("calculate"), use_container_width=True):
        if weight > 0 and height > 0:
            bmi = to_kg(weight) / (height / 100) ** 2

            if bmi < 18.5:
                category, emoji, tone, report = t("cat_under"), "🔵", "warning", t("rep_under")
            elif bmi < 25:
                category, emoji, tone, report = t("cat_normal"), "🟢", "success", t("rep_normal")
            elif bmi < 30:
                category, emoji, tone, report = t("cat_over"), "🟠", "warning", t("rep_over")
            else:
                category, emoji, tone, report = t("cat_obese"), "🔴", "error", t("rep_obese")

            st.divider()
            st.subheader(t("your_result"))
            st.metric(t("your_bmi"), f"{bmi:.1f}")
            st.write(f"{t('category')}: {emoji} **{category}**")
            getattr(st, tone)(report)
            st.info(t("age_note"))
        else:
            st.warning(t("enter_warning"))

    # Motivating goal snapshot
    st.divider()
    st.subheader(t("snapshot"))
    progress = compute_progress()
    if progress is None:
        st.info(t("no_goals"))
    else:
        st.progress(progress, text=t("progress_label"))
        if progress >= 1.0:
            st.success(t("goal_reached"))
        else:
            st.caption(t("keep_going"))


# ======================= GOALS PAGE =======================
elif page == "goals":
    st.title(t("goals_title"))
    st.write(t("goals_intro"))
    units = st.session_state.units

    start = st.number_input(f"{t('start_w')} ({units})", min_value=0.0, max_value=1100.0,
                            step=0.5, value=to_display(st.session_state.start_weight))
    current = st.number_input(f"{t('current_w')} ({units})", min_value=0.0, max_value=1100.0,
                              step=0.5, value=to_display(st.session_state.current_weight))
    target = st.number_input(f"{t('target_w')} ({units})", min_value=0.0, max_value=1100.0,
                             step=0.5, value=to_display(st.session_state.target_weight))

    if st.button(t("save_goals"), use_container_width=True):
        st.session_state.start_weight = to_kg(start)
        st.session_state.current_weight = to_kg(current)
        st.session_state.target_weight = to_kg(target)
        st.success(t("goals_saved"))

    progress = compute_progress()
    if progress is not None:
        st.divider()
        st.progress(progress, text=t("progress_label"))
        if progress >= 1.0:
            st.success(t("goal_reached"))
        else:
            st.caption(t("keep_going"))


# ======================= SETTINGS PAGE =======================
elif page == "settings":
    st.title(t("settings_title"))

    languages = list(TRANSLATIONS.keys())
    st.session_state.language = st.selectbox(
        t("language_label"), languages, index=languages.index(st.session_state.language)
    )
    st.session_state.units = st.radio(
        t("units_label"), ["kg", "lb"], index=["kg", "lb"].index(st.session_state.units)
    )
    st.caption(t("settings_note"))
