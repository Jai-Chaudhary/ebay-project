#!/bin/bash
#Run this script from 'scripts' directory of mallet directory

# Define location of generated input file for mallet
	dir=`ls -d ../../inputForMallet/`

	# Read the input-file.txt file 
	# input-file.txt file has a name of a input file on each line 
	# we would like to run LDA over a range of number of topics and
	# calculae perplexity for each number of topics
	inputFiles=${dir}"input-file.txt"
	# Convert to unix format
	# Following command is equivalent to running dos2unix command
	# Some systems do not have dos2unix installed, hence using tr to delete '/r'
	# that Windows puts in the files
	tr -d '\r' < $inputFiles > ${dir}"input-file-unix.txt"
	files=`cat ${dir}"input-file-unix.txt"`
	rm -f ${dir}"input-file-unix.txt"


	for file in $files
	do
		# Train LDA model for a range of number of topics
		# and calculate perplexity for each
		numTopics=`seq 250 30 490`
		for idx in ${numTopics}
		do
			echo -e "#######################################################################"
			echo -e "         File: "${file}" Iteration: "${idx}
			echo -e "#######################################################################"

			# Train LDA model
			../bin/mallet train-topics --num-topics ${idx} --input ${dir}"LDA/"${file}".txt-train.mallet" --evaluator-filename ${dir}"LDA/"${file}"-evaluator" --num-iterations 200 --show-topics-interval 1000 --alpha 50.0 --beta .01
			# Calculate perplexity on test data
			# First calculate document probabilities for each 
			# test document
			../bin/mallet evaluate-topics --evaluator ${dir}"LDA/"${file}"-evaluator" --input ${dir}"LDA/"${file}".txt-test.mallet" --output-doc-probs ${dir}"LDA/"${file}"-docprobs.txt"
			# Calculate document lengths to calculate perplexity
			../bin/mallet run cc.mallet.util.DocumentLengths --input ${dir}"LDA/"${file}".txt-test.mallet" > ${dir}"LDA/"${file}"-doclengths.txt"
			# Calculate perplexity
			docLen=($(cat ${dir}"LDA/"${file}"-doclengths.txt"))
			docProb=($(cat ${dir}"LDA/"${file}"-docprobs.txt"))
			logLikelihood=0
			totalWords=0
			for ((i=0; i<${#docProb[@]}; i++))
			do
				logLikelihood=`echo "$logLikelihood + ${docProb[$i]}" | bc -l`
				totalWords=`echo "$totalWords + ${docLen[$i]}" | bc -l`
			done
			perplexity=`echo "e(-1*$logLikelihood / $totalWords)" | bc -l`
			ppx[$idx]=$perplexity
		done
		# Write perplexity values to a file
		rm -f ${dir}"LDA/"${file}"-perplexity.txt"
		for idx in ${numTopics}
		do
			echo -e $idx"\t"${ppx[$idx]} >> ${dir}"LDA/"${file}"-perplexity.txt"
		done

                # Delete intermediate files
                rm -f ${dir}"LDA/"${file}"-evaluator"
                rm -f ${dir}"LDA/"${file}"-doclengths.txt"
                rm -f ${dir}"LDA/"${file}"-docprobs.txt"
	done
