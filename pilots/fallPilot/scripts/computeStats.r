library(tidyverse)
library(ez)
library(magrittr)

pilot <- read.csv('../data/dissertationPilot.csv')


### I'm going to get the R*2 for both relationships, 
## and for error I think I'll run an ANOVA and do a follow-up comparison on the last two points

## create centered term
pilot$pSwitchC <- pilot$pSwitch - .5

m1 <- lm(rt ~ pSwitchC, data = pilot[pilot$error == 0,])
m2 <- lm(error ~ pSwitchC, data = pilot)

## save results
sink(file = 'regressionResults.txt')
summary(m1)
summary(m2)
sink(NULL)

pilot$rtProba <- with(pilot, m1$coefficients['(Intercept)'] + pSwitchC * m1$coefficients['pSwitchC'])

pilot %<>% 
  mutate(pSwitchC = pSwitchC + .5) 

## just for fun
pilot %>%
  group_by(pSwitchC) %>% 
   summarize(rtProba = mean(rtProba)) %>% 
   ggplot(aes(x = pSwitchC, y = rtProba)) + 
  geom_point(data = pilot, aes(x = pSwitchC, y = rt), alpha = .2) + 
  geom_jitter(data = pilot, aes(x = pSwitchC, y = rt)) +
   geom_point(size = 3, color = 'blue') +
   geom_line(size = 2, color = 'blue') +
 scale_x_continuous(breaks = seq(0,1,.1), labels = seq(0,1,.1)) +
   ylab('Response Time (ms)') +
   xlab('Probability of Switching') +
   theme_bw()
  

### ANOVA stuff

## summarize means first

sink(file='cellMeans.txt')
pilot %>% 
   filter(error == 0) %>% 
   group_by(subject, pSwitch) %>% 
   summarize(rt1 = mean(rt)) %>% 
   group_by(pSwitch) %>% 
   summarize(rt = mean(rt1), se = sd(rt1)/sqrt(n()))

pilot %>% 
   group_by(subject, pSwitch) %>% 
   summarize(error1 = mean(error)) %>% 
   group_by(pSwitch) %>% 
   summarize(error = mean(error1), se = sd(error1)/sqrt(n()))
sink(NULL)

sink(file = 'anovaResults.txt')
print('This is a contrast between 0.9 and 1 levels of pSwitch for RT and errors from two separate ANOVAs')
## rt anova
pilot$pSwitch <- as.factor(pilot$pSwitch)
mRt <- ezANOVA(data = pilot[pilot$error == 0,], wid = subject, within = pSwitch, dv = rt, detailed = TRUE)
omniSsd <- mRt$ANOVA$SSd[2]
omniDfn <- mRt$ANOVA$DFn[2]
omniDfd <- mRt$ANOVA$DFd[2]
mRtFollow <- ezANOVA(data = pilot[pilot$pSwitch == .9 | pilot$pSwitch == 1 & pilot$error == 0,], wid = subject, within = pSwitch, dv = rt, detailed = TRUE)
ssn <- mRtFollow$ANOVA$SSn[2]
dfn <- mRtFollow$ANOVA$DFn[2]

msn <- ssn / dfn
msd <- omniSsd / omniDfd
Fcalc <- msn / msd
p <- pf(Fcalc, dfn, omniDfd, lower.tail = FALSE)

print(paste('RT: F(',dfn,', ', omniDfd,') = ', round(Fcalc,2), ', p = ', round(p,2), sep = ''))

## error anova
pilot$pSwitch <- as.factor(pilot$pSwitch)
mError <- ezANOVA(data = pilot, wid = subject, within = pSwitch, dv = error, detailed = TRUE)
omniSsd <- mError$ANOVA$SSd[2]
omniDfn <- mError$ANOVA$DFn[2]
omniDfd <- mError$ANOVA$DFd[2]
mErrorFollow <- ezANOVA(data = pilot[pilot$pSwitch == .9 | pilot$pSwitch == 1,], wid = subject, within = pSwitch, dv = error, detailed = TRUE)
ssn <- mErrorFollow$ANOVA$SSn[2]
dfn <- mErrorFollow$ANOVA$DFn[2]

msn <- ssn / dfn
msd <- omniSsd / omniDfd
Fcalc <- msn / msd
p <- pf(Fcalc, dfn, omniDfd, lower.tail = FALSE)

print(paste('Errors: F(',dfn,', ', omniDfd,') = ', round(Fcalc,2), ', p = ', round(p,2), sep = ''))
sink(NULL)




















