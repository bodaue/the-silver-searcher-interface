# The Silver Searcher Interface

## Description

<p>
This project is a Python graphical interface using the <a href="https://github.com/TomSchimansky/CustomTkinter">
CustomTKinter</a> and <a href="https://docs.python.org/3/library/tk">Tkinter</a> libraries for convenient interaction 
with <a href="https://github.com/ggreer/the_silver_searcher">The Silver Searcher (Ag)</a> tool.</p>
<p>This interface allows users to perform searches for text patterns in files and configure various parameters for more 
precise and user-friendly searches.</p>

## Dark Theme

<img src="static/interface_dark_theme.png" width="75%">

## Light Theme

<img src="static/interface_light_theme.png" width="75%">

## Requirements

- [Python v3.10.2](https://docs.python.org/3.10/)
- [TKinter](https://docs.python.org/3/library/tk)
- [CustomTKinter v5.2.1](https://github.com/TomSchimansky/CustomTkinter)
- [Packaging v23.2](https://pypi.org/project/packaging/)


## Installation
- Clone project
```commandline
git clone https://github.com/bodaue/the-silver-searcher-interface.git
```
- Install requirements
```commandline
pip install -r requirements.txt
```
- Rename .env.dist to .env
```
ren .env.dist .env
```

## Launch
```
python main.py
```