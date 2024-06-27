import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, classification_report, confusion_matrix
import numpy as np


def plot_roc_curve(models, x_test_vectorized, y_test, file_path):
    plt.figure(figsize=(10, 8))
    for model_name, model in models.items():
        y_pred_prob = model.predict_proba(x_test_vectorized)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.savefig(file_path)
    plt.close()


def plot_confusion_matrix(models, x_test_vectorized, y_test, file_path):
    plt.figure(figsize=(15, 10))
    for i, (model_name, model) in enumerate(models.items()):
        y_pred = model.predict(x_test_vectorized)
        cm = confusion_matrix(y_test, y_pred, normalize='true')
        plt.subplot(2, 2, i+1)
        sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues')
        plt.title(f'{model_name} Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def plot_classification_report(models, x_test_vectorized, y_test, file_path):
    metrics = ['precision', 'recall', 'f1-score']
    scores = {model_name: [] for model_name in models.keys()}

    for model_name, model in models.items():
        y_pred = model.predict(x_test_vectorized)
        report = classification_report(y_test, y_pred, output_dict=True)
        for metric in metrics:
            scores[model_name].append(report['weighted avg'][metric])

    x = np.arange(len(models))
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 8))
    for i, metric in enumerate(metrics):
        values = [scores[model_name][i] for model_name in models.keys()]
        ax.bar(x + i * width, values, width, label=metric)

    ax.set_xlabel('Models')
    ax.set_ylabel('Scores')
    ax.set_title('Classification Scores by Model')
    ax.set_xticks(x + width)
    ax.set_xticklabels(models.keys())
    ax.legend()
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
