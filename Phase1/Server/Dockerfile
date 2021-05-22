FROM python:3
RUN ["apt","-qq","update"]
RUN ["apt","-q","install","-y","kmod"]
RUN ["pip","install","uptime"]
EXPOSE 5000
COPY . .
CMD ["python","server.py"]