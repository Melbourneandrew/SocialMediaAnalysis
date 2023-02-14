from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import torch

emotion_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
emotion_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")
emotion_label_mapping = ['anger', 'joy', 'optimism', 'sadness']
hate_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-hate")
hate_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-hate")
hate_label_mapping = ["not-hate", "hate"]
irony_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-irony")
irony_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-irony")
irony_label_mapping = ["not-irony", "irony"]
offensive_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-offensive")
offensive_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-offensive")
offensive_label_mapping = ["not-offensive", "offensive"]
sentiment_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
sentiment_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
sentiment_label_mapping = ['negative', 'neutral', 'positive']

analysis_tools = {
    "emotion": {
        "model": emotion_model,
        "tokenizer": emotion_tokenizer,
        "label_mapping": emotion_label_mapping
    },
    "hate": {
        "model": hate_model,
        "tokenizer": hate_tokenizer,
        "label_mapping": hate_label_mapping
    },
    "irony": {
        "model": irony_model,
        "tokenizer": irony_tokenizer,
        "label_mapping": irony_label_mapping
    },
    "offensive": {
        "model": offensive_model,
        "tokenizer": offensive_tokenizer,
        "label_mapping": offensive_label_mapping
    },
    "sentiment": {
        "model": sentiment_model,
        "tokenizer": sentiment_tokenizer,
        "label_mapping": sentiment_label_mapping
    }
}


def analyze(posts, analysis_options):
    labeled_predictions = {}
    label_percentages = {}
    for option in analysis_options:
        if option not in analysis_tools:
            return {"results": "Invalid analysis option"}
        print("Analyzing with " + option)
        labeled_predictions[option] = []
        label_percentages[option] = {}
        for label in analysis_tools[option]["label_mapping"]:
            label_percentages[option][label] = 0
        model = analysis_tools[option]["model"]
        tokenizer = analysis_tools[option]["tokenizer"]
        label_mapping = analysis_tools[option]["label_mapping"]

        # Truncate
        posts[:] = [post[:512] for post in posts]
        encoded_input = tokenizer(posts, padding=True, return_tensors='pt')
        outputs = model(**encoded_input)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        num_predictions = len(predictions)
        print("Made " + str(num_predictions) + " predictions" + " with " + str(len(posts)) + " posts")
        # Count Number of each label
        for i, prediction in enumerate(predictions):
            prediction = prediction.tolist()
            # Find max
            max_index = prediction.index(max(prediction))
            label_percentages[option][label_mapping[max_index]] += 1

    return label_percentages
