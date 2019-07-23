rsync -avP -e 'ssh -p 18765' davebrau@ns1.us69.siteground.us:~/public_html/turk/data/dissertation/dissertationExperiment1/*.txt /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp1/dataProcessing/txtData/
./dataProcessing.py /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp1/dataProcessing/txtData/pilot/real/*.txt /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/production/exp1/dataProcessing/txtData/*.txt
Rscript --vanilla /home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/analysis/exp1/scripts/knitAnalysis.r
/home/dave/OneDrive/Research/By\ Project/Dissertation/experiments/upload.sh
firefox https://davebraun.org/results &
