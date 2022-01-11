import json
import torch
from transformers import BertTokenizer
from tokenizers import BertWordPieceTokenizer

def model_load():
    # Should load and return the model.
    # Optional, but if present will be loaded during
    # startup in the "default-python" environment.
    from transformers import BertForMaskedLM
    import warnings; warnings.filterwarnings('ignore')
    model = BertForMaskedLM.from_pretrained('af-ai-center/bert-base-swedish-uncased')
    return model

def model_predict(inp, model=[]):
    # Called by default-python environment.
    # inp -- default is a string, but you can also specify
    # the type in "input_type.py".
    # model is optional and the return value of load_model.
    # Should return JSON.
    
    # predict all tokens
    text = inp.pred
    tokenizer = BertTokenizer.from_pretrained('models/src/models/vocab_swebert.txt', do_lower_case=False)
#     input_ids = tokenizer(text.lower())["input_ids"]
#     tokenizer = BertTokenizer.from_pretrained('src/models/vocab_swebert.txt', lowercase=True, strip_accents=False)
    bert_word_piece_tokenizer = BertWordPieceTokenizer("models/src/models/vocab_swebert.txt", lowercase=True, strip_accents=False)
    output = bert_word_piece_tokenizer.encode(text)
    tokens = output.tokens
    indexed_tokens = output.ids
    input_ids = indexed_tokens
    print(tokens)
    
    # mask one of the tokens
    masked_index = inp.msk_ind
    tokens[masked_index] = '[MASK]'
    print(tokens)
#     input_ids[masked_index] = tokenizer.convert_tokens_to_ids('[MASK]')
    indexed_tokens[masked_index] = bert_word_piece_tokenizer.token_to_id('[MASK]')
    print(input_ids)

    # do predictions
    with torch.no_grad(): #deactivate the autograd engine to reduce memory usage and speed up
        outputs = model(torch.tensor([input_ids]))
    predictions = outputs[0]
    
    predicted_index_top5 = torch.argsort(predictions[0, masked_index], descending=True)[:5]
    predicted_token = tokenizer.convert_ids_to_tokens(predicted_index_top5)
#   predicted_index_top5
    print(predicted_token)
    return {"result": predicted_token}

if __name__ == "__main__":
    from input_type import PredType
    inp = PredType(msk_ind=10)
    print(inp)
    model = model_load()
    res = model_predict(inp, model)
    print(res)
