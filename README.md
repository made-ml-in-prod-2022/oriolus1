Чтобы запустить train с моделью random forest:

python ml_project/train_pipeline.py ml_project/configs/forest_train_config.yaml

Чтобы запустить train с моделью logistic regression:

python ml_project/train_pipeline.py ml_project/configs/logistic_train_config.yaml

Чтобы запустить inference:

python ml_project/predict_pipeline.py ml_project/configs/predict_config.yaml

Чтобы запустить тесты:

pytest tests/test_all.py