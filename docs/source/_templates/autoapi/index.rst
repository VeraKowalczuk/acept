API Reference
=============

The following packages are part of the ACEPT project:

* acept: The main package of the project
* UrbanHeatPro: A tool to create heat demand profiles 

The API Reference for the acept package is very extensive and up-to-date with the latest version of the code.
It provides detailed information on the available modules, functions, classes, and attributes.


.. note:: 
   Unfortunately, the API reference for UrbanHeatPro might be incomplete or outdated. 
   While the documentation in the source code was updated and extended as part of this project, 
   there is no guarantee that it fits the code 100%.
   
   For example, the types of parameters or attributes might not be up-to-date with the latest version of the library.
   Therefore, it is recommended to check the respective source code if the documentation is unclear.
    

.. toctree::
   :titlesonly:

   {% for page in pages %}
   {% if page.top_level_object and page.display %}
   {{ page.include_path }}
   {% endif %}
   {% endfor %}