
from pathlib import Path
import sys

sys.path.append('../core')

import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from .training_util import concat_tensors_in_dict, get_accuracy, get_confusion_matrix, get_rmse, record_octopus_metrics
from .octopus_model import OctopusModel
from .octopus_data_manager import OctopusDataManager


class OctopusTrainer():
    OPTIMISATION_WEIGHTINGS = {
        'tc_acc_one': 0.13,
        'tc_acc_two': 0.25,
        'tc_acc_three': 0.3,
        'tc_acc_four': 0.25,
        'tc_acc_five': 0.13
    }

    def __init__(
        self,
        path_to_data='/Users/mackdelany/Documents/STAN/stan_model/data/stan_one_training_23_12.csv',
        batch_size=8,
        optimizer='ADAM',
        learning_rate=0.0001,
        debug=False,
        thres_dict=None,
        save_folder=None,
        training_run='test',
        save_folder_exists=False,
        save_state_limit=2
        ):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print('Using device: {}'.format(self.device))
        self.debug = debug
        if self.debug:
            print('\n{}\nIN DEBUG MODE\n{}\n'.format(90*'-', 90*'-'))
        
        self.training_run = training_run
        self._save_folder = save_folder if save_folder else Path(Path.cwd(), training_run)
        if self._save_folder.exists() and not save_folder_exists and training_run != 'dbg': #TODO add ability for dbg folder
            raise ValueError("Save folder already exists - don't overwrite something?")
        self._save_folder.mkdir()
        self._saved_states_loss = {}
        self._saved_states_eval = {}
        self._save_state_limit = save_state_limit

        self._load_data(batch_size=batch_size, path_to_data=path_to_data, device=self.device)
        self._init_class_weights()
        self._load_model()
        self._init_thresholds(thres_dict)
        self._load_optimizer(optimizer, learning_rate)

        self._min_tc_loss = 10000
        self._max_opt_metric = 0

    def _load_data(self, batch_size, path_to_data, device):
        ## dm for data_manager
        self.dm = OctopusDataManager(device, batch_size=batch_size, debug=self.debug, path_to_data=path_to_data)
        self.dm.init_val_data()

    def _init_class_weights(self):
        self.class_weights = self.dm.init_class_weights(return_weights=True)
    
    def _load_model(self):
        self.model = OctopusModel(self.device, self.class_weights)
       
    def _init_thresholds(self, thres_dict=None):
        if thres_dict:
            raise ValueError('Thresholds already set')
        else:
            self.y2_thres = 0.5
            self.y3_thres = 0.5
            self.y4_thres = 0.5
            self.y5_thres = 0.5
            self.y6_thres = 0.5
            self.y7_thres = 0.5
            self.y8_thres = 0.5
            self.y9_thres = 0.5

    def _load_optimizer(self, optimizer, learning_rate):
        print('\nLoading optimizer: {} with lr {}'.format(optimizer, learning_rate))
        if optimizer == 'ADAM':
            self.optimizer = torch.optim.Adam(self.model.model_params, lr=learning_rate)
        else:
            raise ValueError('No other optimizers currently supported')
        self.lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, factor=0.3, patience=5000, verbose=True, min_lr=0.000001
            )

    def _toggle_distilbert_grad(self, requires_grad: bool):
        for param in self.model.distilbert.parameters():
            param.requires_grad = True
        for param in self.model.pooling_layer.parameters():
            param.requires_grad = requires_grad

    def _toggle_tc_grad(self, requires_grad: bool):
        for param in self.model.tc_classifier.parameters():
            param.requires_grad = requires_grad

    def _toggle_abcd_grad(self, requires_grad: bool):
        for param in self.model.abcd_classifier.parameters():
            param.requires_grad = requires_grad

    def _toggle_outcome_grad(self, requires_grad: bool):
        for param in self.model.sepsis_classifier.parameters():
            param.requires_grad = requires_grad    
        
    def _save_state_loss(self, step, loss):
        save_path = Path(self._save_folder, 'state_dict_step_{}'.format(step))
        torch.save(self.model.state_dict(), str(save_path))
        print('Saving state dict to {}'.format(save_path))
        self._saved_states_loss.update({loss: save_path})
        if len(self._saved_states_loss) > self._save_state_limit:
            max_saved_loss = max(self._saved_states_loss.keys())
            path_to_delete = self._saved_states_loss.pop(max_saved_loss)
            print('Max saved loss is {}, removing {}'.format(max_saved_loss, path_to_delete))
            path_to_delete.unlink()

    def _save_state_opt_eval(self, step, opt):
        save_path = Path(self._save_folder, 'state_dict_step_{}'.format(step))
        torch.save(self.model.state_dict(), str(save_path))
        print('Saving state dict to {}'.format(save_path))
        self._saved_states_eval.update({opt: save_path})
        if len(self._saved_states_eval) > self._save_state_limit:
            max_saved_opt = max(self._saved_states_eval.keys())
            path_to_delete = self._saved_states_eval.pop(max_saved_opt)
            print('Max saved opt metric is {}, removing {}'.format(max_saved_opt, path_to_delete))
            path_to_delete.unlink()

    
    def _do_evaluation(self, eval_batch_size=100, step=None):
        print('\nEvaluating model')

        with torch.no_grad():

            #pointers for readability...
            input_ids = self.dm.val_encodings['input_ids'].to(self.device)
            attn_mask = self.dm.val_encodings['attention_mask'].to(self.device)

            outputs, val_examples = self.model.infer_in_batches(input_ids, attn_mask, eval_batch_size)

            abcd_probs = outputs['abcd_probs']
            sepsis_probs = outputs['sepsis_probs']

            y2_probs = torch.masked_select(abcd_probs[:, 0], self.dm.abcd_val_context_mask)
            y3_probs = torch.masked_select(abcd_probs[:, 1], self.dm.abcd_val_context_mask)
            y4_probs = torch.masked_select(abcd_probs[:, 2], self.dm.abcd_val_context_mask)
            y5_probs = torch.masked_select(abcd_probs[:, 3], self.dm.abcd_val_context_mask)
            y6_probs = torch.masked_select(abcd_probs[:, 4], self.dm.abcd_val_context_mask)
            y7_probs = torch.masked_select(abcd_probs[:, 5], self.dm.abcd_val_context_mask)
            y8_probs = torch.masked_select(abcd_probs[:, 6], self.dm.abcd_val_context_mask)
            sepsis_probs = torch.masked_select(sepsis_probs[:, 0], self.dm.outcome_val_context_mask)
            
            y2_pred = (y2_probs > self.y2_thres).long()
            y3_pred = (y3_probs > self.y3_thres).long()
            y4_pred = (y4_probs > self.y4_thres).long()
            y5_pred = (y5_probs > self.y5_thres).long()
            y6_pred = (y6_probs > self.y6_thres).long()
            y7_pred = (y7_probs > self.y7_thres).long()
            y8_pred = (y8_probs > self.y8_thres).long()
            y9_pred = (sepsis_probs > self.y9_thres).long()

            """
            Funcs exported to octopus_core #TODO check that still works
            """

            # triage code
            tc_pred = outputs['tc_probs'].argmax(1)
            tc_accuracy = get_accuracy(tc_pred, self.dm.y1_val_tensor)
            tc_rmse = get_rmse(tc_pred, self.dm.y1_val_tensor)

            tc_pred_cpu = tc_pred.cpu()

            self.dm.val_df['tc_pred'] = tc_pred_cpu
            val_df = self.dm.val_df

            def get_tc_code_accuracy_from_val_df(val_df, tc):
                correct = val_df[(val_df.y1_triage_code==tc) & (val_df['y1_triage_code']==val_df['tc_pred'])].shape[0]
                tc_example_count = sum(val_df.y1_triage_code==tc)
                tc_accuracy = correct / tc_example_count
                return tc_accuracy

            def get_tc_context_accuracy_from_val_df(val_df, context):
                if context not in ['FAST', 'VITAL', 'FULL']:
                    raise
                correct = val_df[(val_df.data_class.str.contains(context)) & (val_df['y1_triage_code']==val_df['tc_pred'])].shape[0]
                ex_count = sum((val_df.data_class.str.contains(context)))
                acc = correct / ex_count
                return acc

            # triage code offset by 1!!
            tc_acc_one = get_tc_code_accuracy_from_val_df(val_df, 0)
            tc_acc_two = get_tc_code_accuracy_from_val_df(val_df, 1)
            tc_acc_three = get_tc_code_accuracy_from_val_df(val_df, 2)
            tc_acc_four = get_tc_code_accuracy_from_val_df(val_df, 3)
            tc_acc_five = get_tc_code_accuracy_from_val_df(val_df, 4)

            tc_acc_fast = get_tc_context_accuracy_from_val_df(val_df, 'FAST')
            tc_acc_vital = get_tc_context_accuracy_from_val_df(val_df, 'VITAL')
            tc_acc_full = get_tc_context_accuracy_from_val_df(val_df, 'FULL')

            # abcd 
            airway_accuracy = get_accuracy(y2_pred, self.dm.y2_val_tensor)
            breathing_accuracy = get_accuracy(y3_pred, self.dm.y3_val_tensor)
            circulation_accuracy = get_accuracy(y4_pred, self.dm.y4_val_tensor)
            disability_accuracy = get_accuracy(y5_pred, self.dm.y5_val_tensor)
            neuro_accuracy = get_accuracy(y6_pred, self.dm.y6_val_tensor)
            immunocompromised_accuracy = get_accuracy(y7_pred, self.dm.y7_val_tensor)
            mental_health_accuracy = get_accuracy(y8_pred, self.dm.y8_val_tensor)

            airway_cm = get_confusion_matrix(y2_pred, self.dm.y2_val_tensor)
            breathing_cm = get_confusion_matrix(y3_pred, self.dm.y3_val_tensor)
            circulation_cm = get_confusion_matrix(y4_pred, self.dm.y4_val_tensor)
            disability_cm = get_confusion_matrix(y5_pred, self.dm.y5_val_tensor)
            neuro_cm = get_confusion_matrix(y6_pred, self.dm.y6_val_tensor)
            immunocompromised_cm = get_confusion_matrix(y7_pred, self.dm.y7_val_tensor)
            mental_health_cm = get_confusion_matrix(y8_pred, self.dm.y8_val_tensor)

            # other
            sepsis_accuracy = get_accuracy(y9_pred, self.dm.y9_val_tensor)
            sepsis_cm = get_confusion_matrix(y9_pred, self.dm.y9_val_tensor)

            metrics = {
                'step': step,
                'tc_accuracy': tc_accuracy,
                'tc_rmse': tc_rmse,
                'tc_acc_one': tc_acc_one,
                'tc_acc_two': tc_acc_two,
                'tc_acc_three': tc_acc_three,
                'tc_acc_four': tc_acc_four,
                'tc_acc_five': tc_acc_five,
                'tc_acc_fast': tc_acc_fast,
                'tc_acc_vital': tc_acc_vital,
                'tc_acc_full': tc_acc_full,
                'airway_accuracy': airway_accuracy,
                'breathing_accuracy': breathing_accuracy,
                'circulation_accuracy': circulation_accuracy,
                'disability_accuracy': disability_accuracy,
                'neuro_accuracy': neuro_accuracy,
                'immunocompromised_accuracy': immunocompromised_accuracy,
                'mental_health_accuracy': mental_health_accuracy,
                'sepsis_accuracy': sepsis_accuracy,
                'airway_cm': airway_cm,
                'breathing_cm': breathing_cm,
                'circulation_cm': circulation_cm,
                'disability_cm': disability_cm,
                'neuro_cm': neuro_cm,
                'immunocompromised_cm': immunocompromised_cm,
                'mental_health_cm': mental_health_cm,
                'sepsis_cm': sepsis_cm
                }

            return metrics


    
    def train(self, epochs=20, db_train_epochs=10, eval_batch_size=100, eval_cadence=500, save_after=2000):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print('Using device: {}'.format(device))

        print('\nTraining model for {} epochs'.format(epochs))
        self.model.train()  # ensure model is set to train
        global_step = 0

        ####################
        ## Set context
        ####################
        for epoch in range(1, epochs):
            for context in self.dm.train_contexts:
                print('\nEpoch {}, {}'.format(epoch, context))
                
                ####################
                ## Decide what layers are trainable
                ####################
                if epoch <= db_train_epochs:
                    self._toggle_distilbert_grad(True)
                else:
                    self._toggle_distilbert_grad(False)

                if context in self.dm.triage_code_contexts:
                    self._toggle_tc_grad(True)
                else:
                    self._toggle_tc_grad(False)

                if context in self.dm.abcd_contexts:
                    self._toggle_abcd_grad(True)
                else:
                    self._toggle_abcd_grad(False)

                if context in self.dm.outcome_contexts:
                    self._toggle_outcome_grad(True)
                else:
                    self._toggle_outcome_grad(False)


                for i_batch, batch in enumerate(self.dm.train_contexts[context]):
                    global_step += 1
                    
                    ####################
                    ## Training step
                    ####################
                    batch['X']['input_ids'] = batch['X']['input_ids'].to(self.device)
                    batch['X']['attention_mask'] = batch['X']['attention_mask'].to(self.device)
                    batch['labels']['y1_triage_code'] = batch['labels']['y1_triage_code'].to(self.device)
                    batch['labels']['y2_airway_altered'] = batch['labels']['y2_airway_altered'].to(self.device)
                    batch['labels']['y3_breathing_altered'] = batch['labels']['y3_breathing_altered'].to(self.device)
                    batch['labels']['y4_circulation_altered'] = batch['labels']['y4_circulation_altered'].to(self.device)
                    batch['labels']['y5_disability_altered'] = batch['labels']['y5_disability_altered'].to(self.device)
                    batch['labels']['y6_neuro_altered'] = batch['labels']['y6_neuro_altered'].to(self.device)
                    batch['labels']['y7_immunocompromised'] = batch['labels']['y7_immunocompromised'].to(self.device)
                    batch['labels']['y8_mental_health'] = batch['labels']['y8_mental_health'].to(self.device)
                    batch['labels']['y9_sepsis'] = batch['labels']['y9_sepsis'].to(self.device)

                    outputs = self.model.forward(batch['X'])
                    losses = self.model.calculate_losses(batch['labels'], outputs)
                    
                    if global_step > 1:
                        lr_list = self.lr_scheduler._last_lr
                        current_lr = sum(lr_list) / len(lr_list)
                    else:
                        current_lr = 0.00001

                    self.record_losses(losses, global_step, current_lr)

                    if losses['tc_loss'] < self._min_tc_loss and save_after < global_step:
                        print('\nNew min loss: {}, saving state..'.format(losses['tc_loss']))
                        self._min_tc_loss = losses['tc_loss']
                        self._save_state_loss(global_step, losses['tc_loss'])

                    # zero grad with optimizer ?
                    self.optimizer.zero_grad()

                    # propogate gradients
                    if context in self.dm.abcd_contexts:
                        losses['abcd_loss'].backward(retain_graph=True)
                    if context in self.dm.outcome_contexts:
                        losses['sepsis_loss'].backward(retain_graph=True)
                    losses['tc_loss'].backward()

                    # optimizer step
                    self.optimizer.step()
                    self.lr_scheduler.step(losses['tc_loss'].item())

                    if global_step % 50 == 0:
                        print('Step {}'.format(global_step))
                        print('\nTriage code loss: {}\nABCD loss: {}\nSepsis loss: {}'.format(losses['tc_loss'], losses['abcd_loss'], losses['sepsis_loss']))
                    
                    if (global_step % eval_cadence == 0) or (global_step == 1):
                        print('Evaluating...')
                        print('Epoch {}/{} {} iteration {}'.format(epoch, epochs, context, i_batch))

                        self.model.eval()  # set mode to eval
                        metrics = self._do_evaluation(eval_batch_size=eval_batch_size, step=global_step)
                        self.model.train()  # change mode back to train

                        #HACK
                        opt_metric = (
                            (OctopusTrainer.OPTIMISATION_WEIGHTINGS['tc_acc_one'] * metrics['tc_acc_one']) +
                            (OctopusTrainer.OPTIMISATION_WEIGHTINGS['tc_acc_two'] * metrics['tc_acc_two']) +
                            (OctopusTrainer.OPTIMISATION_WEIGHTINGS['tc_acc_three'] * metrics['tc_acc_three']) +
                            (OctopusTrainer.OPTIMISATION_WEIGHTINGS['tc_acc_four'] * metrics['tc_acc_four']) +
                            (OctopusTrainer.OPTIMISATION_WEIGHTINGS['tc_acc_five'] * metrics['tc_acc_five'])
                            )

                        print('\nOpt metric: {}'.format(opt_metric))
                        if opt_metric > self._max_opt_metric and save_after < global_step:
                            print('\nNew min loss: {}, saving state..'.format(losses['tc_loss']))
                            self._max_opt_metric = opt_metric
                            self._save_state_opt_eval(global_step, losses['tc_loss'])

                        print('\nTriage code evaluation\nAccuracy: {}\nRMSE:{}'.format(metrics['tc_accuracy'], metrics['tc_rmse']))

                        print('\nABCD evaluation')
                        print('Airway precision: {}'.format(metrics['airway_cm']['precision']))
                        print('Airway recall: {}'.format(metrics['airway_cm']['recall']))
                        print('Breathing precision: {}'.format(metrics['breathing_cm']['precision']))
                        print('Breathing recall: {}'.format(metrics['breathing_cm']['recall']))
                        print('Circulation precision: {}'.format(metrics['circulation_cm']['precision']))
                        print('Circulation recall: {}'.format(metrics['circulation_cm']['recall']))
                        print('Disability precision: {}'.format(metrics['disability_cm']['precision']))
                        print('Disability recall: {}'.format(metrics['disability_cm']['recall']))
                        print('Neuro precision: {}'.format(metrics['neuro_cm']['precision']))
                        print('Neuro recall: {}'.format(metrics['neuro_cm']['recall']))
                        print('Immunocompromised precision: {}'.format(metrics['immunocompromised_cm']['precision']))
                        print('Immunocompromised recall: {}'.format(metrics['immunocompromised_cm']['recall']))
                        print('Mental health precision: {}'.format(metrics['mental_health_cm']['precision']))
                        print('Mental health recall: {}'.format(metrics['mental_health_cm']['recall']))

                        print('\nSepsis evaluation')
                        print('Sepsis accuracy: {}'.format(metrics['sepsis_accuracy']))
                        print('Precision: {}'.format(metrics['sepsis_cm']['precision']))
                        print('Recall: {}'.format(metrics['sepsis_cm']['recall']))
                        print('True positives: {}'.format(metrics['sepsis_cm']['tp']))
                        print('False positives: {}'.format(metrics['sepsis_cm']['fp']))
                        print('True negatives: {}'.format(metrics['sepsis_cm']['tn']))
                        print('False negatives: {}'.format(metrics['sepsis_cm']['fn']))

                        metrics.update({'current_lr': current_lr}) #TODO do this better ? 
                        record_octopus_metrics(metrics, self._save_folder, self.training_run)

    def record_losses(self, losses, global_step, current_lr):
        """
        """
        losses = {
            'step': global_step,
            'current_lr': current_lr,
            'tc_loss': losses['tc_loss'].item(),
            'abcd_loss': losses['abcd_loss'].item(),
            'sepsis_loss': losses['sepsis_loss'].item()
            }
        file_path = Path(self._save_folder, '{}_losses.csv'.format(self.training_run))
        if file_path.exists():
            losses_file = pd.read_csv(str(file_path))
            losses_file = losses_file.append(losses, ignore_index=True)
            losses_file.to_csv(str(file_path), index=False)
        else:
            losses_file = pd.DataFrame(losses, index=[0])
            losses_file.to_csv(str(file_path), index=False)



if __name__ == '__main__':
    import platform
    import sys

    training_run = sys.argv[1]
    if 'debug' in sys.argv:
        debug = True
    else:
        debug = False

    if not debug and Path('{}_metrics.csv'.format(training_run)).exists():
        raise

    if debug and platform.system() == 'Darwin':
        path_to_data = '/Users/mackdelany/Documents/STAN/stan_model/data/stan_one_debug.csv'
    elif debug:
        path_to_data = '/home/mack/stan/stan_one_debug.csv'
    elif platform.system() == 'Darwin':
        path_to_data = '/Users/mackdelany/Documents/STAN/stan_model/data/stan_one_training_29_12.csv'
    else:
        path_to_data = '/home/mack/stan/stan_one_training_29_12.csv'

    x = OctopusTrainer(
        learning_rate=0.00001,
        batch_size=64, 
        debug=debug, 
        path_to_data=path_to_data,
        training_run=training_run
        )  

    x.train()