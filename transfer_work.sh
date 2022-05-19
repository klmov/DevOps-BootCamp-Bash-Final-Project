#!/usr/bin/env bash

currentVersion="1.23.0"
down="false"

httpDownload()
{
    curl -A curl --progress-bar -o "$tempOutputPath/$3" "https://transfer.sh/$2/$3" || { echo "Failure!"; return 1;}
}

singleDownload()
{
  if [[ ! -d $1 ]];then { echo "Directory doesn't exist, creating it now..."; mkdir -p "$1";};fi
  tempOutputPath=$1
  if [ -f "$tempOutputPath/$3" ];then
    echo -n "File aleady exists at $tempOutputPath/$3, do you want to delete it? [Y/n] "
    read -r answer
    if [[ "$answer" == [Yy] ]] ;then
      rm -f "$tempOutputPath"/"$3"
    else
      echo "Stopping download"
      return 1
    fi
  fi
  echo "Downloading $3"
  httpDownload "$tempOutputPath" "$2" "$3"
  echo "Success!"
}

httpSingleUpload()
{
    response=$(curl -A curl --progress-bar --upload-file "$1" "https://transfer.sh/$2") || { echo "Failure!"; return 1;}
}

printUploadResponse()
{
fileID=$(echo "$response" | cut -d "/" -f 4)
  cat <<EOF
Transfer Download Command: transfer.sh -d desiredOutputDirectory $fileID $tempFileName
Transfer File URL: $response
EOF
}

singleUpload()
{
  filePath=$(echo "$1" | sed s:"~":"$HOME":g)
  if [ ! -f "$filePath" ];then { echo "Error: invalid file path"; return 1;}; fi
  tempFileName=$(echo "$1" | sed "s/.*\///")
  echo "Uploading $tempFileName"
  httpSingleUpload "$filePath" "$tempFileName"
}

while getopts ":d" opt; do
  case "$opt" in
    \?) echo "Invalid option: -$OPTARG" >&2
      exit 1
    ;;
    d)
      down="true"

      inputFilePath=$(echo "$*" | sed s/-d//g | sed s/-o//g | cut -d " " -f 2)
      inputID=$(echo "$*" | sed s/-d//g | sed s/-o//g | cut -d " " -f 3)
      inputFileName=$(echo "$*" | sed s/-d//g | sed s/-o//g | cut -d " " -f 4)
    ;;
    :)  echo "Option -$OPTARG requires an argument." >&2
      exit 1
    ;;
  esac
done

if [[ $# == "0" ]]; then
  usage
  exit 0
elif [[ $# == "1" ]];then
  if [[ $1 == "help" ]]; then
    usage
    exit 0
  elif [ -f "$1" ];then
    singleUpload "$1" || exit 1
    printUploadResponse
    exit 0
  else
    echo "Error: invalid filepath"
    exit 1
  fi
else
  if $down ;then
    singleDownload "$inputFilePath" "$inputID" "$inputFileName" || exit 1
    exit 0
  fi
fi