#!/bash/bin


# replace space with _ for files
for file in *; do 
  replace=`echo $file |sed s/\.jpeg/\.jpg/g`;
  if [ $replace != $file ]; then
    mv "$file" "$replace"; 
  fi
done

