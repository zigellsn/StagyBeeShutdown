FROM stagybee/python-base:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV RUN_IN_CONTAINER 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt && \
    rm -f ./requirements.txt

COPY --chown=pyuser:users main ./

USER pyuser

ENTRYPOINT ["python", "/home/pyuser/sbshutdown.py"]