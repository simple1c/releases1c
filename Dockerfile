FROM python:slim

RUN pip install --upgrade releases1c

#ENTRYPOINT [ "python","-m", "releases1c" ]