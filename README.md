# Darbuka Tone Classification

A system to identify from the basic tone and tone pattern darbuka musical instrument using [Onset Detection](https://musicinformationretrieval.com/onset_detection.html), [Mel-Frequency Cepstral Coefficient (MFCC) algorithm](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum), and [K-Nearest Neighbor (KNN) algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)

**![#f03c15](https://via.placeholder.com/15/f03c15/f03c15.png)  The tone identification functions, machine learning models, and the darbuka tone dataset are excluded in this repository. Please contact [hairullana99@gmail.com](mailto:hairullana99@gmail.com) if you want to request a function and darbuka tone dataset**

![models](https://user-images.githubusercontent.com/56705867/179347929-57c55de2-380c-4dc5-8904-4b1d7e2232a5.png)
 ![functions](https://user-images.githubusercontent.com/56705867/175550539-05dab479-7d95-4378-ba87-13783e362828.png) ![dataset](https://user-images.githubusercontent.com/56705867/175552431-4af963e2-e05d-4fe9-b8df-0349750972c3.png)


# Features

* **Training Dataset**
  * Description: Perform extraction using MFCC on the training data then save it into the database
  * Parameter: frame length, overlap, coefficients
* **Testing Dataset**
  * Description: Identify Darbuka Basic Tone and Tone Pattern
  * Parameter: K (KNN)
  * Type of Identification:
    * **Basic Tone**: basic tone identification from file input
    * **Tone Pattern**: tone pattern identification from file input with onset detection
    * **Basic Tone**: basic tone identification from dataset and display system accuracy
    * **Basic Tone**: tone pattern identification from dataset and display system accuracy
  

# Technology used in the System

* Python v3.9.7
  * django v4.0.3 (backend framework)
  * librosa v0.9.1 (python module for audio and music processing)
  * pydub v0.25.1 (manipulate audio with an simple and easy high level interface)
  * matplotlib v3.5.1 (python plotting package)
* HTML, CSS
  * bootstrap v3.3.7 (css framework)
* Javascript
  * jquery (javascript library)
* SQL Database
  * mysql (database management system)

# Preview Home Page

![Homepage](https://user-images.githubusercontent.com/56705867/175541573-e46c81fb-f30c-4014-ab97-3982080bf8c5.jpg)
![Homepage](https://user-images.githubusercontent.com/56705867/175542097-0efcc534-88fa-4344-bce4-ae34fccd0f85.jpg)

# Preview Testing (Automatic Identification with All of Dataset and Choose Models with Parameters Input)

![image](https://user-images.githubusercontent.com/56705867/179348236-c5bce6e6-646f-4a5e-95fc-eccd444e705a.png)

# Preview Idenrification (Input File for User and Use The Best Model)

![image](https://user-images.githubusercontent.com/56705867/179348194-cefca9ad-be6d-4515-9e26-0f34cb76ffeb.png)
