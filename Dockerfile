# start by pulling the python image
FROM python:3.9-alpine3.16

# copy the requirements file into the image
COPY ./requirements.txt /requirements.txt

# switch working directory
WORKDIR /

# install libfi library
RUN apk add libffi-dev

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /

# configure the container to run in an executed manner
ENTRYPOINT [ "unicorn" ]

CMD ["app:app --reload" ]