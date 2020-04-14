#! /bash/bin



# replace space with underscore
cd $PWD;
# replace space with _ for files
for file in *; do 
  replace=`echo $file | tr ' ' '_'`;
  if [ $replace != $file ]; then
    mv "$file" "$replace"; 
  fi
done

# change uppper case to lower case
for x in `ls`
  do
    if [ ! -d $x ]; then
      continue
    fi

  lc=`echo $x  | tr '[A-Z]' '[a-z]'`;
  if [ $lc != $x ]; then
    mv $x $lc;
  fi
done

# remove the commercial substring
for y in `ls`
  do
    if [ ! -d $y ]; then
      continue
    fi
    replace2=`echo "$y"|sed 's/__/_/'`
    mv $y $replace2
done

# find . ! -path . -maxdepth 1 -type d -exec echo $(eval basename {}) \;
