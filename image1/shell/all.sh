
#! /bash/bin

# move all the photos in 1500px dir to the parent dir and delete the 1500px folder
for d in $(find . -type d -name "1500px")
do
  #Do something, the directory is accessible with $d:
  echo "$d"
  rm -r "$d"
  
done 
