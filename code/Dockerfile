FROM python:3.7-stretch
COPY . /code
WORKDIR /code
RUN mkdir ./app/trained_model
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip3 install torch==1.8.1+cpu torchvision==0.9.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install transformers==4.6.1

EXPOSE 5000
CMD flask run --host=0.0.0.0