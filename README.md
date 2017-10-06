django-la-carousel
==================

Django app for a simple responsive carousel management

- Install requirements based in file `requirements.txt` into your project;

- Copy `carousel` APP folder to your project;

- Add carousel into `INSTALLED_APPS`;

- Execute `python manage.py syncdb`;

- Access your django admin and visit the carousel app;

- Call the templatetags, js, css into your template and generate carousel. Ex.:
    ``` html
    {% load carousel_tags %}
    
    <!-- Latest JQuery -->
    <script src=" ""https://code.jquery.com/jquery-3.1.1.min.js" type="text/javascript" charset="utf-8"></script>
    
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    
    {% generate_carousel 'principal' %}
    ```