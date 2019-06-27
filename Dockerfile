FROM python:3.6
ADD . /app
WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
RUN pip install --user pipenv
RUN pipenv install --system --deploy
RUN python manage.py migrate
RUN chmod +x ./init.sh
RUN ./init.sh
EXPOSE 8080
CMD exec python manage.py runserver 0.0.0.0:8080
