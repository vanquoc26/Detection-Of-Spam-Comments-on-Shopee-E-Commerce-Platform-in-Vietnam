import random
from preprocessing import *
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


headers_list = [{ 
	'authority': 'httpbin.org', 
	'cache-control': 'max-age=0', 
	'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 
	'sec-ch-ua-mobile': '?0', 
	'upgrade-insecure-requests': '1', 
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
	'sec-fetch-site': 'none', 
	'sec-fetch-mode': 'navigate', 
	'sec-fetch-user': '?1', 
	'sec-fetch-dest': 'document', 
	'accept-language': 'en-US,en;q=0.9', 
}
] 
headers = random.choice(headers_list) 

def model(text):
    tokenizer = DistilBertTokenizer.from_pretrained("model_directory")
    # Load model architecture từ thư mục chứa các file model
    model = DistilBertForSequenceClassification.from_pretrained("model_directory")
    # Load model weights và map to CPU
    model.load_state_dict(torch.load(r"model_directory\bert_model.pth", map_location=torch.device('cpu')))
    model.eval()
    # Tokenize input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    # Thực hiện dự đoán
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    # Lấy nhãn dự đoán
    predicted_label = torch.argmax(logits, dim=1).item()
    # Map nhãn sang tên lớp
    label_map = {0: 'Not Spam', 1: 'Spam'}
    predicted_class = label_map[predicted_label]
    return predicted_class

        
    