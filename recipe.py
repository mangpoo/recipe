from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Groq API 설정
client = Groq(api_key=api_key)

# 요리 종류 리스트
cuisines = [
    "",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek",
    "Korean",
]

# 식이 제한 리스트
dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced",
]

# 언어 딕셔너리
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi',
}


@app.route('/')
def index():
    return render_template(
        'index.html',
        cuisines=cuisines,
        dietary_restrictions=dietary_restrictions,
        languages=languages
    )


@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # 사용자 입력 받기
    ingredients = request.form.getlist('ingredient')

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    # cuisine, restrictions, language 추출
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_language = request.form.get('language')

    # 프롬프트 구성 (언어 포함)
    prompt = (
        f"Craft a recipe in HTML in {selected_language} using "
        f"{', '.join(ingredients)}. "
        f"It's okay to use some other necessary ingredients. "
        f"Ensure the recipe ingredients appear at the top, "
        f"followed by the step-by-step instructions."
    )

    if selected_cuisine:
        prompt += f" The cuisine should be {selected_cuisine}."

    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f" The recipe should have the following restrictions: {', '.join(selected_restrictions)}."

    # Groq API 호출
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        recipe = completion.choices[0].message.content
        # 마크다운 코드블록 제거
        recipe = recipe.strip()
        if recipe.startswith("```html"):
            recipe = recipe[7:]
        if recipe.startswith("```"):
            recipe = recipe[3:]
        if recipe.endswith("```"):
            recipe = recipe[:-3]
        recipe = recipe.strip()
    except Exception as e:
        recipe = f"<p>Error generating recipe: {str(e)}</p>"

    return render_template('recipe.html', recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)
