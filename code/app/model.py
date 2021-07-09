from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast
import torch
import nltk
import numpy as np
import pandas as pd


def load_model(model_directory=None, model=DistilBertForSequenceClassification,
               tokenizer=DistilBertTokenizerFast, tokenizer_class='distilbert-base-uncased'):
    """
    Function to load a pretrained hugging face model.
    Returns a model and tokenizer
    """
    tokenizer_ = tokenizer.from_pretrained(tokenizer_class)  # Load tokenizer
    model_ = model.from_pretrained(model_directory)  # Load pretrained model
    return model_, tokenizer_


def predict_statement(sentence: str, model=None, tokenizer=None):
    """
    Function to get predictions from the inputted model and tokenizer
    Returns soft and hard predictions from a SINGLE sentence
    """
    inputs = tokenizer(sentence, truncation=True, padding=True, return_tensors="pt")
    outputs = model(**inputs)
    logit_probs = outputs.logits
    soft_preds = torch.softmax(logit_probs.float(), dim=1)  # Get soft predictions
    hard_preds = logit_probs.detach().numpy().argmax(
        axis=1)  # Get the predictions based on the higher probablity on columns
    return soft_preds, hard_preds


def monogram_explain(sent, model, tokenizer):
    '''returns whether sentence is true, and top bigrams that make it true/false'''
    orig_pred_soft, orig_pred_hard = predict_statement(sent, model, tokenizer)
    word_list = sent.split(' ')
    removed_prob = []
    for bigram in word_list:
        removed = sent.replace(bigram, '')
        soft_removed, hard_removed = predict_statement(removed, model, tokenizer)
        soft_removed = soft_removed.detach().numpy()[0]
        if orig_pred_hard[0] == 1:
            removed_prob.append(soft_removed[1])
        else:
            removed_prob.append(soft_removed[0])
    diff_prob = np.array(removed_prob) - orig_pred_soft.detach().numpy()[0][orig_pred_hard[0]]
    df = pd.DataFrame(zip(word_list, removed_prob, diff_prob), 
                      columns=['bigram','removed_prob','change_prob'])
    df = df.sort_values('change_prob')
    most_true = df.head(3)
    most_false = df.tail(3)  
    true = dict(zip(most_true.bigram, most_true.change_prob.values * -100))
    false = dict(zip(most_false.bigram, most_false.change_prob.values * -100))
    return true, false

    
def bigram_explain(sent, model, tokenizer):
    '''returns whether sentence is true, and top bigrams that make it true/false'''
    orig_pred_soft, orig_pred_hard = predict_statement(sent, model, tokenizer)
    bigram_list = list(nltk.bigrams(nltk.word_tokenize(sent)))[:-1]
    removed_prob = []
    for bigram in bigram_list:
        bigram = ' '.join(bigram)
        removed = sent.replace(bigram, '')
        soft_removed, hard_removed = predict_statement(removed, model, tokenizer)
        soft_removed = soft_removed.detach().numpy()[0]
        if orig_pred_hard[0] == 1:
            removed_prob.append(soft_removed[1])
        else:
            removed_prob.append(soft_removed[0])
    diff_prob = np.array(removed_prob) - orig_pred_soft.detach().numpy()[0][orig_pred_hard[0]]
    # print(orig_pred_soft.detach().numpy()[0][orig_pred_hard[0]])
    df = pd.DataFrame(zip(bigram_list, removed_prob, diff_prob), 
                      columns=['bigram','removed_prob','change_prob'])
    df = df.sort_values('change_prob')
    most_true = df.head(3)
    most_false = df.tail(3)
    true = dict(zip(most_true.bigram, most_true.change_prob.values * -100))
    false = dict(zip(most_false.bigram, most_false.change_prob.values * -100))
    return true, false

