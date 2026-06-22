import time

from pytorch_lightning.loggers.tensorboard import TensorBoardLogger
from pytorch_lightning.trainer.trainer import Trainer

from Model import Model
from Datamodule import Datamodule

OUT_FEATURES = 10

datamodule = Datamodule()
datamodule.prepare_data()
datamodule.setup("fit")


logger = TensorBoardLogger(
    "runs",
    name="train",
)

start_time = time.time()

dropout_rate = 0.05
n_hidden = 1
n_width = 128
lr = 0.001

total_score = 0.0
for fold, train_loader, val_loader in datamodule.cv_train_val_splits():
    print(f"Starting new training {fold=}")

    model = Model(fold, dropout_rate, n_hidden, n_width, OUT_FEATURES, lr)
    trainer = Trainer(
        max_epochs=20,
        devices=1,
        fast_dev_run=False,
        enable_checkpointing=True,
        enable_progress_bar=False,
        logger=logger,
    )
    trainer.fit(model, train_loader, val_loader)
    result = trainer.validate(model, val_loader)

    total_score += result[0]["val_accuracy"]

avg_score = total_score / 5
print(f"\nAverage score: {avg_score:.3f}")

print(f"\nRun duration: {time.time() - start_time}s")
