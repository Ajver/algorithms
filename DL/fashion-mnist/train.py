import datetime
import time
from pathlib import Path

from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers.tensorboard import TensorBoardLogger
from pytorch_lightning.trainer.trainer import Trainer
import json

from Model import Model, ModelParams
from Datamodule import Datamodule

OUT_FEATURES = 10

datamodule = Datamodule()
datamodule.prepare_data()
datamodule.setup("fit")

start_time = time.time()
date_now = datetime.datetime.now()
print(f"Date now: {date_now}")

save_dir = Path(f"./checkpoints/run_{date_now}")
save_dir.mkdir(parents=True, exist_ok=False)

model_params = ModelParams(
    dropout_rate=0.05,
    n_hidden=1,
    n_width=128,
    lr=0.001,
)
with open(save_dir/"model_params.json", "w") as f:
    s = json.dumps(model_params.model_dump(), indent="\t")
    f.write(s)


total_score = 0.0
for fold, train_loader, val_loader in datamodule.cv_train_val_splits():
    print(f"Starting new training {fold=}")

    logger = TensorBoardLogger(
        "runs",
        name="train",
        version=f"fold{fold}",
    )

    checkpoint_callback = ModelCheckpoint(
        dirpath=save_dir/f"fold{fold}/",
        filename="model-{epoch:02d}-{val_loss:.3f}",
        monitor="val_loss",
        mode="min",
        save_top_k=1,
        save_last=False,
    )

    model = Model(fold, OUT_FEATURES, model_params)
    trainer = Trainer(
        max_epochs=30,
        callbacks=[checkpoint_callback],
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
