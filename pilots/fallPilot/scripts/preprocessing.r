library(tidyverse)
library(data.table)
source('trimSubjectRts.r')

current_data <- read.csv('../data/dissertationPilotRaw.csv')

keep <- t(matrix(c("Subject", "subject",
                   "Procedure.SubTrial.", "procedure",
                   #"responselocation.SubTrial.","responselocation",
                   "pSwitch", "pSwitch",
                   
                   #"blocks.Sample", "block",
                   "stim1.SubTrial.", "stim",
                   "SubTrial", "trial",
                    "Taskcode","taskcode",
                    "transition","transition",
                   "stimulus2.RT","rt"
),nrow=2))

current_data <- current_data[,keep[,1]]

colnames(current_data) <- keep[,2]

# realizing startblock wasn't coded for in the transition var4
current_data <- current_data %>% 
  filter(procedure == 'cuedproc') %>% 
  mutate(startBlock = ifelse(pSwitch != shift(pSwitch), 1, 0),
         error = ifelse(taskcode == 'error', 1, 0),
         errortrim = ifelse(taskcode == 'error' | shift(taskcode) == 'error', 1, 0))

current_data <- current_data[2:(nrow(current_data)),]

errorSubjects <- current_data %>% 
  group_by(subject) %>% 
  summarize(error = mean(error)) %>% 
  mutate(flag = ifelse(error > .15, '*',''))

paste('Number of subjects with error rates > .15: ', nrow(errorSubjects[errorSubjects$flag == '*',]))

## trimming
current_data <- current_data[!current_data$subject %in% errorSubjects[errorSubjects$error>.15,'subject'],]
current_data <- trimSubjectRts(current_data)
current_data <- current_data %>% 
  ##filter(errortrim == 0, startBlock == 0) %>% 
  ## not filtering out errors so that they can be analyzed
  filter(startBlock == 0) %>% 
  select(-startBlock)


write.csv(current_data, '../data/dissertationPilot.csv', row.names = FALSE)






