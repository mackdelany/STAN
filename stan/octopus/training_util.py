
from pathlib import Path

import pandas as pd
import torch

def get_accuracy(pred: torch.tensor, labels: torch.tensor) -> float:
    assert pred.shape[0] == labels.shape[0]
    correct = torch.sum(pred==labels)
    acc = (correct / pred.shape[0]).item()
    return acc

def get_rmse(pred: torch.tensor, labels: torch.tensor) -> float:
    assert pred.shape[0] == labels.shape[0]
    mse = torch.sum((pred - labels)**2) / pred.shape[0]
    rmse = (mse**0.5).item()
    return rmse

def get_confusion_matrix(pred: torch.tensor, labels: torch.tensor, rates=False) -> float:
    tp = torch.sum(torch.logical_and(pred==1, labels==1))
    fp = torch.sum(torch.logical_and(pred==1, labels==0))
    tn = torch.sum(torch.logical_and(pred==0, labels==0))
    fn = torch.sum(torch.logical_and(pred==0, labels==1))
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    cm = {
        'tp': tp.item(), 'fp': fp.item(), 'tn': tn.item(), 'fn': fn.item(), 
        'precision': precision.item(), 'recall': recall.item()
        }
    if rates:
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)
        cm.update({'tpr': tpr.item(), 'fpr': fpr.item()})
    return cm

def pd_series_to_tensor(series, tensor_type_match=None):
    tensor = torch.tensor(series)
    if tensor_type_match:
        tensor = tensor.astype(tensor_type_match)
    return tensor

def concat_tensors_in_dict(new_dict, old_dict=None):
    """Concats all tensors in dict b into dict a. Tensors must have same keys.

    Args:
        - new_dict: dictionary of tensors
        - old_dict: dictionary of tensors
    """
    if old_dict:
        for tensor in old_dict:
            old_dict[tensor] = torch.cat([old_dict[tensor], new_dict[tensor]])
            assert old_dict[tensor][-1,0] == new_dict[tensor][-1,0]
        return old_dict
    return new_dict

def record_octopus_metrics(metrics, save_folder, tag):
    def flatten_dict(old_dict, key_to_keep=None):
        if key_to_keep:
            edited_dict = {}
            for old_key in old_dict:
                edited_dict[('{}_{}'.format(key_to_keep, old_key))] = old_dict[old_key]
            old_dict = edited_dict
        new_dict = {}
        for key in old_dict:
            if isinstance(old_dict[key], dict):
                flattened_dict = flatten_dict(old_dict[key], key_to_keep=key)
                new_dict.update(flattened_dict)
            else:
                new_dict.update({key: old_dict[key]})
        return new_dict

    metrics = flatten_dict(metrics)

    file_path = Path(save_folder, '{}_metrics.csv'.format(tag))
    if file_path.exists():
        metrics_file = pd.read_csv(str(file_path))
        metrics_file = metrics_file.append(metrics, ignore_index=True)
        metrics_file.to_csv(str(file_path), index=False)
    else:
        metrics_file = pd.DataFrame(metrics, index=[0])
        metrics_file.to_csv(str(file_path), index=False)