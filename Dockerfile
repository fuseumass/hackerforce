FROM python:3.6
ADD . /app
WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
RUN \
  pip install --user pipenv && \
  pipenv install --system --deploy && \
  chmod +x ./init.sh && \
  ./init.sh
EXPOSE 8080
CMD python manage.py migrate && \
  python manage.py runserver 0.0.0.0:8080
