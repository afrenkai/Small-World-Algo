from flask import Flask, render_template, request, redirect, url_for
from getcards import fetch_card_info
from classes import Card
from dbops import query_db, insert_card_into_db, create_db
from algo import find_all_valid_bridges
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'ydk'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the database
create_db()


# Check if file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    # Query all monster cards in the database for the dropdown
    cards = query_db("SELECT name FROM cards WHERE card_type = 'Monster'")

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                # Read the YDK file and process it
                main_deck_ids, extra_deck_ids, side_deck_ids = read_ydk_file(filename)

                # Insert the cards into the database (main deck, in this case)
                for card_id in main_deck_ids:
                    card = fetch_card_info(card_id=card_id)
                    if card:
                        insert_card_into_db(card)

                return redirect(url_for('index'))

        hand = request.form.getlist('hand')
        target_name = request.form['target']

        hand_cards = [
            query_db("SELECT * FROM cards WHERE name = %s", [name], one=True)
            for name in hand
        ]

        hand_cards = [
            Card(
                id=card['id'],
                name=card['name'],
                card_type=card['card_type'],
                attribute=card['attribute'],
                level=card['level'],
                atk=card['atk'],
                def_=card['def']
            )
            for card in hand_cards if card
        ]

        target_card = query_db("SELECT * FROM cards WHERE name = %s", [target_name], one=True)
        if target_card:
            target_card = Card(
                id=target_card['id'],
                name=target_card['name'],
                card_type=target_card['card_type'],
                attribute=target_card['attribute'],
                level=target_card['level'],
                atk=target_card['atk'],
                def_=target_card['def']
            )

        result, _ = find_all_valid_bridges(hand_cards, target_name, hand_cards)

        return render_template('index.html', cards=cards, result=result)

    return render_template('index.html', cards=cards, result=None)


if __name__ == '__main__':
    app.run(debug=True)
