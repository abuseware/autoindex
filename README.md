What is it?
================================================================================
AutoIndex is a small and fast index generator written in Python.

Advantages over httpd built-in generators
================================================================================
  * More info about files
  * Customizable
  * Skinnable

Disadvantages
================================================================================
  * Possibly much slower than built-in one

Requirements
================================================================================
  * Python 3.1 or newer
  * Flask 0.10 or newer
  * UWSGI or other WSGI/FastCGI wrapper
  * Standalone HTTP server (Apache, Lighttpd, NGINX, ...)

How to launch?
================================================================================
Use UWSGI daemon, ex:

    # uwsgi --plugin python --uid http --gid http -s /tmp/autoindex.sock --module main:web

Example of use with NGINX
================================================================================
    server {
        root /var/www/public_html;

        try_files $uri @autoindex;
        error_page 403 =200 @browse;

        location /static {
            alias /var/www/autoindex/static;
        }

        location /get {
            types { }
            default_type application/octet-stream;
            rewrite ^/get/(.+)$ /$1 break;
        }

        location @autoindex {
            include uwsgi_params;
            uwsgi_pass unix:/tmp/autoindex.sock;
        }
        
        location @browse {
            rewrite ^ /browse/ redirect;
        }
    }
