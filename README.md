<p align="center">
  <img src="assets/logo.png" width="75%"/>
</p>

## What is LitMind Dictionary?

LitMind Dictionary(https://dictionary.litmind.ink) is an open-source online generative dictionary that takes a word and context containing the word as input and automatically generates a definition as output.

<p align="center">
  <img src="assets/main_arch.png" width="75%"/>
</p>

## Our System
### Workflow

The overall workflow of LitMind Dictionary

<p align="center">
  <img src="assets/work_flow.png" width="50%" />
</p>

### Definition Generation Model

The definition generation model (DGM) shown in the figure below is the core component of LitMind Dictionary. It is used to automatically generate the definition of a given word. The whole model is a transformer based encoder-decoder
model, where the encoder is initialized with BERT.

<p align="center">
  <img src="assets/model.png" width="60%" />
</p>

## How to Run This Code?
### Web

LitMind Dictionary's web interface is developed based on the [VUE](https://cn.vuejs.org/index.html) framework.
You may install [npm](https://www.npmjs.com/) package management tool first, and run the following commands to run our web interface locally.

``` bash
# init the project and install modules
npm install

# local run
npm run dev
```

### Server

#### Requirements
- tornado
- requests
- sqlalchemy
- captcha
- numpy

#### How to run the code
After installing the dependency packages, you can run the code using the command:

``` bash
cd server
python app.py
```
