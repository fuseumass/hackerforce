FROM python:3.6
ADD . /app
WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
RUN \
  pip install --user pipenv && \
  pipenv install --system --deploy 
EXPOSE 8080
CMD chmod +x ./safe_init.sh && ./safe_init.sh && \
  python manage.py runserver 0.0.0.0:8080
