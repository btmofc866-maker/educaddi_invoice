from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
from num2words import num2words
import webbrowser
from threading import Timer

# Initialize Flask app with auto template reload
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.cache = {}

# -------------------------------
# Helper Functions
# -------------------------------

# Load available categories based on JSON files in 'course_data' folder
def get_categories():
    return [file.split(".")[0] for file in os.listdir("course_data") if file.endswith(".json")]

# Load courses from the selected category JSON file
def load_courses(category):
    try:
        with open(f"course_data/{category}.json") as f:
            return json.load(f)["courses"]
    except (FileNotFoundError, KeyError):
        return []

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def form():
    categories = get_categories()
    return render_template('form.html', categories=categories)

@app.route('/get_courses', methods=['POST'])
def get_courses():
    category = request.form['category']
    courses = load_courses(category)
    return jsonify(courses)

@app.route('/invoice', methods=['POST'])
def invoice():
    student_id = request.form['student_id']

    name = request.form['name']
    mobile = request.form['mobile']
    address = request.form['address']
    student_id = request.form['student_id']
    center_location = request.form['location']
    location = request.form.get('location')

    category = request.form['category']
    selected_courses = request.form.getlist('courses')
    discount = float(request.form.get('discount', 0))

    # Load selected courses and calculate prices
    courses = load_courses(category)
    selected_course_details = [course for course in courses if course["name"] in selected_courses]
    total_price = sum(course["price"] for course in selected_course_details)
    final_price = total_price - discount
    final_price_words = num2words(int(final_price), lang='en').capitalize()

    # Generate unique invoice number
    now = datetime.now()
    invoice_number = f"ST{now.strftime('%Y%m%d%H%M%S')}"
    invoice_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    # Process Installments
    installments = int(request.form.get('installments', 1))
    installment_details = []
    if installments > 1:
        for i in range(1, installments + 1):
            installment_amount = float(request.form.get(f'installment_amount_{i}', 0))
            installment_date = request.form.get(f'installment_date_{i}')
            installment_status = request.form.get(f'installment_status_{i}')
            installment_details.append({
                'amount': installment_amount,
                'date': installment_date,
                'status': installment_status
            })

    # Render invoice
    return render_template(
        'invoice.html',
        name=name,
        mobile=mobile,
        address=address,
        student_id=student_id,
        center_location=center_location,
        category=category,
        selected_course_details=selected_course_details,
        total_price=total_price,
        discount=discount,
        final_price=final_price,
        final_price_words=final_price_words,
        invoice_number=invoice_number,
        invoice_datetime=invoice_datetime,
        installments=installments,
        installment_details=installment_details
    )

# -------------------------------
# Run Flask App
# -------------------------------
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)  # Keep debug=True during development
