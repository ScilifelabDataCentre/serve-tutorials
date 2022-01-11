from pydantic import BaseModel

class PredType(BaseModel):
    # Optional, but if presents specifies the input 'inp'
    # to predict.
    # Default pred: str. Can be accessed in predict as inp.pred.
    pred = "Av alla städer i världen, är du den stad som fått allt."
    msk_ind = 1