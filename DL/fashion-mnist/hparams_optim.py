import json
import time

from pytorch_lightning.loggers.tensorboard import TensorBoardLogger
from pytorch_lightning.trainer.trainer import Trainer
import optuna

from Model import Model
from Datamodule import Datamodule

OUT_FEATURES = 10

datamodule = Datamodule()
datamodule.prepare_data()
datamodule.setup("fit")


def objective(trial):
    logger = TensorBoardLogger(
        "runs",
        name="hparams",
        version=f"trial_{trial.number}",
        default_hp_metric=False
    )

    dropout_rate = trial.suggest_float("dropout_rate", 0, 0.4)
    n_hidden = trial.suggest_int("n_hidden", 1, 5)
    n_width = trial.suggest_categorical("n_width", [16, 32, 64, 128, 256])
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)

    total_score = 0.0
    for fold, train_loader, val_loader in datamodule.cv_train_val_splits():
        print(f"Starting new training {trial.number=} {fold=}")

        model = Model(fold, dropout_rate, n_hidden, n_width, OUT_FEATURES, lr)
        trainer = Trainer(
            max_epochs=5,
            devices=1,
            fast_dev_run=False,
            enable_checkpointing=False,
            enable_progress_bar=False,
            logger=logger,
        )
        trainer.fit(model, train_loader, val_loader)
        result = trainer.validate(model, val_loader)

        total_score += result[0]["val_accuracy"]

    avg_score = total_score / 5

    metrics = {"accuracy": avg_score}
    logger.log_hyperparams(trial.params, metrics)
    logger.log_metrics(metrics, step=0)

    return avg_score


start_time = time.time()

study = optuna.create_study(study_name="hparams", direction="maximize")
study.optimize(objective, n_trials=50)

print(f"\nRun duration: {time.time() - start_time}s")


with open("best_params.json", "w") as f:
    params = study.best_params.copy()
    params["score"] = study.best_value
    s = json.dumps(params, indent=4)
    f.write(s)
