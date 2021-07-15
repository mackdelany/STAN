
from pathlib import Path

from transformers import DistilBertTokenizer, DistilBertModel, DistilBertConfig, DistilBertForSequenceClassification


def save_hf_models(
    stan_path: str = './stan/model/saved/hf/predict',
    octo_path: str = './stan/model/saved/hf/triage',
    stan_tokenizer_name: str = 'stan_tokenizer',
    octopus_model_name: str = 'octopus_triage_model',
    octopus_tokenizer_name: str = 'octopus_tokenizer',
    octopus_config_name: str = 'octopus_model_config',
    model_max_length: int = 512
) -> None:
    print('Saving Hugging Face models...')

    print(f"{'-'*90}\nSTAN Predict model\n{'-'*90}")
    print('\nLoading and saving tokenizer, distilbert-base-uncased from pretrained')
    stan_tokenizer = DistilBertTokenizer.from_pretrained(
        'distilbert-base-uncased',
        max_length=model_max_length
    )
    stan_tokenizer.save_pretrained(
        str(Path(stan_path, stan_tokenizer_name))
    )

    print(f"\n\n{'-'*90}\nOCTOPUS Triage model\n{'-'*90}")
    print('\nLoading and saving tokenizer, distilbert-base-uncased from pretrained')
    octopus_tokenizer = DistilBertTokenizer.from_pretrained(
        'distilbert-base-uncased',
        max_length=model_max_length
    )
    octopus_tokenizer.save_pretrained(
        str(Path(octo_path, octopus_tokenizer_name))
    )

    print('\nLoading and saving config, distilbert-base-uncased from pretrained')
    octopus_config = DistilBertConfig.from_pretrained(
        'distilbert-base-uncased', return_dict=True
    )
    octopus_config.save_pretrained(
        str(Path(octo_path, octopus_config_name))
    )

    print('\nLoading and saving model, distilbert-base-uncased from pretrained')
    octo_distilbert = DistilBertModel.from_pretrained(
        'distilbert-base-uncased', config=octopus_config
    )
    octo_distilbert.save_pretrained(
        str(Path(octo_path, octopus_model_name))
    )


if __name__ == '__main__':
    save_hf_models()
