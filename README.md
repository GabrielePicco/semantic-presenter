# Semantic Presenter
Multithreading server which provides a semantic analysis service

The server is developed in python (with support for multithreading) and provides a service of semantic analysis of a text or an url, generating a page composed of video images and articles concerning the topics present in the text / web page.

A statistical analysis of the words contained in the text is performed and the keywords are identified.

The project was developed for academic / educational purposes.

To start the server, install dependencies:

    $pip install -r requirements.txt

then:

    $python serverHTTP.py

The semantic analysis service will be available on the page: http://localhost:8080

The analysis of the wikipedia page on [DNS](https://en.wikipedia.org/wiki/Domain_Name_System) will produce the following result:

![](https://i.imgur.com/YOdXEkN.png?raw=true)
