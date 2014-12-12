#!/bin/bash
# Run this script from 'scripts' directory of mallet directory

# Define location of generated input file for mallet
dir=`ls -d ../../inputForMallet/`

files=`ls -d ../../inputForMallet/*`
for file in $files
do	
	name=`basename $file`
	echo $name	
	if [[ $name == "version-major.txt" ]]
	then 
		continue
	fi
	# Create a directory named LDA and put all of the mallet traning and test 
	mkdir -p ${dir}"LDA"


	../bin/mallet import-file --input $file --output ${dir}"LDA/"${name}".mallet" --keep-sequence --remove-stopwords
		# Split data into 80% training and 20% testing
	../bin/mallet split --input ${dir}"LDA/"${name}".mallet" --training-file ${dir}"LDA/"${name}"-train.mallet" --testing-file ${dir}"LDA/"${name}"-test.mallet" --training-portion 0.8
done