# Machine Learning-Based Web Application Firewall (WAF)

## Overview
This project implements a **Web Application Firewall (WAF)** using machine learning and deep learning techniques. The WAF detects web-based threats and provides a simulated interface for testing attack scenarios. The project also includes a comprehensive analysis of the model performance.

---

## Features
- **Machine Learning Models**: Random Forest, SVM.
- **Deep Learning Models**: LSTM, CNN, and CNN-LSTM.
- **Threat Detection**: Identifies various web attacks.
- **Web Interface**: Allows users to simulate attack requests and view detection results.
- **Performance Metrics**: Accuracy, Precision, Recall, F1-Score, Confusion Matrices, ROC Curves.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries/Frameworks**: 
  - Machine Learning: Scikit-learn, XGBoost
  - Deep Learning: TensorFlow, Keras
  - Data Handling: Pandas, NumPy
  - Visualization: Matplotlib, Seaborn
- **Web Framework**: Flask
- **Network Analysis**: Scapy
- **Environment Management**: Anaconda

---

## Datasets
Code for processing the datasets is located in the `Dataset` directory. To run the data cleaning notebooks, download the required datasets and place them in the `Dataset` directory.

- **ECML/PKDD 2007 dataset**: [Download Here](http://www.lirmm.fr/pkdd2007-challenge/)
- **HTTP Parameters dataset**: [Download Here](https://github.com/Morzeux/HttpParamsDataset)
- **XSS dataset**: [Download Here](https://www.kaggle.com/syedsaqlainhussain/cross-site-scripting-xss-dataset-for-deep-learning)

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/waf-ml-project.git
