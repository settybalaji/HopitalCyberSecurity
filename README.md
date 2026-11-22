# HopitalCyberSecurity
Generating hospital network dataset...
Dataset generated successfully!
   network_feature_1  network_feature_2  network_feature_3  network_feature_4  \
0          -0.862129           0.282940          -0.771683           1.300791   
1           0.428872          -0.189877          -0.283902           0.702441   
2           7.798377          -1.816815           1.217962          -0.574017   
3           3.750242          -1.675640          -2.597779          -0.915146   
4          -5.173787           3.099287           0.308300          -0.361223   

   network_feature_5  network_feature_6  network_feature_7  network_feature_8  \
0           0.666799          -1.603175           5.908121           5.806372   
1           1.026555           0.168668          -1.230644           1.076932   
2           3.126187           2.069453          -2.643346          -3.399620   
3          -2.671638           0.315427           0.673047          -0.133725   
4           0.063396           0.866936           0.209266           4.171748   

   network_feature_9  network_feature_10  ...  network_feature_12  \
0           3.541950           -1.850519  ...            1.282363   
1           0.785219            3.078306  ...            1.079943   
2          -0.946125            0.029591  ...            0.418897   
3          -1.054220            1.023767  ...            0.759429   
4          -4.932220           -1.204782  ...            1.252061   

   network_feature_13  network_feature_14  network_feature_15  \
0            3.266783           -1.378326            2.403766   
1            2.261500            1.472587           -1.185349   
2           -0.163857            1.381746           -1.604234   
3            2.636592            0.043135            1.267805   
4           -0.464278            0.728914           -0.330517   

   network_feature_16  network_feature_17  network_feature_18  \
0           -2.564709            2.170327            0.599400   
1           -2.039994            0.444338           -4.196636   
2           -3.895575            0.994625           -1.415420   
3            1.236386           -1.678386            4.349249   
4            3.444509           -2.837559           -1.867530   

   network_feature_19  network_feature_20  label  
0           -0.226900            1.455956      0  
1           -0.795092           -4.589576      1  
2           -0.166886           -2.906883      0  
3            0.890790            2.011401      1  
4           -0.477899           -0.528952      1  

[5 rows x 21 columns]

Class distribution:
label
0    6282
1    2718
Name: count, dtype: int64

Preprocessing network data...
Preprocessing completed!

Training centralized AI model...
Centralized model accuracy: 0.9566666666666667

Creating hospital clients...
Hospital 1: 2400 records
Hospital 2: 2400 records
Hospital 3: 2400 records

Starting Federated Learning...
Round 1: Accuracy = 0.8289
Round 2: Accuracy = 0.8289
Round 3: Accuracy = 0.8289
Round 4: Accuracy = 0.8289
Round 5: Accuracy = 0.8289
Round 6: Accuracy = 0.8289
Round 7: Accuracy = 0.8289
Round 8: Accuracy = 0.8289
Round 9: Accuracy = 0.8289
Round 10: Accuracy = 0.8289

Evaluating Federated Model...

FEDERATED LEARNING RESULTS
Accuracy: 0.8289
Precision: 0.7428
Recall: 0.6636
F1 Score: 0.701

Classification Report:
              precision    recall  f1-score   support

      Normal       0.86      0.90      0.88      1256
      Attack       0.74      0.66      0.70       544

    accuracy                           0.83      1800
   macro avg       0.80      0.78      0.79      1800
weighted avg       0.83      0.83      0.83      1800


Running Differential Privacy experiment...
Noisy model accuracy: 0.8267

====================================
 CYBERATTACK DETECTION
====================================

Network activity appears normal.
Attack probability: 33.36 %

====================================
 CLOUD COORDINATION
====================================
Cloud coordinator started.
Hospital 1: Local model update prepared.
Hospital 2: Local model update prepared.
Hospital 3: Local model update prepared.
Global model aggregation completed.
Global model distributed to hospitals.

====================================
 MODEL COMPARISON
====================================
                           Model  Accuracy  Precision    Recall  F1 Score
0      Centralized Random Forest  0.956667   0.936330  0.919118  0.927644
1  Federated Logistic Regression  0.828889   0.742798  0.663603  0.700971
2          Noisy Federated Model  0.826667   0.738683  0.659926  0.697087



====================================
 PROJECT EXECUTION COMPLETED
====================================
Dataset: Generated successfully
Hospitals: 3
Federated Rounds: 10
Centralized Accuracy: 0.9567
Federated Accuracy: 0.8289
Noisy Model Accuracy: 0.8267

Generated files:
dataset/hospital_network.csv
results/model_comparison.csv
results/confusion_matrix.png
results/federated_accuracy.png
models/federated_model.pkl

SMART HOSPITAL CYBERSECURITY SYSTEM FINISHED!
