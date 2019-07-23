## sync local directory with remote
rsync -avP -e 'ssh -p 18765' davebrau@ns1.us69.siteground.us:~/public_html/turk/data/dissertation/dissertationExperiment1/*.txt /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp1/dataProcessing/txtData/
## Convert txt data to csv and move
./dataProcessing.py /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp1/dataProcessing/txtData/pilot/real/*.txt /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp1/dataProcessing/txtData/*.txt
## Knit all markdown docs
Rscript --vanilla /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/analysis/exp1/scripts/knitAnalysis.r
## reject bots -- need to readjust for boto3
#/home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/mturk/exp1RejectBots.py
## Upload modified markdown docs to live
/home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/upload.sh
## Check it out
firefox https://davebraun.org/results &
