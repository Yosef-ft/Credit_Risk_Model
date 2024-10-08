import matplotlib.pyplot as plt
import seaborn as sns
import scorecardpy as sc

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve, precision_score, recall_score, f1_score


class Evaluation:

    def evaluate(self, y_pred, y_test, X_test, model):
        '''
        This funtion calculates the accuracy, precision, recall and f1 score for a given y_pred, y_test
        '''
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        class_proba = model.predict_proba(X_test)[:, 1]

        roc_auc = roc_auc_score(y_test, class_proba)


        print(f"Accuracy      : {accuracy:.4f}")
        print(f"Precision     : {precision:.4f}")
        print(f"Recall        : {recall:.4f}")
        print(f"F1 Score      : {f1:.4f}")
        print(f"Roc Auc Score : {roc_auc:.4f}")


    def plot_confusion_matrix(self, y_test, y_pred):
        '''
        This funtion calculates the confusion_matrix for a given model
        '''

        cm = confusion_matrix(y_test, y_pred)

        # Plot confusion matrix
        plt.figure(figsize=(5, 3))
        sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', cbar=False)

        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()


    def plot_roc_curve(self, y_test, X_test, model):
        '''
        This funtion plots roc curve for a given model

        Parameter:
        ---------
            y_test
            X_test
            model: models(like logistic regression, .....)
        '''

        class_proba = model.predict_proba(X_test)[:, 1]
        
        roc_auc = roc_auc_score(y_test, class_proba)

        fpr, tpr, thresholds = roc_curve(y_test, class_proba)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='grey', linestyle='--')

        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend(loc='lower right')
        plt.grid(True)
        plt.show()  


    def roc_with_sc(self, model, X_train, X_test, y_test, y_train):
        '''
        This funcion plots roc curve using the scorecard library for detailed analysis
        '''
        train_pred = model.predict_proba(X_train)[:,1]
        test_pred = model.predict_proba(X_test)[:,1]
        train_perf = sc.perf_eva(y_train, train_pred, title = "train")
        test_perf = sc.perf_eva(y_test, test_pred, title = "test")