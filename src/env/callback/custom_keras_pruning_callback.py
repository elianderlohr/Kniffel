from typing import Dict
from typing import Optional
import warnings

import optuna

with optuna._imports.try_import() as _imports:
    from keras.callbacks import Callback

if not _imports.is_successful():
    Callback = object  # NOQA

import numpy as np


class CustomKerasPruningCallback(Callback):
    """Keras callback to prune unpromising trials.

    See `the example <https://github.com/optuna/optuna-examples/blob/main/
    keras/keras_integration.py>`__
    if you want to add a pruning callback which observes validation accuracy.

    Args:
        trial:
            A :class:`~optuna.trial.Trial` corresponding to the current evaluation of the
            objective function.
        monitor:
            An evaluation metric for pruning, e.g., ``val_loss`` and
            ``val_accuracy``. Please refer to `keras.Callback reference
            <https://keras.io/callbacks/#callback>`_ for further details.
        interval:
            Check if trial should be pruned every n-th epoch. By default ``interval=1`` and
            pruning is performed after every epoch. Increase ``interval`` to run several
            epochs faster before applying pruning.
    """

    log_dict = {}

    def __init__(
        self, trial: optuna.trial.Trial, monitor: str, interval: int = 1
    ) -> None:
        super().__init__()

        _imports.check()

        self._trial = trial
        self._monitor = monitor
        self._interval = interval
        self.log_dict = {}
        self.log_dict["episode_reward"] = []
        self.log_dict["nb_episode_steps"] = []
        self.log_dict["nb_steps"] = []

    def _calculate_custom_metric(self, l: list):
        sm_list = [np.power(v, 2) if v > 0 else -1 * np.power(v, 2) for v in l]
        return np.mean(sm_list)

    def on_epoch_end(self, epoch: int, logs: Optional[Dict[str, float]] = None) -> None:

        self.log_dict["episode_reward"].append(float(logs["episode_reward"]))
        self.log_dict["nb_episode_steps"].append(int(logs["nb_episode_steps"]))
        self.log_dict["nb_steps"].append(int(logs["nb_steps"]))

        if (epoch + 1) % self._interval != 0:
            return

        logs = logs or {}
        # implement custom metric

        episode_reward_custom = self._calculate_custom_metric(
            self.log_dict["episode_reward"]
        )
        nb_episode_steps_custom = self._calculate_custom_metric(
            self.log_dict["nb_episode_steps"]
        )

        if self._monitor == "episode_reward":
            current_score = float(episode_reward_custom)
        elif self._monitor == "nb_episode_steps":
            current_score = float(nb_episode_steps_custom)
        else:
            current_score = float(
                episode_reward_custom + (nb_episode_steps_custom * 10)
            )

        if self.log_dict[self._monitor] is None:
            message = (
                "The metric '{}' is not in the evaluation logs for pruning. "
                "Please make sure you set the correct metric name.".format(
                    self._monitor
                )
            )
            warnings.warn(message)
            return

        self._trial.report(float(current_score), step=epoch)

        self.log_dict["episode_reward"] = []
        self.log_dict["nb_episode_steps"] = []
        self.log_dict["nb_steps"] = []

        if self._trial.should_prune():
            message = "Trial was pruned at epoch {}.".format(epoch)
            raise optuna.TrialPruned(message)
