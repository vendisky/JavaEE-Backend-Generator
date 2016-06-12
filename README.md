# JavaEE-Backend-Generator
JavaEE Backend Generator, based on Hibernate 5.x and Spring 4.x

### How to use

Edit txt files in 'entity' directory

> txt file name: class name

> txt file content: attribute type, attribute name

Remember to leave the last line blank

<br/>

Edit config.py

in config.py, 'entities' is a list which could contain multiple class names

then run javaeeGen.py

### Output

4 backend layers: model -> dao -> service -> controller