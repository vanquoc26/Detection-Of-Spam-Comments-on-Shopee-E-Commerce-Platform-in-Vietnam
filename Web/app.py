from flask import Flask, render_template, request, jsonify
from crawls import *
from flask_socketio import SocketIO
from MongoDB import collection
import requests
import re
import threading

app = Flask(__name__)
socketio = SocketIO(app)
is_running = False

def fetch_reviews():
    reviews = list(collection.find())
    spam_count = 0
    non_spam_count = 0
    for review in reviews:
        review['_id'] = str(review['_id'])  # Convert ObjectId to string
        if review['label'] == 'Spam':
            spam_count += 1
        else:
            non_spam_count += 1
    return reviews, spam_count, non_spam_count

def background_thread(url):
    global is_running
    is_running = True
    r = re.search(r"i\.(\d+)\.(\d+)", url)
    shop_id, item_id = r.groups()
    ratings_url = f"https://shopee.vn/api/v2/item/get_ratings?filter=1&flag=1&itemid={item_id}&limit=20&offset={{offset}}&shopid={shop_id}&type=0"
    offset = 0
    while is_running:
        data = requests.get(ratings_url.format(offset=offset), headers=headers).json()
        if not data["data"]["ratings"]:
            print("**Không còn dữ liệu mới**")
            break

        for rating in data["data"]["ratings"]:
            if rating["comment"]:  # Check for non-empty comments
                product_name = rating["product_items"][0]["name"] if rating["product_items"] else "Unknown Product"
                username = rating["author_username"]
                rating_star = rating["rating_star"]
                original_comment = rating["comment"]

                # Process the comment
                clean_text = remove_emoji(original_comment)
                clean_text = standardize_data(clean_text)
                clean_text = remove_repetitive_characters(clean_text)
                clean_text = correct_spelling_teencode(clean_text)
                label = model(clean_text)
                print(clean_text)
                # Create document to insert into MongoDB
                document = {
                    "username": username,
                    "rating": rating_star,
                    "comment": original_comment,
                    "product_name": product_name,
                    "comment_clean": clean_text,
                    "label": label
                }

                # Insert document into MongoDB and get _id
                result = collection.insert_one(document)
                document['_id'] = str(result.inserted_id)  # Convert ObjectId to string

                # Emit new review and updated counts to client via WebSocket
                reviews, spam_count, non_spam_count = fetch_reviews()
                socketio.emit('new_review', {"review": document, "spam_count": spam_count, "non_spam_count": non_spam_count})

        offset += 20

@app.route('/', methods=['GET'])
def Hello_World():
    return render_template('./index.html')

@app.route('/stop', methods=['POST'])
def stop_process():
    global is_running
    is_running = False
    return jsonify({"status": "stopped"})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        print("Đã gửi url")
        collection.delete_many({})
        print("Đã xóa collection")
        threading.Thread(target=background_thread, args=(url,)).start()
        return jsonify({"status": "success"})
    reviews, spam_count, non_spam_count = fetch_reviews()
    return render_template('index.html', reviews=reviews, spam_count=spam_count, non_spam_count=non_spam_count)

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews, spam_count, non_spam_count = fetch_reviews()
    return jsonify(reviews)

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    predict_text = model(text)  # Call your model's prediction function
    return jsonify({'predict': predict_text})

if __name__ == '__main__':
    socketio.run(app, port=3000, debug=True)
