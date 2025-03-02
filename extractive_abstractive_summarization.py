# -*- coding: utf-8 -*-
"""Extractive_Abstractive_Summarization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QS71M_ZY4rNneq9YlTqGmLUWobasiowp

STORY: There was once a boy who grew up in a wealthy family. His father took him on a trip to show how less fortunate people lived. They stayed on a poor family’s farm, helping with their work. Afterward, the father asked his son what he learned. Surprisingly, the boy said the poor family was lucky. He compared their simple yet fulfilling life to his own, noting their abundance in companionship, nature, and self-sufficiency. The boy realized that wealth is not just about money but also about happiness, relationships, and freedom.

PARAGRAPH: Technology is the application of scientific knowledge to develop tools, systems, and processes that improve human life. It has transformed communication, healthcare, education, and industries, making tasks more efficient and accessible.

The internet has revolutionized how people connect, while artificial intelligence and automation are reshaping industries by increasing productivity. In healthcare, technologies like telemedicine and robotic surgeries have enhanced medical treatments. Renewable energy solutions, such as solar and wind power, address environmental concerns by reducing dependence on fossil fuels.

However, technology also brings challenges like cybersecurity threats, data privacy concerns, and job displacement due to automation. Ethical considerations regarding AI and biotechnology are becoming increasingly important.

Despite these challenges, technology continues to drive innovation and progress. When used responsibly, it has the potential to solve global issues such as climate change and disease control, shaping a more advanced and sustainable future for humanity.
"""

!pip install sumy

import nltk
nltk.download('punkt_tab')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration
import torch
import random

def extractive_summaries(text, num_sentences_list=[2, 3, 4, 5]):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizers = {
        "TextRank": TextRankSummarizer(),
        "LexRank": LexRankSummarizer()
    }
    summaries = {}
    for name, summarizer in summarizers.items():
        for num_sentences in num_sentences_list:
            key = f"{name} ({num_sentences} sentences)"
            summary = summarizer(parser.document, num_sentences)
            sentences = [str(sentence) for sentence in summary]
            random.shuffle(sentences)  # Shuffle to create variations
            summaries[key] = " ".join(sentences)
    return summaries

def abstractive_summaries(text, max_length=100, min_length=30, num_variants=5):
    models = {
        "T5": ("t5-small", T5Tokenizer, T5ForConditionalGeneration),
        "BART": ("facebook/bart-large-cnn", BartTokenizer, BartForConditionalGeneration)
    }
    summaries = {}
    for model_name, (model_path, tokenizer_class, model_class) in models.items():
        tokenizer = tokenizer_class.from_pretrained(model_path)
        model = model_class.from_pretrained(model_path)
        input_text = "summarize: " + text if model_name == "T5" else text
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        model_summaries = []
        for _ in range(num_variants):
            summary_ids = model.generate(
                inputs, max_length=max_length, min_length=min_length, length_penalty=random.uniform(1.5, 2.5),
                num_beams=random.choice([4, 6, 8]), top_k=random.choice([30, 50, 70]),
                top_p=random.uniform(0.8, 0.98), temperature=random.uniform(0.6, 1.0),
                do_sample=True, early_stopping=True
            )
            model_summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))
        summaries[model_name] = model_summaries
    return summaries

# Example Usage
if __name__ == "__main__":
    text = input("Enter text to summarize:")

    print("Extractive Summaries:")
    for key, summary in extractive_summaries(text).items():
        print(f"{key}: {summary}\n")

    print("\nAbstractive Summaries:")
    abstractive = abstractive_summaries(text)
    for model, summaries in abstractive.items():
        for i, summary in enumerate(summaries, 1):
            print(f"{model} Variant {i}: {summary}\n")

