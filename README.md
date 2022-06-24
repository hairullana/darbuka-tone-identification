# Darbuka Tone Classification

A system to identify from the basic tone and tone pattern darbuka musical instrument using [Onset Detection](https://musicinformationretrieval.com/onset_detection.html), [Mel-Frequency Cepstral Coefficient (MFCC) algorithm](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum), and [K-Nearest Neighbor (KNN) algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)

**![#f03c15](https://via.placeholder.com/15/f03c15/f03c15.png)  The tone identification functions and the darbuka tone dataset are excluded in this repository. Please contact [hairullana99@gmail.com](mailto:hairullana99@gmail.com) if you want to request a function and darbuka tone dataset**

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

# Preview Training

![Training](https://user-images.githubusercontent.com/56705867/175541700-0070649d-2ca7-4f3b-beb5-8bdf43c5a60a.jpeg)
![Training](https://user-images.githubusercontent.com/56705867/175542627-da4debf8-d9c7-4fc5-8245-7cb834b5e6b9.jpg)

# Preview Testing (Automatic Identification with All of Dataset)

![Testing](https://user-images.githubusercontent.com/56705867/175542846-026163cc-56c9-4c50-bba3-2bbd275d5b93.jpeg)
![Testing](https://user-images.githubusercontent.com/56705867/175543000-6948b8bd-e49a-462e-bc75-684f282bd94e.jpeg)

# Preview Testing (Input File)

![Testing](https://user-images.githubusercontent.com/56705867/175543489-d9d6ee51-8dc0-4868-9469-ff28797d3204.jpeg)
