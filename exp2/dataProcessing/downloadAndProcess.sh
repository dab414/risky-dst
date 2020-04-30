## rsync from server
rsync -avP -e 'ssh -p 18765' davebrau@ns1.us69.siteground.us:~/public_html/turk/data/dissertation/dissertationExperiment2/*.txt /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp2/dataProcessing/txtData/
## convert usable data
./dataProcessing.py txtData/*.txt 
## knit markdowns
Rscript --vanilla /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/analysis/exp2/scripts/knitAnalysis.r
## reject bots
/home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/mturk/scripts/rejectBots.py exp2
## upload 
/home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/upload.sh
## Check it out
firefox https://davebraun.org/results &


