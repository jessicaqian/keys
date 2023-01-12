FROM python:3.6
WORKDIR /home/keys
COPY . /home/keys
RUN ln -s /home/keys/lib/libaci.so /usr/lib/
RUN pip3 install requests
RUN pip3 install logging
RUN pip3 install Django==2.1.15 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install /home/keys/lib/STPython-2.0.5-cp36-cp36m-linux_x86_64.whl
RUN pip3 install /home/keys/lib/psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.whl


CMD ["python3","createtable.py"]
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
