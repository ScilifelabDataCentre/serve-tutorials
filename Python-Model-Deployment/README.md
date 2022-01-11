# Transformer example project

This STACKn example project demonstrates how to deploy the Swedish BERT model developed by the Swedish Unemployment Agency: https://github.com/af-ai-center/SweBERT.git and publish live prediction endpoints to a STACKn model portal.

***

## BERT and the Swedish BERT models


The realease of the BERT architecture is seen as one of the major breakthroughs in NLP (natural language processing) in the last few years. BERT has presented state of the art results across a number of different use cases, such as document classification, sentiment analysis, natural language inference, questions answering, sentence similarity and more.

Arbetsförmedlingen (The Swedish Public Employment Service) has developed Swedish BERT models which were trained on Swedish Wikipedia with approximately 2 million articles and 300 million words.

## Getting started

Please follow and refer to [these detailed steps](https://github.com/scaleoutsystems/examples/tree/main/tutorials/studio/quickstart#transformers-example-project) in order to create a "STACKn Default" project and correclty set up a Jupiter instance.

Clone this repository:

    $ git clone https://github.com/scaleoutsystems/transformers-example-project.git

and then install the pip requirements and enable the Jupyter notebook extension:
    
    $ pip install -r requirements.txt
    $ jupyter nbextension enable --py widgetsnbextension
    
Now you should be ready to open the `getting_started_with_swebert.ipynb` in the _notebooks_ folder. Please follow the notebook's instructions.

## Deploying the model

Once you have run all the cells in the above notebook, open up again a terminal in your Jupyter Lab session and execute the following command within the repository directory:

- `stackn create object afbert -r minor` (**Note:** add the flag `--insecure` in case you have deployed STACKn locally with a self-signed certificate)

- `stackn get objects` (**Note:** add the flag `--insecure` in case you have deployed STACKn locally with a self-signed certificate)

(Check that the model is listed; you should be able to see the newly created model object in your Studio UI, under the "_Objects_" tab)

Deploy the newly created model object with the "_Python Model Deployment_" component (under the "_Serve_" tab in Studio). _Name_ can be anything, _Model_ should match the name of the newly created model (e.g. "afbert:v0.1.0"); leave the rest as defaults.

**Note:** It could take some time for this model to initialize, so keep checking the logs until it is available and wait until it is running successfully.

## Run the prediction

Once the above serving app is up and running, copy the endpoint URL by right-clicking on the _Open_ link.

Go back to your Jupyter Lab session and open the `predict.ipynb` notebook under the _notebooks_ folder. Paste the copied URL at line 12 in order to use the correct endpoint for the prediction. It is time to test the prediction! Run all the cells and check the results.

**Tips:** You can play around by changing the values of the `example` and `msk_ind` variables. The latter will mask (or "hide") one of the words in the example sentence; then the prediction will shown the possible candidates for such "missing" word.
