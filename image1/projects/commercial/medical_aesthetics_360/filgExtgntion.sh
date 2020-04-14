#!/bash/bin


# replace space with _ for files
for file in *; do 
  replace=`echo $file | tr '.jpeg' '.jpg'`;
  if [ $replace != $file ]; then
    mv "$file" "$replace"; 
  fi
done

