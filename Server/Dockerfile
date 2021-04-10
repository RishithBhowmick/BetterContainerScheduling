FROM python:3
RUN ["apt","-qq","update"]
RUN ["apt","-q","install","-y","kmod"]
RUN ["pip","install","uptime"]
COPY . .
EXPOSE 5000
CMD ["python","server.py"]