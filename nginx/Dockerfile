FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./static /usr/share/nginx/html/static
COPY ./index.html /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
