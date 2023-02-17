#!/bin/bash

ROOTPATH=`pwd`
VERSION="v1.0"

# 构建docker image镜像并导出tar包
function build_image() {
    rm keys.tar
    cd ${ROOTPATH}/../
    echo -e "-------------开始构建Docker镜像-------------"
    docker build -t keys:${VERSION} ./
    echo -e "-------------构建完成-------------"
    echo -e "-------------开始导出TAR包-------------"
    docker save -o keys.tar keys:${VERSION}
    mv keys.tar ${ROOTPATH}
    echo -e "-------------导出完成-------------"
}

# 导入tar包并创建docker container
function install() {
    cd ${ROOTPATH}
    echo -e "-------------开始导入Docker镜像-------------"
    docker load -i keys.tar
    echo -e "-------------导入完成-------------"
    echo -e "-------------开始创建Docker容器-------------"
    docker run -itd --name=keys -v /etc/localtime:/etc/localtime -v /etc/timezone:/etc/timezone --network=host keys:${VERSION}
    echo -e "-------------创建完成-------------"
}

function uninstall() {
    echo -e "-------------开始卸载Docker容器及镜像-------------"
    containerID=`docker ps -a | grep keys | awk '{print $1}'`
    echo -e "容器ID: ${containerID}"
    docker stop ${containerID}
    docker rm -f ${containerID}
    imageID=`docker images | grep keys | awk '{print $3}'`
    echo -e "镜像ID: ${imageID}"
    docker rmi -f ${imageID}
    echo -e "-------------卸载完成-------------"
}

if [[ -z $1 ]]; then
  echo -e "Usage:\n  -b:构建docker image镜像并导出tar包\n  -i:导入tar包并创建docker container\n  -r:卸载docker容器及镜像\n  -v:查看当前版本"
fi
if [[ $1 == "-b" ]]; then
  build_image
fi
if [[ $1 == "-i" ]]; then
  install
fi
if [[ $1 == "-r" ]]; then
  uninstall
fi
if [[ $1 == "-v" ]]; then
  echo -e "当前版本: ${VERSION}"
fi

