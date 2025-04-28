from flask import Flask, render_template, redirect, url_for, session
from forms import BookingForm
from models import treatments

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BookingForm()
    # Populate treatment choices
    form.treatments.choices = [(t['id'], f"{t['name']} (${t['price']})") for t in treatments]
    if form.validate_on_submit():
        selected = form.treatments.data
        cart = session.get('cart', [])
        cart.extend(selected)
        session['cart'] = cart
        return redirect(url_for('cart_view'))
    return render_template('index.html', form=form)

@app.route('/cart')
def cart_view():
    cart_ids = session.get('cart', [])
    cart_items = [t for t in treatments if t['id'] in cart_ids]
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

if __name__ == '__main__':
    app.run(debug=True)