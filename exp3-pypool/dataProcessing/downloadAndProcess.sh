## rsync from server
rsync -avP -e 'ssh -p 18765' --exclude=*init.txt u231-f6hnzkbwb44b@davebraun.net:~/www/davebraun.net/public_html/turk/data/dissertation/dissertationExperiment3-pypool/*.txt '/home/dave/Dropbox (Lehigh University)/Research/By Project/Dissertation/experiments/production/exp3-pypool/dataProcessing/txtData/'
## convert usable data
python dataProcessing.py txtData/*.txt 
## knit markdowns
Rscript --vanilla '/home/dave/Dropbox (Lehigh University)/Research/By Project/Dissertation/experiments/analysis/exp3-pypool/scripts/knitAnalysis.r'
## upload 
bash '/home/dave/Dropbox (Lehigh University)/Research/By Project/Dissertation/experiments/upload.sh'
## Check it out
firefox https://davebraun.net/results &


