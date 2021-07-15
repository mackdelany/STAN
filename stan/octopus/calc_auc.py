
from pathlib import Path

import torch

from .training_util import concat_tensors_in_dict, get_confusion_matrix, pd_series_to_tensor, record_octopus_metrics
from .octopus_data_manager import OctopusDataManager
from .octopus_model import OctopusModel

FAST_CONTEXTS = ['EPS_FAST', 'EPSI_FAST', 'ESNO_FAST', 'STAN_FAST']
VITAL_CONTEXTS = ['EPS_VITAL', 'EPSI_VITAL', 'ESNO_VITAL', 'STAN_VITAL']
FULL_CONTEXTS = ['EPS_FULL', 'EPSI_FULL', 'ESNO_FULL', 'STAN_FULL']


def calc_octupus_auc(
    octopus: OctopusModel,
    dm: OctopusDataManager,
    save_folder=None,
    intervals=3,
    eval_batch_size=50,
    device=None,
    tag=None
) -> None:
    if not save_folder:
        raise ValueError('Need save folder?')
    if not device:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    thresholds = list(range(0, intervals+2))
    thresholds = [t/(intervals+1) for t in thresholds]
    assert 0 in thresholds and 1 in thresholds and len(
        thresholds) == intervals + 2

    """Prepare data..

    We have three contexts...
    - FAST
    - VITAL
    - FULL

    Let's evaluate all...
    """
    fast_mask = pd_series_to_tensor(dm.val_df.data_class.isin(FAST_CONTEXTS))
    vital_mask = pd_series_to_tensor(dm.val_df.data_class.isin(VITAL_CONTEXTS))
    full_mask = pd_series_to_tensor(dm.val_df.data_class.isin(FULL_CONTEXTS))
    assert dm.val_df.shape[0] == fast_mask.shape[0] == vital_mask.shape[0] == full_mask.shape[0]

    octopus.eval()

    with torch.no_grad():
        input_ids = dm.val_encodings['input_ids'].to(device)
        attn_mask = dm.val_encodings['attention_mask'].to(device)
        outputs, val_examples = octopus.infer_in_batches(
            input_ids, attn_mask, eval_batch_size)

        for thres in thresholds:
            abcd_probs = outputs['abcd_probs']
            sepsis_probs = outputs['sepsis_probs']

            y2_probs = torch.masked_select(
                abcd_probs[:, 0], dm.abcd_val_context_mask)
            y3_probs = torch.masked_select(
                abcd_probs[:, 1], dm.abcd_val_context_mask)
            y4_probs = torch.masked_select(
                abcd_probs[:, 2], dm.abcd_val_context_mask)
            y5_probs = torch.masked_select(
                abcd_probs[:, 3], dm.abcd_val_context_mask)
            y6_probs = torch.masked_select(
                abcd_probs[:, 4], dm.abcd_val_context_mask)
            y7_probs = torch.masked_select(
                abcd_probs[:, 5], dm.abcd_val_context_mask)
            y8_probs = torch.masked_select(
                abcd_probs[:, 6], dm.abcd_val_context_mask)
            sepsis_probs = torch.masked_select(
                sepsis_probs[:, 0], dm.outcome_val_context_mask)

            y2_pred = (y2_probs > thres).long()
            y3_pred = (y3_probs > thres).long()
            y4_pred = (y4_probs > thres).long()
            y5_pred = (y5_probs > thres).long()
            y6_pred = (y6_probs > thres).long()
            y7_pred = (y7_probs > thres).long()
            y8_pred = (y8_probs > thres).long()
            y9_pred = (sepsis_probs > thres).long()

            airway_cm = get_confusion_matrix(
                y2_pred, dm.y2_val_tensor, rates=True)
            breathing_cm = get_confusion_matrix(
                y3_pred, dm.y3_val_tensor, rates=True)
            circulation_cm = get_confusion_matrix(
                y4_pred, dm.y4_val_tensor, rates=True)
            disability_cm = get_confusion_matrix(
                y5_pred, dm.y5_val_tensor, rates=True)
            neuro_cm = get_confusion_matrix(
                y6_pred, dm.y6_val_tensor, rates=True)
            immunocompromised_cm = get_confusion_matrix(
                y7_pred, dm.y7_val_tensor, rates=True)
            mental_health_cm = get_confusion_matrix(
                y8_pred, dm.y8_val_tensor, rates=True)
            sepsis_cm = get_confusion_matrix(
                y9_pred, dm.y9_val_tensor, rates=True)

            metrics = {
                'threshold': thres,
                'airway_cm': airway_cm,
                'breathing_cm': breathing_cm,
                'circulation_cm': circulation_cm,
                'disability_cm': disability_cm,
                'neuro_cm': neuro_cm,
                'immunocompromised_cm': immunocompromised_cm,
                'mental_health_cm': mental_health_cm,
                'sepsis_cm': sepsis_cm,
            }

            record_octopus_metrics(metrics, save_folder, tag)

    print('Calculations completed!')


if __name__ == '__main__':
    from datetime import datetime as dt
    import platform

    BATCH_SIZE = 64
    DEBUG = True
    INTERVALS = 10

    MODELS = [
        'plz_work_lr_5_bs_64',
        'lr_5_bs_64_new_weights',
        'lr_5_bs_64_new_weights_half_gap_again',
        'deprecate_1_higher_w_on_abcdo'
    ]
    MODEL_FOLDER = '/home/mack/stan/stan/stan/model/saved/octopus_models'

    today = dt.now()

    debug = False

    if debug and platform.system() == 'Darwin':
        path_to_data = '/Users/mackdelany/Documents/STAN/stan_model/data/stan_one_debug.csv'
        MODEL_FOLDER = '/Users/mackdelany/Documents/STAN/stan/stan/octopus/saved_models'
        MODELS = [MODELS[0]]
    elif debug:
        path_to_data = '/home/mack/stan/stan_one_debug.csv'
    else:
        path_to_data = '/home/mack/stan/stan_one_training_29_12.csv'

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    dm = OctopusDataManager(device, batch_size=BATCH_SIZE,
                            debug=DEBUG, path_to_data=path_to_data)
    dm.init_val_data()
    class_weights = dm.init_class_weights(return_weights=True)

    for model in MODELS:
        print('\nTesting {}'.format(model))
        model_path = Path(MODEL_FOLDER, model)

        octopus = OctopusModel(device, class_weights)
        octopus.load_params(str(model_path))

        auc = calc_octupus_auc(
            octopus,
            dm,
            intervals=INTERVALS,
            device=device,
            save_folder=MODEL_FOLDER,
            tag=f'{model}_{today.day}_{today.month}_{today.year}_auc'
            )
