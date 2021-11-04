# Cement_quality_prediction
Dash application , how to predict   cement quality with Machine learning The  WEB application is designed to demonstrate how different machine learning models predict cement compressive strength. The target or predicted variables can be 7days and 28 days compressive strength as well.

To get the application working is necessary:
1.	Git  clone https://github.com/Igor-Konnov/Cement_quality_prediction.git
2.	To add 2 datasets,  data.csv, data2.csv  with predictors and predicted variables.
3.	Change columns(predictors and target ) name if different in content.py, stat.py 

Files structure :
/dash-slides
   /assets
   /slides
     -content.py
     -graph.py
     -introduction.py
     -reference.py
     -stat.py
     -table.py

   index.py
   app.py
   presentation.py
   utils.py – the file consists of  Ml models list, change if necessary, or to turn the hyperparameters. 

requirements.txt : 

dash                               1.21.0
dash-bootstrap-components          0.13.0
scipy                              1.6.2
statsmodels                        0.12.2 
